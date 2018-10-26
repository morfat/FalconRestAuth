
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
from ..emails.models import EmailProvider , EmailTemplate

from ..celery_proj.tasks import send_gmail

class AuthMixin:
    """ to be used in auth classes for common methods """

    def get_tenant(self,db,host_name):
        return db.objects( Tenant.all() ).filter( host_name__eq=host_name ).fetch_one()
    
    def get_appication(self, db, application_id):
        return db.objects( Application.all() ).filter( id__eq=application_id).fetch_one()

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
        if email:
            #send email
            provider = db.objects( EmailProvider.gmail() ).filter(tenant_id__eq=tenant_id).fetch()[0]
            template = db.objects( EmailTemplate.account_created() ).filter(tenant_id__eq=tenant_id).fetch()[0]

            send_gmail.delay(provider,template, recipient=email, body_replace_params = {"password":raw_password})

        return user





class RetrieveUpdateUser(RetrieveUpdateResource):
    login_required = True

    model = User

    serializer_class = UserSerializer




class RegisterUser(CreateResource, ClientMixin, AuthMixin):
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

        #client_id = posted_data.pop("client_id",None)
        #client = self.get_client(db,client_id)
        host_name = posted_data.pop("host_name")
        agree = posted_data.pop("agree", None)
        tenant = self.get_tenant(db,host_name)
        tenant_id = tenant.get("id")
        application = self.get_appication(db,application_id=tenant.get("application_id") )
        auth_username_field = application.get("auth_username_field")

        email = posted_data.get("email")
        user_password =  posted_data.get("password")
        phone_number = posted_data.get("phone_number")
        organization_name = posted_data.pop("organization_name",None)
        organization_id  = None

        #check to know what 
        if auth_username_field == 'email':
            if email is None:
                raise falcon.HTTPBadRequest(description="Email is needed")

        elif auth_username_field == 'phone_number':
            if phone_number is None:
                raise falcon.HTTPBadRequest(description="Phone Number is needed")
        #

        posted_data.update({"tenant_id":tenant_id})
        tenant = db.objects( Tenant.get( pk=tenant_id) ).fetch()[0]


        #create user
        raw_password = user_password if user_password else  self.model.get_random_password()
        
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
        #send email
        if email and not user_password:
            try:
                provider = db.objects( EmailProvider.gmail() ).filter(tenant_id__eq=tenant_id).fetch()[0]
                template = db.objects( EmailTemplate.account_created() ).filter(tenant_id__eq=tenant_id).fetch()[0]

                send_gmail.delay(provider,template, recipient=email, body_replace_params = {"password":raw_password})
            except IndexError:
                print("Email not configured")
                print("PAssword", raw_password)


        #to avoid error when client id is not given
        #req.context['auth'] = {"client_id": client_id, "tenant_id": tenant_id}

        return user
    
    def on_post(self,req,resp):
        db = self.get_db(req)
        posted_data = req.media
        serializer = self.get_serializer_class()(posted_data)
        #data = serializer.valid_write_data

        resp.media = { "data": [ self.perform_create(req,db,posted_data) ] }





