

from .models import Permission
from .serializers import PermissionSerializer

from falchemy_rest.resources import ListCreateResource ,RetrieveUpdateResource


class ListCreatePermissions(ListCreateResource):

    login_required = True

    multitenant = False
  
    model = Permission

    serializer_class = PermissionSerializer
    filterable_fields = ('content_type_id',)


class RetrieveUpdatePermission(RetrieveUpdateResource):
    login_required = True
    multitenant = False

    model = Permission

    serializer_class = PermissionSerializer


    


    
   

        



