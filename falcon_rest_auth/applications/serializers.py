

import serpy
from falcon_rest.serializers import BaseSerializer

class ApplicationSerializer(BaseSerializer):

    name = serpy.StrField()
    is_multitenant = serpy.BoolField()
    
  



