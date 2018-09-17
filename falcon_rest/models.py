from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.declarative import has_inherited_table

from sqlalchemy import Column, Integer, String, Boolean,DateTime,ForeignKey
import uuid

import datetime

def utc_now():
    return datetime.datetime.utcnow()

def utc_timestamp():
    t = utc_now().timestamp()
    return str(t).split('.')[0]

def hex_uuid():
    return uuid.uuid4().hex

def utc_pk():
    return utc_timestamp() + hex_uuid()



class CRUDMixin:
    #Column('deleted',Boolean,default = False)

    def add(self):
        table = self.__table__
        print (table.insert())
        print ("Checking self")
        print (table.select(), self.connection)
    
    @classmethod
    def all(cls):
        return cls.__table__.select()
    
    @classmethod
    def insert(cls):
        return cls.__table__.insert()

    @classmethod
    def delete(cls):
        return cls.__table__.delete()
        

        
    


class TimestampMixin:
    created_at = Column(DateTime,nullable = False,default = utc_now)
    updated_at = Column(DateTime,nullable = False,default = utc_now,onupdate = utc_now)
    

class BaseTable(CRUDMixin,TimestampMixin):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'
        
    id = Column(String(50), primary_key = True, default = utc_pk )




class HasTenantMixin:

    @declared_attr
    def tenant_id(cls):
        return Column(String(50), ForeignKey('tenants.id'))


Base = declarative_base(cls = BaseTable)
 









