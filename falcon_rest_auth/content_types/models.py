
from falchemy_rest.models import Base

from sqlalchemy import Column, String, Boolean, ForeignKey , UniqueConstraint

                       
class ContentType(Base):

    display_name = Column(String(100), nullable = False)
    code_name = Column(String(100), nullable = False)
    application_id = Column(String(50), ForeignKey('applications.id') , nullable = False)

    __table_args__ =  ( UniqueConstraint('application_id', 'code_name', name='_application_content'),
                       )



    