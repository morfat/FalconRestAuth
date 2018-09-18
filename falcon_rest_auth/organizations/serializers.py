

import serpy
from falchemy_rest.serializers import BaseSerializer

class OrganizationSerializer(BaseSerializer):
    name = serpy.StrField()
    tenant_id = serpy.StrField()
   


    
    
  



