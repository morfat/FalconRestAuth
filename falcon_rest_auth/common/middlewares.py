

from falchemy_rest import middlewares

from ..tenants.models import Tenant
from ..sites.models import Site

from ..applications.models import Application

import falcon

class CustomAuthMiddleWare(middlewares.AuthMiddleWare):
    def __init__(self):
        pass

    def get_secret_key(self,req):
        host_name = req.forwarded_host
        db =  self.get_db(req)

        site = self.get_site(db, host_name)

        if not site:
            raise falcon.HTTPForbidden(description=" Requests from this site not configured. ")

        tenant = self.get_authenticated_tenant(db, site.get("tenant_id") )
        application = self.get_authenticated_app(db, tenant.get("application_id") )

        #add the tenant and application to context
        req.context["authenticated_app"] = application
        req.context["authenticated_tenant"] = tenant
        return application.get("signing_secret")
    
    def get_site(self,db, host_name):
        return db.objects( Site.all() ).filter(host_name__eq=host_name).fetch_one()
    
    def get_authenticated_tenant(self,db, tenant_id):
        return db.objects( Tenant.get(tenant_id) ).fetch_one()

    def get_authenticated_app(self,db,application_id):
        return db.objects( Application.get(application_id ) ).fetch_one()


"""
class TenantResourceValidationMiddleWare:
    
    Called after 'CustomAuthMiddleWare '

    1. To validate that resource tenant is correct as required
    2. For SUPER tenants, check if they have enough access to the other Tenants (for super tenant paths)
    3. To set the correct resource tenant
    

    pass

"""


