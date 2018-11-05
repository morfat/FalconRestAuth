
from falchemy_rest.models import Base

from sqlalchemy import Column, String, ForeignKey , UniqueConstraint

class Permission(Base):
    display_name = Column(String(100), nullable = False)
    code_name = Column(String(100), nullable = False)
    content_type_id =  Column(String(50),ForeignKey('content_types.id') , nullable = False)

    __table_args__ =  ( UniqueConstraint('content_type_id', 'code_name', name='_content_permission'),
                       )