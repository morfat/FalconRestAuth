
import json
import serpy
from falchemy_rest.serializers import BaseSerializer
from jwcrypto import jwk

class ClientSerializer(BaseSerializer):

    
    
    name = serpy.StrField()
    is_first_party = serpy.BoolField()
    client_type = serpy.StrField()
    auth_call_back_urls = serpy.StrField(required=False)
    web_origins =  serpy.StrField(required=False)
    client_secret = serpy.MethodField()
    client_id = serpy.StrField(required=False)
    description =  serpy.StrField(required=False)
    organization_id = serpy.StrField()
    tenant_id = serpy.StrField()
    

    class Meta:
        read_protected_fields = ('client_secret',)
        write_protected_fields = ('client_id','id','created_at','updated_at',)


    def get_client_secret(self,obj):
        client_type = obj.get("client_type")
        if client_type == 'spa':
            return None

        key = jwk.JWK.generate(kty = 'oct',size = 256)
        return json.loads(key.export()).get("k")
        



