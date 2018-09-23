
import falcon

from .models import User , OrganizationUser
from ..tenants.models import Tenant
from ..clients.models import Client
from ..clients.mixins import ClientMixin
from ..apis.models import API
from ..applications.models import Application

from ..organizations.models import Organization

from .serializers import UserSerializer , LoginUserSerializer, UserRegisterSerializer,UserChangePasswordSerializer
from . import serializers


from falchemy_rest.resources import ListCreateResource ,RetrieveUpdateResource,CreateResource



from jwcrypto import jwk,jwt

import json
import datetime

class ListCreateUsers(ListCreateResource):
    """ 
    
    We expect client_id to be passed for non authorized logins.

    """

    login_required = True

    model = User

    filterable_fields = ()
    searchable_fields = ('name',)

    serializer_class = UserSerializer

    def perform_create(self,req,db,posted_data):
        tenant_id =   self.get_auth_tenant_id(req)

        print (tenant_id)

        email = posted_data.get("email")
        phone_number = posted_data.get("phone_number") 
        organization_id = posted_data.pop("organization_id", None)
       

        if  not phone_number and not email:
            raise falcon.HTTPBadRequest(title="Missing Field", description="either phone_number or email field is needed")

        
        #create user
        raw_password = self.model.get_random_password()
        
        print (raw_password)

        posted_data.update({"tenant_id": tenant_id})

        user = db.objects( self.model.insert() ).create(**posted_data)
        user_id = user.get("id")


        #set user password 
        self.model.set_password(db =db , user_id = user_id, password = raw_password)


        tenant = db.objects( Tenant.get( pk=tenant_id) ).fetch()[0]


        if 'B2B' == tenant.get("business_mode"):
            if not organization_id:
                raise falcon.HTTPBadRequest( title="Organization is required for B2B business mode",
                                             description="Either organization_id field is required."
                                            )
            else:
                #add organization user  if required
                db.objects( OrganizationUser.insert() ).create(**{"organization_id": organization_id,"user_id":user_id})

        #send user email or sms 
        #@TODO 

        return user





class RetrieveUpdateUser(RetrieveUpdateResource):
    login_required = True

    model = User

    serializer_class = UserSerializer




class RegisterUser(CreateResource, ClientMixin):
    """ 

    Use this endpoint to create new users only. For unauthenticated use only.

    #we expect multisite logins here irrespective of same client
    Hence the main client cas to be is_first_party = True
    
    ON SPA if want to pull clients, create an endpoint to get primary_clisne i.e first_party_client client based on
    domain name
    e.g  #tenant = db.objects( Tenant.get(host_name=req.forwarded_host)).fetch()[0]


    Then get tenant from the client.

    """

    login_required = False

    model = User

    serializer_class = UserRegisterSerializer

    



    def perform_create(self,req,db,posted_data):
        db = self.get_db(req)
        client_id = posted_data.pop("client_id",None)
        client = self.get_client(db,client_id)

        tenant_id = client.get("tenant_id")
        email = posted_data.get("email")
        phone_number = posted_data.get("phone_number")
        organization_name = posted_data.pop("organization_name",None)
        organization_id  = None

     
        if  not phone_number and not email:
            raise falcon.HTTPBadRequest(title="Missing Username Field", description="Either phone_number or email field is needed")

        
        posted_data.update({"tenant_id":tenant_id})
        tenant = db.objects( Tenant.get( pk=tenant_id) ).fetch()[0]


        #create user
        raw_password = self.model.get_random_password()
        
        print (raw_password)

        user = db.objects( self.model.insert() ).create(**posted_data)
        user_id = user.get("id")

        #set user password 
        self.model.set_password(db =db , user_id = user_id, password = raw_password)


        if 'B2B' == tenant.get("business_mode"):
            if not organization_name:
                raise falcon.HTTPBadRequest( title="Missing Organization",
                                             description="organization_name field is required."
                                            )
            else:
                # create organization
                organization_data = { "name": organization_name , "tenant_id": tenant_id}
                organization = db.objects( Organization.insert( ) ).create(** organization_data)
                organization_id = organization.get("id")
                
            #add organization user as admin

            db.objects( OrganizationUser.insert() ).create(**{"organization_id": organization_id,"user_id":user_id, "is_admin": True})

        #send user email or sms 
        #@TODO 

        return user


