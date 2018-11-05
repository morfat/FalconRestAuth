

import serpy
from falchemy_rest.serializers import BaseSerializer

class PermissionSerializer(BaseSerializer):
    code_name = serpy.StrField()
    display_name = serpy.StrField()
    content_type_id = serpy.StrField(required=False)
   
