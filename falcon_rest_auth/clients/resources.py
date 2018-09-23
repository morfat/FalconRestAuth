
import falcon

from .models import Client
from .serializers import ClientSerializer

from falchemy_rest.resources import ListCreateResource ,RetrieveUpdateResource

class ClientMixin:

    def get_client(self, client_id):
        if not client_id:
            raise falcon.HTTPBadRequest(title="Missing client_id Field", description="client_id field is needed")
        
        client =  db.objects( Client.get(client_id) ).fetch()[0]
        if not client:
            raise falcon.HTTPBadRequest(title="Invalid Client", description="Valid client_id is needed")
        
        return client



class ListCreateClients(ListCreateResource):

    login_required = False

  
    model = Client

    filterable_fields = ('tenant_id','organization_id',)
    searchable_fields = ('name',)

    serializer_class = ClientSerializer


class RetrieveUpdateClient(RetrieveUpdateResource):
    login_required = False

    model = Client

    serializer_class = ClientSerializer


    


    
   

        



