

from .resources import *

routes = [
    ('',ListCreateUsers() ),
    ('/{pk}',RetrieveUpdateUser() ),

]

