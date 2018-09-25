

from .resources import *

routes = [
    ('/providers',ListCreateEmailProviders() ),
    ('/providers/{pk}',RetrieveUpdateEmailProvider() ),
    ('/templates',ListCreateEmailTemplates() ),
    ('/templates/{pk}',RetrieveUpdateEmailTemplate() ),


]

