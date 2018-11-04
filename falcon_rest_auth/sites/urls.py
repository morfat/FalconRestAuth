

from .resources import *

routes = [
    ('',ListCreateSites() ),
    ('/{pk}',RetrieveUpdateSite() ),

]

