
import falcon

from .models import Application
from .serializers import ApplicationSerializer

from falchemy_rest.resources import ListCreateResource ,RetrieveUpdateResource

class ListCreateApplications(ListCreateResource):

    login_required = False

  
    model = Application

    filterable_fields = ('name','is_multitenant',)
    searchable_fields = ('name',)

    serializer_class = ApplicationSerializer


class RetrieveUpdateApplication(RetrieveUpdateResource):
    login_required = False

    model = Application

    serializer_class = ApplicationSerializer


    


    
   

        



