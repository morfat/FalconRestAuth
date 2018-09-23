

from falchemy_rest import middlewares

from ..tenants.models import Tenant
from ..applications.models import Application


class CustomAuthMiddleWare(middlewares.AuthMiddleWare):
    def __init__(self):
        pass

    def get_secret_key(self,req):
        host_name = req.forwarded_host

        db = req.context['db'] 

        
        tenant = db.objects( Tenant.get(host_name=host_name)).fetch()[0]
        application = db.objects( Application.get(tenant.get("application_id") ) ).fetch()[0]
      
        key = application.get("signing_secret")

        print (key)

        return key

    

