
import falcon

from .models import ContentType
from .serializers import ContentTypeSerializer

from falchemy_rest.resources import ListCreateResource ,RetrieveUpdateResource

class ContentTypeMixin:

    def get_client(self, client_id):
        if not client_id:
            raise falcon.HTTPBadRequest(title="Missing client_id Field", description="client_id field is needed")
        
        client =  db.objects( ContentType.get(client_id) ).fetch()[0]
        if not client:
            raise falcon.HTTPBadRequest(title="Invalid ContentType", description="Valid client_id is needed")
        
        return client



class ListCreateContentTypes(ListCreateResource):

    login_required = True
  
    model = ContentType

    filterable_fields = ('organization_id',)
    searchable_fields = ('name',)

    serializer_class = ContentTypeSerializer


class RetrieveUpdateContentType(RetrieveUpdateResource):
    login_required = True

    model = ContentType

    serializer_class = ContentTypeSerializer


    


    
   

        



