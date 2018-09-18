
import falcon

from .models import Client
from .serializers import ClientSerializer

from falchemy_rest.resources import ListCreateResource ,RetrieveUpdateResource

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


    


    
   

        



