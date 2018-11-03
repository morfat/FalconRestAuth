

import serpy
from falchemy_rest.serializers import BaseSerializer

class TeamSerializer(BaseSerializer):

    organization_id = serpy.StrField()
    name =  serpy.StrField()
    

class TeamRoleSerializer(BaseSerializer):
    name =  serpy.StrField()


class TeamUserSerializer(BaseSerializer):
    first_name =  serpy.StrField()
    last_name =  serpy.StrField()
    email =  serpy.StrField()
    full_name = serpy.MethodField()

    def get_full_name(self, obj):
        return "%s %s"%( obj.get("first_name"), obj.get("last_name") )