class LoginUser(CreateResource,ClientMixin):
    
    serializer_class = LoginUserSerializer
    login_required = False

    def on_post(self,req,resp):
        db = self.get_db(req)
        posted_data = req.media
        serializer = self.get_serializer_class()(posted_data)
        data = serializer.valid_write_data

        #get client
        host_name = posted_data.get("host_name")
        tenant = db.objects( Tenant.all() ).filter( host_name__eq=host_name ).fetch_one()
        tenant_id = tenant.get("id")
        application_id = tenant.get("application_id")
        application = db.objects( Application.all() ).filter( id__eq=application_id).fetch_one()
        
        try:
            api = db.objects( API.default_tenant_api(tenant_id) ).fetch_one()
        except IndexError:
            raise falcon.HTTPBadRequest(description="Default Resource Server on every Tenant is needed")

        #get user
        auth_username_field = application.get("auth_username_field")
        email = data.get("email")
        phone_number = data.get("phone_number")
        password = data.get("password")
        user = None
        user_queryset =  db.objects( User.all() ).filter(tenant_id__eq = tenant_id)

        #check to know what 
        if auth_username_field == 'email':
            if email is None:
                raise falcon.HTTPBadRequest(description="Email is needed")
            
            user = user_queryset.filter( email__eq = email ).fetch_one()

            #check if password is valid
            if not User.is_valid_password(user.get("password"), password):
                raise falcon.HTTPBadRequest(title="Login Failed",description="Valid Email and Password is needed")
                

        
        elif auth_username_field == 'phone_number':
            if phone_number is None:
                raise falcon.HTTPBadRequest(description="Phone Number is needed")
            
            user = user_queryset.filter( phone_number__eq = phone_number ).fetch_one()

            #check if password is valid
            if not User.is_valid_password(user.get("password"), password):
                raise falcon.HTTPBadRequest(title="Login Failed",description="Valid Phone number and Password is needed")
                

        #claims
        token_lifetime = api.get("token_lifetime_web")

        issued_at = datetime.datetime.now() #datetime.datetime.utcnow()
        expires_at = issued_at +  datetime.timedelta(seconds = token_lifetime)

       
        user_id = user.get("id")

        user_profile = {  "organization_id":None, "is_organization_admin":None, "is_staff":user.get("is_staff"),
                          "is_super_user":user.get("is_super_user"), "first_name":user.get("first_name"), 
                          "last_name": user.get("last_name") 
                        }
        
        #make access and id tokens

        access_token_claims = { 
                    "iat": int(issued_at.timestamp()),
                    "exp": int(expires_at.timestamp()) ,
                    #"client_id":client_id,
                    "tenant_id": tenant_id,
                    "sub": user_id
                }
        
        #get user organization
        user_organization = None
        try:
            user_organization = db.objects( OrganizationUser.user_organization(user_id) ).fetch()[0]
            user_profile.update({"organization_id": user_organization.get("organization_id"), "is_organization_admin": user_organization.get("is_admin")})
            access_token_claims.update({"user_organization_id": user_organization.get("organization_id"), "user_is_organization_admin": user_organization.get("is_admin")})
        except IndexError:
            pass

        #get signning key. 
        api_signing_key = api.get("signing_secret")
        application_signing_key = None

        if not api_signing_key:
            #get application signing key
            #application_id = tenant.get("application_id")
            #application = db.objects( Application.get( application_id) ).fetch()[0]
            
            application_signing_key = application.get("signing_secret")

            #print (application_signing_key)
            #print("FOR APP")
        
        secret_key = api_signing_key or application_signing_key
        
        #print (secret_key)



        resp.media = {"access_token": self.generate_encrypted_token(key = self.get_signing_secret(key = secret_key ), claims = access_token_claims),
                      "token_type": "Bearer", 
                      "expires_in": token_lifetime , 
                      "user_profile":user_profile
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
        tenant_id = auth.get("tenant_id")
        current_password = posted_data.get("current_password")

        user = db.objects( self.model.get(user_id) ).fetch()[0]


        #check if password is valid

        if not User.is_valid_password(user.get("password"), current_password):
            raise falcon.HTTPBadRequest(description="Invalid Current Password")
        
        #change password

        self.model.set_password(db =db , user_id = user_id, password = posted_data.get("new_password"))

        #@TODO 
        #send email on password changed successfully
        email = user.get("email")

        if email:
            #send email
            provider = db.objects( EmailProvider.gmail() ).filter(tenant_id__eq=tenant_id).fetch()[0]
            template = db.objects( EmailTemplate.password_changed() ).filter(tenant_id__eq=tenant_id).fetch()[0]

            send_gmail.delay(provider,template, recipient=email)




        return {}



class UserResetPassword(CreateResource,ClientMixin, AuthMixin):
    
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

        host_name = posted_data.pop("host_name")

        tenant = self.get_tenant(db,host_name)
        tenant_id = tenant.get("id")
        application = self.get_appication(db,application_id=tenant.get("application_id") )
        auth_username_field = application.get("auth_username_field")

        
        #client_id = posted_data.pop("client_id")
        #client = self.get_client(db,client_id)

        #tenant_id = client.get("tenant_id")
        email = posted_data.get("email")
        phone_number = posted_data.get("phone_number")

        #check to know what 
        if auth_username_field == 'email':
            if email is None:
                raise falcon.HTTPBadRequest(description="Email is needed")

        elif auth_username_field == 'phone_number':
            if phone_number is None:
                raise falcon.HTTPBadRequest(description="Phone Number is needed")
        #

        posted_data.update({"tenant_id":tenant_id})
        #tenant = db.objects( Tenant.get( pk=tenant_id) ).fetch()[0]


        queryset = db.objects( User.all() ).filter(tenant_id__eq=tenant_id)

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
        raw_password = random_password

        print (random_password)

        self.model.set_password(db =db , user_id = user.get("id"), password = random_password)

        #@TODO 
        #send email on password reset successfully
        if email:
            try:
                #send email
                provider = db.objects( EmailProvider.gmail() ).filter(tenant_id__eq=tenant_id).fetch()[0]
                template = db.objects( EmailTemplate.password_reset() ).filter(tenant_id__eq=tenant_id).fetch()[0]

                send_gmail.delay(provider,template, recipient=email, body_replace_params = {"password":raw_password})
            except IndexError:
                print("provider not configured")

        return {}