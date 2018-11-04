

from falchemy_rest.models import Base,HasTenantMixin
from sqlalchemy import Column, String, UniqueConstraint


class Site(HasTenantMixin,Base):
    host_name = Column(String(100), nullable=False, unique=True)




    