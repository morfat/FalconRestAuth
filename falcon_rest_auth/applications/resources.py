
import falcon

from .models import Application

from falcon_rest.resources import BaseResource

class ApplicationListResource(BaseResource):

    login_required = False

    queryset = Application.all()
    model = Application

    
    


    
   

        



