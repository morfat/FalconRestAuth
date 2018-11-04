

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
        print (host_name)


        db = req.context['db'] 

        site =  db.objects( Site.all() ).filter(host_name__eq=host_name).fetch_one()
        if not site:
            raise falcon.HTTPForbidden(description=" Requests from this site not configured. ")

        tenant = db.objects( Tenant.get(site.get("tenant_id")) ).fetch_one()
        application = db.objects( Application.get(tenant.get("application_id") ) ).fetch()[0]
      
        key = application.get("signing_secret")

        # print (key)

        return key

    

