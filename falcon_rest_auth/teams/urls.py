

from .resources import *

routes = [
    ('',ListCreateTeams() ),
    ('/{pk}', RetrieveUpdateTeam() ),
    ('/{pk}/roles',ListTeamRoles() ),
    ('/{pk}/roles/add',AddTeamRoles() ),
    ('/{pk}/roles/remove',RemoveTeamRoles() ),
    ('/{pk}/members',ListTeamMembers() ),
    ('/{pk}/members/add',AddTeamMembers() ),
    ('/{pk}/members/remove',RemoveTeamMembers() )
]

