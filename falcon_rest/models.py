from sqlalchemy.ext.declarative import declarative_base, declared_attr

from sqlalchemy import Column, Integer


class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'
        
    id = Column(Integer, primary_key = True)


Base = declarative_base(cls = BaseModel)

