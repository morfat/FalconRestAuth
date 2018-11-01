

from falchemy_rest.models import Base,HasTenantMixin

from sqlalchemy import Column, String, Boolean, ForeignKey , UniqueConstraint



class Team(HasTenantMixin,Base):
    name = Column(String(100), nullable = False)
    organization_id =  Column(String(50),ForeignKey('organizations.id') , nullable = False)
   
    __table_args__ =  ( UniqueConstraint('organization_id', 'name', name='_organization_name'),
                       )
    

class TeamRoles(HasTenantMixin,Base):
    role_id =  Column(String(50),ForeignKey('roles.id') , nullable = False)
    team_id =  Column(String(50),ForeignKey('teams.id') , nullable = False)

    __table_args__ =  ( UniqueConstraint('role_id', 'team_id', name='_team_role'),
                       )








    