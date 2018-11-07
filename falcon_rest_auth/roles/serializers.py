

import serpy
from falchemy_rest.serializers import BaseSerializer

class RoleSerializer(BaseSerializer):

    organization_id = serpy.StrField()
    name =  serpy.StrField()

class RolePermissionSerializer(BaseSerializer):
    content_type_display_name = serpy.StrField()
    content_type_code_name = serpy.StrField()
    display_name = serpy.StrField()
    code_name = serpy.StrField()
    direction = serpy.StrField()
    label = serpy.MethodField()

    def get_label(self, obj):
        return "{0} {1}".format( obj.get("display_name") ,obj.get("content_type_display_name") )
        
