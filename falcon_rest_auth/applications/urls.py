

from .resources import *

routes = [
    ('',ListCreateApplications() ),
    ('/{pk}',RetrieveUpdateApplication() ),

]

