

from .resources import *

routes = [
    ('',ListCreatePermissions() ),
    ('/{pk}',RetrieveUpdatePermission() ),

]

