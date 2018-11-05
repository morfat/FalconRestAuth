
import json
import serpy
from falchemy_rest.serializers import BaseSerializer

class ContentTypeSerializer(BaseSerializer):
    code_name = serpy.StrField()
    display_name = serpy.StrField()
    application_id = serpy.StrField(required=False)
   
