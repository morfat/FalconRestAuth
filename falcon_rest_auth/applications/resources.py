
import falcon

from .models import Application
from .serializers import ApplicationSerializer

from falcon_rest.resources import BaseResource, ListResource

class ListApplications(ListResource):

    login_required = False

    #queryset = Application.all()
    model = Application

    filterable_fields = ('name','is_multitenant',)
    searchable_fields = ('name',)

    serializer_class = ApplicationSerializer


    
    


    
   

        



