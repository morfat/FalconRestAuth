
import falcon

from .models import Tenant
from .serializers import TenantSerializer

from falchemy_rest.resources import ListCreateResource ,RetrieveUpdateResource





class ListCreateTenants(ListCreateResource):

    login_required = False

  
    model = Tenant

    filterable_fields = ('application_id',)
    searchable_fields = ('name',)

    serializer_class = TenantSerializer


class RetrieveUpdateTenant(RetrieveUpdateResource):
    login_required = False

    model = Tenant

    serializer_class = TenantSerializer


    


    
   

        



