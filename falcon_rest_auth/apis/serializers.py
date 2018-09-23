
import json
import serpy
from falchemy_rest.serializers import BaseSerializer
from jwcrypto import jwk

   

class APISerializer(BaseSerializer):

    name = serpy.StrField()
    is_default = serpy.BoolField( required=False)
    uri = serpy.StrField()
    description =  serpy.StrField(required=False)
    token_lifetime = serpy.IntField(required=False)
    token_lifetime_web = serpy.IntField(required=False)
    signing_secret = serpy.MethodField()
    create_secret_key = serpy.BoolField( )
    tenant_id = serpy.StrField()
    
    class Meta:
        read_protected_fields = ('signing_secret',)
        write_protected_fields = ('id','created_at','updated_at','create_secret_key',)


    def get_signing_secret(self,obj):
        create_secret_key = obj.get("create_secret_key")
        if create_secret_key and create_secret_key is True:
            key = jwk.JWK.generate(kty = 'oct',size = 256)
            return json.loads(key.export()).get("k")
        else:
            #this api will use application's secret key
            return None

        



