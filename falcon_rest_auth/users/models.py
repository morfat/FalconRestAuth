

from falchemy_rest.models import Base,HasTenantMixin

from sqlalchemy import Column, String, Boolean, ForeignKey , UniqueConstraint


from argon2 import PasswordHasher as ph
import argon2 
import random


class User(HasTenantMixin,Base):

    email = Column(String(100), nullable = True)
    phone_number = Column(String(12), nullable = True)
    email_is_confirmed = Column(Boolean,default = False)
    phone_number_is_confirmed = Column(Boolean,default = False)
    password = Column( String(100), nullable = False)
    is_active = Column(Boolean,default = True)
    is_staff = Column(Boolean,default = False)
    is_super_user = Column(Boolean,default = False)
    first_name = Column(String(100), nullable = True)
    last_name = Column(String(100), nullable = True)


    __table_args__ =  ( UniqueConstraint('tenant_id', 'email', name='_unique_email_per_tenant'),
                        UniqueConstraint('tenant_id', 'phone_number', name='_unique_phone_number_per_tenant')
                       )
    
   
    @classmethod
    def is_valid_password(self,hashed,raw_password):
        try:
            return ph().verify(hashed,raw_password)
        except argon2.exceptions.VerifyMismatchError:
            return False

    @classmethod
    def hashed_password(self,raw_password):
        return ph().hash(raw_password)

    @classmethod
    def get_random_password(self):
        return str( random.randint(100000,999999) )

    @classmethod
    def set_password(cls, db,user_id,password):
        password = cls.hashed_password(password)
        return db.objects( cls.update() ).filter(id__eq = user_id).update(**{"password": password})



    


class OrganizationUser(Base):
    user_id = Column(String(50), ForeignKey('users.id') ,nullable = False )
    organization_id =  Column(String(50),ForeignKey('organizations.id') , nullable = False)
    is_admin = Column(Boolean,default = False)

    __table_args__ = ( UniqueConstraint('user_id', 'organization_id', name='_unique_organization_user'),
                     )



    