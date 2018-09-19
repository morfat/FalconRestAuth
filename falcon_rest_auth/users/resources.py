
import falcon

from .models import User
from .serializers import UserSerializer

from falchemy_rest.resources import ListCreateResource ,RetrieveUpdateResource

class ListCreateUsers(ListCreateResource):

    login_required = False

    model = User

    filterable_fields = ('tenant_id',)
    searchable_fields = ('name',)

    serializer_class = UserSerializer

    def perform_create(self,req,db,posted_data):

        created = db.objects( self.model.insert() ).create(**posted_data)

        return created
        



class RetrieveUpdateUser(RetrieveUpdateResource):
    login_required = False

    model = User

    serializer_class = UserSerializer


    


    
   

        



