
import falcon

from .models import User , OrganizationUser
from ..tenants.models import Tenant
from ..clients.models import Client
from ..organizations.models import Organization

from .serializers import UserSerializer , LoginUserSerializer

from falchemy_rest.resources import ListCreateResource ,RetrieveUpdateResource,CreateResource


from jwcrypto import jwk,jwt

import json
import datetime
from falcon_rest_auth.settings import OAUTH_SECRET_KEY

class ListCreateUsers(ListCreateResource):
    """ 
    
    We expect client_id to be passed for non authorized logins.

    """

    login_required = False

    model = User

    filterable_fields = ('tenant_id',)
    searchable_fields = ('name',)

    serializer_class = UserSerializer

    def perform_create(self,req,db,posted_data):

        client_id = posted_data.pop("client_id" ,None)
        tenant_id =  posted_data.get("tenant_id")
        email = posted_data.get("email")
        phone_number = posted_data.get("phone_number")

        
        organization_id = posted_data.pop("organization_id", None)
        organization_name = posted_data.pop("organization_name",None)
        is_organization_admin = posted_data.pop("is_organization_admin",False)


        if  not phone_number and not email:
            raise falcon.HTTPBadRequest(title="Missing Field", description="either phone_number or email field is needed")

        if not tenant_id:
            #check if tenant id was given
            if not client_id:
                raise falcon.HTTPBadRequest(title="Missing Field", description="client_id field is required.")
            
            client =  db.objects( Client.all() ).filter(client_id__eq = client_id).fetch()

            tenant_id = client[0].get("tenant_id")
            posted_data.update({"tenant_id":tenant_id})
        
        tenant = db.objects( Tenant.get( tenant_id) ).fetch()[0]

        if 'B2B' == tenant.get("business_mode"):
            if not organization_id and not organization_name:
                raise falcon.HTTPBadRequest( title="Organization is required for B2B business mode",
                                             description="Either organization_id or organization_name field is required."
                                            )
            elif not organization_id:
                #make / create organization
                organization_data = { "name": organization_name , "tenant_id": tenant_id}
                organization = db.objects( Organization.insert( ) ).create(** organization_data)
                organization_id = organization.get("id")
                
               

        #create user
        raw_password = self.model.get_random_password()
        
        print (raw_password)
        

        user = db.objects( self.model.insert() ).create(**posted_data)
        user_id = user.get("id")


        #set user password 
        self.model.set_password(db =db , user_id = user_id, password = raw_password)

        #add organization user  if required
        db.objects( OrganizationUser.insert() ).create(**{"organization_id": organization_id,"user_id":user_id, "is_admin": is_organization_admin})

        #send user email or sms 
        #@TODO 

        return user





class RetrieveUpdateUser(RetrieveUpdateResource):
    login_required = False

    model = User

    serializer_class = UserSerializer




class LoginUser(CreateResource):
    serializer_class = LoginUserSerializer
    login_required = False

    def on_post(self,req,resp):
        db = self.get_db(req)
        posted_data = req.media
        serializer = self.get_serializer_class()(posted_data)

        data = serializer.valid_write_data

        #get client
        client_id = data.get("client_id")

        client = db.objects( Client.get(pk = client_id) ).fetch()[0]
        tenant_id = client.get("tenant_id")

        #get user
        email = data.get("email")
        phone_number = data.get("phone_number")
        password = data.get("password")

        queryset =  db.objects( User.all() ).filter(tenant_id__eq = tenant_id)

        if email:
            queryset = queryset.filter(email__eq = email)
        elif phone_number:
            queryset = queryset.filter(phone_number__eq = phone_number)
        
        user = queryset.fetch()[0]



        #claims
        token_lifetime = 90 #seconds

        #audience = 
        issued_at = datetime.datetime.now() #datetime.datetime.utcnow()
        expires_at = issued_at +  datetime.timedelta(seconds = token_lifetime)

       
        user_id = user.get("id")
       

        access_token_claims = { 
                    #"aud": audience,
                    "iat":int(issued_at.timestamp()),
                    "exp":int(expires_at.timestamp()) ,
                    "client_id":client_id,
                    "tenant_id":tenant_id,
                    "sub":user_id,


                }

        id_token = { "user_id": user_id, "email": user.get("email") , "phone_number": user.get("phone_number"), "first_name":user.get("first_name"), "last_name": user.get("last_name") }

        resp.media = {"access_token": self.generate_encrypted_token(key = self.get_signing_secret(key = OAUTH_SECRET_KEY ), claims = access_token_claims),
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
    






    


    
   

        



