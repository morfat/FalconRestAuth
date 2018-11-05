
#create all db
import sys

from falchemy_rest.models import Base

from falcon_rest_auth.settings import DB_ENGINE

from falchemy_rest.sql import Db 


def init_db():
    from falcon_rest_auth.applications import models
    from falcon_rest_auth.content_types import models
    from falcon_rest_auth.permissions import models
    from falcon_rest_auth.tenants import models
    from falcon_rest_auth.sites import models
    from falcon_rest_auth.organizations import models
    from falcon_rest_auth.clients import models
    from falcon_rest_auth.users import models
    from falcon_rest_auth.apis import models
    from falcon_rest_auth.emails import models
    from falcon_rest_auth.roles import models
    from falcon_rest_auth.teams import models


    Base.metadata.create_all(DB_ENGINE)



def init_app(db, app_name):
    from falcon_rest_auth.applications.models import Application
    from falcon_rest_auth.tenants.models import Tenant
    from falcon_rest_auth.sites.models import Site
    from falcon_rest_auth.apis.models import API
    from falcon_rest_auth.organizations.models import Organization
    from falcon_rest_auth.users.models import User, OrganizationUser


    auth_username_field = input("Enter App Username field ( email or phone_number ): ")

    is_multitenant_q = input("Is the Application Multitenant ? ( y , n): ")
    tenant_business_mode = input("Business Mode ? ( B2B, B2C): ")
    username = input("Enter Superuser %s: "%(auth_username_field))
    password = input("Enter Superuser Password: ")

    api_uri = input("Default Resource Server URL: ")
    is_multitenant = True if is_multitenant_q == 'y' else False

    
    created_app = db.objects( Application.insert() ).create(**{"auth_username_field": auth_username_field,"name":app_name,"is_multitenant": is_multitenant })

    #create super tenant
    application_id = created_app.get("id")
    created_tenant = db.objects( Tenant.insert() ).create(**{"is_super_tenant": True,"name":"Default","business_mode": tenant_business_mode,
                                            "application_id": application_id
                                            })
   
    
    #create default api
    tenant_id = created_tenant.get("id")
    created_api = db.objects( API.insert() ).create(**{"is_default": True,"name":"Default","description": "Default Generated",
                                            "uri": api_uri,"tenant_id": tenant_id
                                            })

    #create default site with default domain name
    created_site = db.objects( Site.insert() ).create(**{ "tenant_id": tenant_id, "domain_name":"admin.localhost" })

    #create user
    user_d = { "password": password , "is_staff": True, "is_super_user": True,
               "is_active": True, auth_username_field: username,"tenant_id": tenant_id
            }
    created_user = db.objects( User.insert() ).create(**user_d)
    user_id = created_user.get("id")

    User.set_password( db, user_id, password)
    

    #create organization
    if tenant_business_mode == 'B2B':
        created_organization = db.objects( Organization.insert() ).create(**{"name":"Default","tenant_id": tenant_id })
        db.objects( OrganizationUser.insert() ).create(**{"is_admin":True,"user_id": user_id, "organization_id": created_organization.get("id") })


#Db Tables

init_db()

# Create new app data

args = sys.argv

try:
    db = Db( DB_ENGINE.connect() )
    transaction = db._connection.begin()

    app_name = args[1]
    init_app(db, app_name)

    transaction.commit()

except IndexError:
    transaction.rollback()
finally:
    db._connection.close()



