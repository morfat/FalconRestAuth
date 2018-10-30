

import serpy
from falchemy_rest.serializers import BaseSerializer

class RoleSerializer(BaseSerializer):

    organization_id = serpy.StrField()
    name =  serpy.StrField()
    

