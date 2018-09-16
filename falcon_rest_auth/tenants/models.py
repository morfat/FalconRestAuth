

from falcon_rest.models import Base
from sqlalchemy import Column, String, Boolean, ForeignKey


class Tenant(Base):
    name = Column(String(100), nullable = False,unique = True)
    is_super_tenant = Column(Boolean, default = False)
    application_id = Column(String(50), ForeignKey('applications.id'))
    domain_name = Column(String(50),unique = True, nullable = False)
    business_mode = Column(String(10)) #B2B or B2C






    