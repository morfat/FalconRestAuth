

from .resources import *

routes = [
    ('',ListCreateContentTypes() ),
    ('/{pk}',RetrieveUpdateContentType() ),

]

