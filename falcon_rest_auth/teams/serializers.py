

import serpy
from falchemy_rest.serializers import BaseSerializer

class TeamSerializer(BaseSerializer):

    organization_id = serpy.StrField()
    name =  serpy.StrField()
    

