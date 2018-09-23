
import json
import serpy
from falchemy_rest.serializers import BaseSerializer
from jwcrypto import jwk

   

class APISerializer(BaseSerializer):

    name = serpy.StrField()
    is_default = serpy.BoolField()
    uri = serpy.StrField()
    description =  serpy.StrField(required=False)
    token_lifetime = serpy.IntField(required=False)
    token_lifetime_web = serpy.IntField(required=False)
    signing_secret = serpy.MethodField()
    tenant_id = serpy.StrField()
    
    class Meta:
        read_protected_fields = ('signing_secret',)
        write_protected_fields = ('id','created_at','updated_at',)


    def get_signing_secret(self,obj):
        if obj.get("is_default") is False:

            key = jwk.JWK.generate(kty = 'oct',size = 256)
            return json.loads(key.export()).get("k")
        else:
            #this api will use application's secret key
            return None

        



