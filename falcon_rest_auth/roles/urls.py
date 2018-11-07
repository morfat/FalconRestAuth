

from .resources import *

routes = [
    ('',ListCreateRoles() ),
    ('/{pk}', RetrieveUpdateRole() ),
    ('/{pk}/permissions', ListRolePermissions() )
]

