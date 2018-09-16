

from falcon_rest.models import Base,HasTenantMixin

from sqlalchemy import Column, String, Boolean, ForeignKey


class Organization(HasTenantMixin,Base):
    name = Column(String(100), nullable = False,unique = True)
    




    