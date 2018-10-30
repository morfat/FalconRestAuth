

from .resources import *

routes = [
    ('',ListCreateRoles() ),
    ('/{pk}', RetrieveUpdateRole() )
]

