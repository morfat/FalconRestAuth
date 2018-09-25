

from falchemy_rest.models import Base,HasTenantMixin 

from sqlalchemy import Column, String, Boolean, Text,UniqueConstraint


                       
class EmailProvider(HasTenantMixin,Base):
    PROVIDER_SENDGRID = 'sendgrid'
    PROVIDER_GMAIL = 'gmail',
    PROVIDER_SENDINBLUE = 'sendinblue'

    name = Column(String(100), nullable = False) #e.g gmail , sendgrid
    activated = Column(Boolean, default = False)
    default_from_address = Column(String(100), nullable = False)
    credentials = Column(Text, nullable = False)
    settings =  Column(Text, nullable = True) #e.g 


    __table_args__ =  ( UniqueConstraint('tenant_id', 'name', name='_unique_emailprovider_per_tenant'),
                       )
    
    @classmethod
    def gmail(cls):
        return cls.all().where(cls.name==cls.PROVIDER_GMAIL)




class EmailTemplate(HasTenantMixin,Base):
    TEMPLATE_PASSWORD_RESET = 'password_reset'
    TEMPLATE_PASSWORD_CHANGED = 'password_changed'
    TEMPLATE_ACCOUNT_CREATED = 'account_created'
    
    name = Column(String(100), nullable = False) #e.g password_reset,password_change
    body = Column(Text, nullable = True)
    activated = Column(Boolean, default = False)
    subject = Column(String(100), nullable = True)
    
    __table_args__ =  ( UniqueConstraint('tenant_id', 'name', name='_unique_emailtemplate_per_tenant'),
                       )
    
    @classmethod
    def account_created(cls):
        return cls.all().where(cls.name==cls.TEMPLATE_ACCOUNT_CREATED)
    
    @classmethod
    def password_reset(cls):
        return cls.all().where(cls.name==cls.TEMPLATE_PASSWORD_RESET)
    

    @classmethod
    def password_changed(cls):
        return cls.all().where(cls.name==cls.TEMPLATE_PASSWORD_CHANGED)
    
    








    