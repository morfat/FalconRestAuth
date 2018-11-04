

from falchemy_rest.models import Base,HasTenantMixin
from sqlalchemy import Column, String, UniqueConstraint


class Site(HasTenantMixin,Base):
    domain_name = Column(String(100), nullable = False)
    
    __table_args__ =  ( UniqueConstraint('tenant_id', 'domain_name', name='_unique_tenant_domain_name'),
                      )





    