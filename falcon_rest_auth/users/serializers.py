

import serpy
from falchemy_rest.serializers import BaseSerializer

class UserSerializer(BaseSerializer):

    tenant_id = serpy.StrField(required=False) 
    organization_id = serpy.StrField(required=False) #when given , we assume we are adding another organization member.
    is_organization_admin = serpy.StrField(required=False)

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
        write_protected_fields = ()



class UserRegisterSerializer(BaseSerializer):
    client_id = serpy.StrField(required=False)
    organization_name = serpy.StrField(required=False) #needed for  for B2B tenant business mode type.

    email =  serpy.StrField(required = False)
    phone_number =  serpy.StrField(required = False)

    first_name =  serpy.StrField(required = False)
    last_name =  serpy.StrField(required = False) 
 
    class Meta:

        read_protected_fields = ('password',)
        write_protected_fields = ()





class LoginUserSerializer(BaseSerializer):
    """ for use in getting access token"""

    client_id = serpy.StrField()
    email =  serpy.StrField(required = False)
    phone_number =  serpy.StrField(required = False)
    password = serpy.StrField()
    #audience = serpy.StrField() #the tenat full uri that expects this token



    
