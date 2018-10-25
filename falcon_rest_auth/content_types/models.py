

from falchemy_rest.models import Base

from sqlalchemy import Column, String, ForeignKey

                       
class ContentType(Base):
    display_name = Column(String(100), nullable = False,unique = True)
    code_name = Column(String(100), nullable = False,unique = True)
    application_id = Column(String(50), ForeignKey('applications.id') , nullable = False)








    