
import falcon

from .models import Application
from .serializers import ApplicationSerializer

from falcon_rest.resources import BaseResource, ListResource, RetrieveResource,DestroyResource,CreateResource

class ListApplications(ListResource,CreateResource):

    login_required = False

    #queryset = Application.all()
    model = Application

    filterable_fields = ('name','is_multitenant',)
    searchable_fields = ('name',)

    serializer_class = ApplicationSerializer


class RetrieveApplication(RetrieveResource,DestroyResource):
    login_required = False
    #queryset = Application.all()
    
    model = Application

    serializer_class = ApplicationSerializer


    


    
   

        



