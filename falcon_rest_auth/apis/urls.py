

from .resources import *

routes = [
    ('',ListCreateAPIs() ),
    ('/{pk}',RetrieveUpdateAPI() ),

]

