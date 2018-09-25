

from .resources import *

routes = [
    ('/providers',ListCreateEmailProviders() ),
    ('/providers/{pk}',RetrieveUpdateEmailProvider() ),

]

