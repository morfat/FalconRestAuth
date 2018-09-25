

import serpy
from falchemy_rest.serializers import BaseSerializer
import json

class DictField(serpy.Field):
    def to_value(self,value):
        try:
            return json.loads(value)
        except TypeError:
            return json.dumps(value)



class EmailProviderSerializer(BaseSerializer):
    name = serpy.StrField()
    activated = serpy.BoolField()
    default_from_address = serpy.StrField()
    credentials = DictField()
    




class EmailTemplateSerializer(BaseSerializer):
    name = serpy.StrField()
   


    
    
  



