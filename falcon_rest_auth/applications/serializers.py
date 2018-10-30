

import serpy
from falchemy_rest.serializers import BaseSerializer
from jwcrypto import jwk
import json

class ApplicationSerializer(BaseSerializer):

    name = serpy.StrField()
    is_multitenant = serpy.BoolField()
    signing_secret = serpy.MethodField()

    class Meta:
        read_protected_fields = ('signing_secret',)
        write_protected_fields = ('id','created_at','updated_at',)


    def get_signing_secret(self,obj):
        key = jwk.JWK.generate(kty = 'oct',size = 256)
        return json.loads(key.export()).get("k")
     

    
    

class ContentTypeSerializer(BaseSerializer):
    name = serpy.StrField()
    code = serpy.StrField()
    application_id = serpy.StrField()
    



