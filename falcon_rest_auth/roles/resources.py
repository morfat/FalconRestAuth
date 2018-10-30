
import falcon

from .models import Role
from .serializers import RoleSerializer 

from falchemy_rest.resources import ListCreateResource ,RetrieveUpdateResource,CreateResource



class ListCreateRoles(ListCreateResource):
    
    login_required = True
    model = Role
    serializer_class = RoleSerializer

class RetrieveUpdateRole(RetrieveUpdateResource):
    #login_required = False

    model = Role

    serializer_class = RoleSerializer


    