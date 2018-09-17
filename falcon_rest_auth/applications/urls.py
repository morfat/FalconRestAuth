

from .resources import *

routes = [
    ('',ListApplications() ),
    ('/{pk}',RetrieveApplication() ),

]

