
import falcon

from .models import Application

from falcon_rest.resources import BaseResource

class ApplicationListResource(BaseResource):

    login_required = False

    queryset = Application.all()
    model = Application

    def on_get(self,req, resp):
        db = self.get_db(req)

        apps = db.objects( self.get_queryset() ).fetch()


        print (apps)


        resp.media = {}
    


    
   

        



