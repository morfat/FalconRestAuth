
import falcon

from .models import Application
from .serializers import ApplicationSerializer

from falchemy_rest.resources import BaseResource, ListResource, RetrieveResource,DestroyResource,CreateResource, UpdateResource

class ListApplications(ListResource,CreateResource):

    login_required = False

  
    model = Application

    filterable_fields = ('name','is_multitenant',)
    searchable_fields = ('name',)

    serializer_class = ApplicationSerializer


class RetrieveApplication(RetrieveResource,DestroyResource,UpdateResource):
    login_required = False

    model = Application

    serializer_class = ApplicationSerializer


    


    
   

        



