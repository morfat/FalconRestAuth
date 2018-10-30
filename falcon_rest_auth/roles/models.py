

from falchemy_rest.models import Base,HasTenantMixin

from sqlalchemy import Column, String, Boolean, ForeignKey , UniqueConstraint



class Role(HasTenantMixin,Base):
    name = Column(String(100), nullable = False)
    organization_id =  Column(String(50),ForeignKey('organizations.id') , nullable = False)
   
    __table_args__ =  ( UniqueConstraint('organization_id', 'name', name='_organization_name'),
                       )
    

class RolePermission(HasTenantMixin,Base):
    role_id =  Column(String(50),ForeignKey('roles.id') , nullable = False)
    permission_id =  Column(String(50),ForeignKey('permissions.id') , nullable = False)

    __table_args__ =  ( UniqueConstraint('role_id', 'permission_id', name='_role_permission'),
                       )








    