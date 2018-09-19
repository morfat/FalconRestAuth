

import serpy
from falchemy_rest.serializers import BaseSerializer

class UserSerializer(BaseSerializer):
  
    tenant_id = serpy.StrField(required=False) 
    organization_id = serpy.StrField(required=False) #wwhen given , we assume we are adding another organization member.
    organization_name = serpy.StrField(required=False) #only required for new registrations for B2B app type.


    email =  serpy.StrField(required = False)
    phone_number =  serpy.StrField(required = False)

    first_name =  serpy.StrField(required = False)
    last_name =  serpy.StrField(required = False) 

    email_is_confirmed =  serpy.BoolField(required = False) 
    phone_number_is_confirmed =  serpy.BoolField(required = False) 
    is_active =  serpy.BoolField(required = False) 
    is_staff =  serpy.BoolField(required = False) 
    is_super_user =  serpy.BoolField(required = False) 

  
    class Meta:
        read_protected_fields = ('password',)


