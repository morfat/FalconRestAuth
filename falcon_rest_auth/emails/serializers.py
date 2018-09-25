

import serpy
from falchemy_rest.serializers import BaseSerializer , DictField
import json




class EmailProviderSerializer(BaseSerializer):
    name = serpy.StrField()
    activated = serpy.BoolField()
    default_from_address = serpy.StrField()
    credentials = DictField()
    




class EmailTemplateSerializer(BaseSerializer):
    name = serpy.StrField()
   


    
    
  



