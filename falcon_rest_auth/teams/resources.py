
import falcon

from .models import Team
from .serializers import TeamSerializer 

from falchemy_rest.resources import ListCreateResource ,RetrieveUpdateResource



class ListCreateTeams(ListCreateResource):
    
    login_required = True
    model = Team
    serializer_class = TeamSerializer

class RetrieveUpdateTeam(RetrieveUpdateResource):
    #login_required = False

    model = Team

    serializer_class = TeamSerializer


    