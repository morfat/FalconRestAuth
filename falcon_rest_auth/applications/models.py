

from falchemy_rest.models import Base

from sqlalchemy import Column, String, Boolean


class Application(Base):
    name = Column(String(100), nullable = False,unique = True)
    description = Column(String(200), nullable = True)
    is_multitenant = Column(Boolean, default = True)
    signing_secret = Column(String(100), nullable = True)



    