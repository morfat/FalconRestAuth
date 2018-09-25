
#create all db

from falchemy_rest.models import Base

from falcon_rest_auth.settings import DB_ENGINE



def init_db():
    from falcon_rest_auth.applications import models
    from falcon_rest_auth.tenants import models
    from falcon_rest_auth.organizations import models
    from falcon_rest_auth.clients import models
    from falcon_rest_auth.users import models
    from falcon_rest_auth.apis import models
    from falcon_rest_auth.emails import models

    drop_all = input("Drop all tables ? Yes / No\t")
    if drop_all == 'yes':
        print ("Dropping Tables")
        Base.metadata.drop_all(DB_ENGINE)
    
   
    Base.metadata.create_all(DB_ENGINE)




init_db()


