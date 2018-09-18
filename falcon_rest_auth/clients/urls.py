

from .resources import *

routes = [
    ('',ListCreateClients() ),
    ('/{pk}',RetrieveUpdateClient() ),

]

