

from .resources import *

routes = [
    ('',ListCreateTeams() ),
    ('/{pk}', RetrieveUpdateTeam() )
]

