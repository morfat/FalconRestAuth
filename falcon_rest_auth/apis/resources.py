
import falcon

from .models import API
from .serializers import APISerializer

from falchemy_rest.resources import ListCreateResource ,RetrieveUpdateResource

class ListCreateAPIs(ListCreateResource):

    login_required = False

  
    model = API

    filterable_fields = ('tenant_id',)
    searchable_fields = ('name',)

    serializer_class = APISerializer


class RetrieveUpdateAPI(RetrieveUpdateResource):
    login_required = False

    model = API

    serializer_class = APISerializer


    


    
   

        



