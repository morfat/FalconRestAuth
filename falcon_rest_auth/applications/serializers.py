

import serpy

class ApplicationSerializer(serpy.DictSerializer):
    name = serpy.StrField()
    is_multitenant = serpy.BoolField()
    
    write_protected_fields = ['id','deleted']
    



