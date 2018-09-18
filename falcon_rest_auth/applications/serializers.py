

import serpy
from falchemy_rest.serializers import BaseSerializer

class ApplicationSerializer(BaseSerializer):

    name = serpy.StrField()
    is_multitenant = serpy.BoolField()
    
  



