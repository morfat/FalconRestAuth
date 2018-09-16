
#create all db

from falcon_rest.models import Base

from falcon_rest_auth.settings import DB_ENGINE

from sqlalchemy.orm import sessionmaker



def init_db():
    from falcon_rest_auth.applications import models
    from falcon_rest_auth.tenants import models
    from falcon_rest_auth.organizations import models


    drop_all = input("Drop all tables ? Yes / No\t")
    if drop_all == 'yes':
        print ("Dropping Tables")
        Base.metadata.drop_all(DB_ENGINE)
    
    Base.metadata.create_all(DB_ENGINE)




init_db()


