

from falchemy_rest.models import Base,HasTenantMixin ,utc_pk

from sqlalchemy import Column, String, Boolean, ForeignKey, Integer

                       
class API(HasTenantMixin,Base):
    name = Column(String(100), nullable = False,unique = True)
    uri = Column(String(200), nullable = False)
    description = Column(String(150), nullable = True)
    token_lifetime = Column(Integer, nullable = False, default = 3600)
    token_lifetime_web = Column(Integer, nullable = False, default = 1800)
    signing_secret = Column(String(100), nullable = True) #if not given, use the app secret
    is_default = Column(Boolean, default = False)

  







    