

import serpy
from falchemy_rest.serializers import BaseSerializer

class TenantSerializer(BaseSerializer):
    
    name = serpy.StrField()
    is_super_tenant = serpy.BoolField()
    application_id = serpy.StrField()
    domain_name = serpy.StrField()
    business_mode = serpy.StrField()  #B2B or B2C


    
    
  



