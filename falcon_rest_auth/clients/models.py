

from falchemy_rest.models import Base,HasTenantMixin ,utc_pk

from sqlalchemy import Column, String, Boolean, ForeignKey

                       
class Client(HasTenantMixin,Base):
    name = Column(String(100), nullable = False,unique = True)
    is_first_party = Column(Boolean, default = False)
    organization_id = Column(String(50), ForeignKey('organizations.id'))
    description = Column(String(150), nullable = True)
    client_id = Column(String(50), nullable = False,  unique = True, default = utc_pk)
    client_secret = Column(String(100), nullable = True)
    web_origins = Column(String(100), nullable = True)
    auth_call_back_urls = Column(String(100), nullable = True)
    is_active = Column(Boolean, default = True)
    client_type = Column(String(100)) 







    