class LoginUser(CreateResource,ClientMixin):

    serializer_class = LoginUserSerializer
    login_required = False

    def on_post(self,req,resp):
        db = self.get_db(req)
        posted_data = req.media
        serializer = self.get_serializer_class()(posted_data)
        data = serializer.valid_write_data

        #get client
        client_id = posted_data.pop("client_id",None)
        client = self.get_client(db,client_id)
        tenant_id = client.get("tenant_id")
        tenant = db.objects( Tenant.get( pk=tenant_id) ).fetch()[0]
        
        try:
            api = db.objects( API.default_tenant_api(tenant_id) ).fetch()[0]
        except IndexError:
            raise falcon.HTTPBadRequest(description="Default API / Resource Server on every Tenant is needed")



        #get user
        email = data.get("email")
        phone_number = data.get("phone_number")
        password = data.get("password")

        if phone_number is None and email is None:
            raise falcon.HTTPBadRequest(description="Email or PhoneNumber is needed")



        queryset =  db.objects( User.all() ).filter(tenant_id__eq = tenant_id)

        if email:
            queryset = queryset.filter(email__eq = email)
        elif phone_number:
            queryset = queryset.filter(phone_number__eq = phone_number)
        
        try:
            user = queryset.fetch()[0]
        except IndexError:
            raise falcon.HTTPBadRequest(description="Insufficient user credentials. Valid Username and Password is needed")

        
        #check if password is valid
        if not User.is_valid_password(user.get("password"), password):
            raise falcon.HTTPBadRequest(title="Login Failed",description="Valid Username and Password is needed")



        #claims
        token_lifetime = api.get("token_lifetime_web")

        issued_at = datetime.datetime.now() #datetime.datetime.utcnow()
        expires_at = issued_at +  datetime.timedelta(seconds = token_lifetime)

       
        user_id = user.get("id")
       
        #make access and id tokens

        access_token_claims = { 
                    "iat":int(issued_at.timestamp()),
                    "exp":int(expires_at.timestamp()) ,
                    "client_id":client_id,
                    "tenant_id":tenant_id,
                    "sub":user_id
                }

        id_token = { "user_id": user_id, "first_name":user.get("first_name"), "last_name": user.get("last_name") }
        
        #get signning key. 
        api_signing_key = api.get("signing_secret")
        application_signing_key = None

        if not api_signing_key:
            #get application signing key
            application_id = tenant.get("application_id")

            application = db.objects( Application.get( application_id) ).fetch()[0]
            application_signing_key = application.get("signing_secret")

            print (application_signing_key)
            print("FOR APP")
        
        secret_key = api_signing_key or application_signing_key
        
        print (secret_key)



        resp.media = {"access_token": self.generate_encrypted_token(key = self.get_signing_secret(key = secret_key ), claims = access_token_claims),
                      "token_type": "Bearer", 
                      "expires_in": token_lifetime , 
                      "id_token":id_token
                      }



    def generate_encrypted_token(self,key,claims):

        token = jwt.JWT( header = {"alg": "HS256"}, claims = claims )

        #sign token
        token.make_signed_token(key)
        #encrypt token
        etoken = jwt.JWT( header = {"alg": "A256KW", "enc": "A256CBC-HS512"},claims = token.serialize() )
        etoken.make_encrypted_token(key)
        return  etoken.serialize()
    
    def get_signing_secret(self,key):
        k = {"k":key, "kty":"oct"}
        return jwk.JWK(**k)
    




class UserChangePassword(CreateResource):
    
    """
    Change Password
    """

    login_required = True

    model = User

   
    serializer_class = UserChangePasswordSerializer

    def on_post(self,req,resp):

        db = self.get_db(req)
        posted_data = req.media
        serializer = self.get_serializer_class()(posted_data)
        posted_data = serializer.valid_write_data

        auth = self.get_auth_data(req)
        user_id = auth.get("sub")
        current_password = posted_data.get("current_password")

        user = db.objects( self.model.get(user_id) ).fetch()[0]


        #check if password is valid

        if not User.is_valid_password(user.get("password"), current_password):
            raise falcon.HTTPBadRequest(description="Invalid Current Password")
        
        #change password

        self.model.set_password(db =db , user_id = user_id, password = posted_data.get("new_password"))

        #@TODO 
        #send email on password changed successfully

        return {}



class UserResetPassword(CreateResource,ClientMixin):
    
    """
    Reset user Password
    """

    login_required = False

    model = User

   
    serializer_class = serializers.UserResetPasswordSerializer

    def on_post(self,req,resp):
        db = self.get_db(req)
        posted_data = req.media
        serializer = self.get_serializer_class()(posted_data)
        posted_data = serializer.valid_write_data
        
        client_id = posted_data.pop("client_id")
        client = self.get_client(db,client_id)

        tenant_id = client.get("tenant_id")
        email = posted_data.get("email")
        phone_number = posted_data.get("phone_number")
      
        if  not phone_number and not email:
            raise falcon.HTTPBadRequest(title="Missing Username Field", description="Either phone_number or email field is needed")

        
        posted_data.update({"tenant_id":tenant_id})
        tenant = db.objects( Tenant.get( pk=tenant_id) ).fetch()[0]


        queryset =  db.objects( User.all(tenant_id=tenant_id) )

        if email:
            queryset = queryset.filter(email__eq = email)
        elif phone_number:
            queryset = queryset.filter(phone_number__eq = phone_number)
        
        user = None

        try:
            user = queryset.fetch()[0]
        except IndexError:
            raise falcon.HTTPBadRequest(description="Account not found")

        #change password
        random_password = self.model.get_random_password()
        print (random_password)

        self.model.set_password(db =db , user_id = user.get("id"), password = random_password)

        #@TODO 
        #send email on password reset successfully

        return {}





    


    
   

        



