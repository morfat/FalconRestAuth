
import falcon

from .models import Organization
from .serializers import OrganizationSerializer

from falchemy_rest.resources import ListCreateResource ,RetrieveUpdateResource , ListResource

class ListCreateOrganizations(ListResource):

    #login_required = False

    model = Organization

    #filterable_fields = ()
    searchable_fields = ('name',)

    serializer_class = OrganizationSerializer


class RetrieveUpdateOrganization(RetrieveUpdateResource):
    #login_required = False

    model = Organization

    serializer_class = OrganizationSerializer


    


    
   

        



