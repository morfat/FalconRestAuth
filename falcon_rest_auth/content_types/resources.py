
import falcon

from .models import ContentType
from .serializers import ContentTypeSerializer

from falchemy_rest.resources import ListCreateResource ,RetrieveUpdateResource


class ListCreateContentTypes(ListCreateResource):

    login_required = True
    multitenant = False
  
    model = ContentType

    serializer_class = ContentTypeSerializer

    def perform_create(self,req,db,posted_data):

        application = self.get_authenticated_application(req)
        posted_data.update({"application_id": application.get("id")})

        return db.objects( self.model.insert() ).create(**posted_data)



class RetrieveUpdateContentType(RetrieveUpdateResource):
    login_required = True
    multitenant = False

    model = ContentType

    serializer_class = ContentTypeSerializer




    
   

        



