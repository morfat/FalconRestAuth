

from .resources import *

routes = [
    ('',ListCreateApplications() ),
    ('/{pk}',RetrieveUpdateApplication() ),
    ('/content-types',ListCreateApplicationContentType() ),


]

