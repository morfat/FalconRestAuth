

from falchemy_rest.models import Base

from sqlalchemy import Column, String, Boolean


class Application(Base):
    name = Column(String(100), nullable = False,unique = True)
    is_multitenant = Column(Boolean, default = True)



    