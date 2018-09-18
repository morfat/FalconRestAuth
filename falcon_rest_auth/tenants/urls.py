

from .resources import *

routes = [
    ('',ListCreateTenants() ),
    ('/{pk}',RetrieveUpdateTenant() ),

]

