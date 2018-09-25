

from falchemy_rest.models import Base,HasTenantMixin 

from sqlalchemy import Column, String, Boolean, Text,UniqueConstraint


                       
class EmailProvider(HasTenantMixin,Base):
    name = Column(String(100), nullable = False) #e.g gmail , sendgrid
    activated = Column(Boolean, default = False)
    default_from_address = Column(String(100), nullable = False)
    credentials = Column(Text, nullable = False)
    settings =  Column(Text, nullable = True)

    __table_args__ =  ( UniqueConstraint('tenant_id', 'name', name='_unique_emailprovider_per_tenant'),
                       )




       
class EmailTemplate(HasTenantMixin,Base):
    TEMPLATE_PASSWORD_RESET = 'password_reset'
    TEMPLATE_PASSWORD_CHANGED = 'password_changed'
    TEMPLATE_ACCOUNT_CREATED = 'account_created'
    
    name = Column(String(100), nullable = False) #e.g password_reset,password_change
    body = Column(Text, nullable = False)
    activated = Column(Boolean, default = False)
    subject = Column(String(100), nullable = False)
    
    __table_args__ =  ( UniqueConstraint('tenant_id', 'name', name='_unique_emailtemplate_per_tenant'),
                       )






    