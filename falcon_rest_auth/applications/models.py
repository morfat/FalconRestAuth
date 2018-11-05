from falchemy_rest.models import Base

from sqlalchemy import Column, String, Boolean, ForeignKey , UniqueConstraint

from falchemy_rest.utils import generate_signing_secret

class Application(Base):
    name = Column(String(100), nullable = False,unique = True)
    description = Column(String(200), nullable = True)
    is_multitenant = Column(Boolean, default = True)
    signing_secret = Column(String(100), nullable = False, default = generate_signing_secret)
    auth_username_field =  Column(String(100), default = 'email', nullable = False)