

import serpy
from falchemy_rest.serializers import BaseSerializer , DictField




class EmailProviderSerializer(BaseSerializer):
    name = serpy.StrField()
    activated = serpy.BoolField()
    default_from_address = serpy.StrField()
    credentials = DictField()
    




class EmailTemplateSerializer(BaseSerializer):
    name = serpy.StrField()
    activated = serpy.BoolField()
    body = serpy.StrField(required=False)
    subject = serpy.StrField(required=False)
    


    
    
  



