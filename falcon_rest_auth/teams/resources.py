
import falcon

from .models import Team, TeamRole, TeamUser
from  ..roles.models import Role

from ..users.models import User
from .serializers import * 

from falchemy_rest.resources import ListCreateResource ,RetrieveUpdateResource, CreateResource, ListResource
from sqlalchemy import select


class ListCreateTeams(ListCreateResource):
    
    login_required = True
    model = Team
    serializer_class = TeamSerializer

class RetrieveUpdateTeam(RetrieveUpdateResource):
    #login_required = False

    model = Team

    serializer_class = TeamSerializer

class AddTeamRoles(CreateResource):
    """ To add roles to specific team """

    login_required = True
    model = TeamRole
   
    def on_post(self,req, resp, pk):
        db = self.get_db(req)
        posted_data = req.media
        print (posted_data)
        role_ids = posted_data.pop("role_ids",[])
        tenant_id = self.get_auth_tenant_id(req)

        for role in role_ids:
            #create
            data = {"team_id": pk, "role_id": role, "tenant_id": tenant_id }
            print (data)
            db.objects( self.model.insert() ).create(**data)

        resp.media = {}
        resp.status = falcon.HTTP_OK


class RemoveTeamRoles(CreateResource):
    """ To remove roles from specific team """

    login_required = True
    model = TeamRole
   
    def on_post(self,req, resp, pk):
        db = self.get_db(req)
        posted_data = req.media
        print (posted_data)
        role_ids = posted_data.pop("role_ids",[])
        tenant_id = self.get_auth_tenant_id(req)
        team_id = pk 

        for role_id in role_ids:
            #create
            db.objects( self.model.delete() ).filter(
                 tenant_id__eq=tenant_id, role_id__eq=role_id, team_id__eq=team_id
                ).delete()

        resp.media = {}
        resp.status =  falcon.HTTP_OK

class ListTeamRoles(ListResource):

    login_required = True
    model = TeamRole
    serializer_class = TeamRoleSerializer

    def on_get(self,req, resp, pk):
        db = self.get_db(req)
        query_params = req.params 

        results, pagination = self.list(req,resp,db, team_id = pk)

        serializer = self.get_serializer_class()(results, many = True)


        resp.media = {"data": serializer.valid_read_data, "pagination": pagination}

    def list(self,req,resp,db, team_id):

        query_params = req.params
        #custom query
        queryset = select( [ Role.id, Role.name ] ).select_from( 
            Role.__table__.join( TeamRole, TeamRole.role_id == Role.id )
             ).where( TeamRole.team_id == team_id )

        queryset_object = db.objects( queryset )

        #1.filter
        filtered_queryset_object = self.filter_queryset(queryset_object, filter_params = query_params)

        #2. paginate and get results

        results, pagination = self.paginator_class().paginate(
                                          url = req.uri,
                                          url_query_params = query_params,
                                          queryset_object = queryset_object
                                          )

        #3. read db/ execute

        #results = filtered_queryset_object.fetch()

        return results, pagination



class AddTeamMembers(CreateResource):
    """ To add Members to specific team """

    login_required = True
    model = TeamUser
   
    def on_post(self,req, resp, pk):
        db = self.get_db(req)
        posted_data = req.media
        print (posted_data)
        user_ids = posted_data.pop("user_ids",[])
        tenant_id = self.get_auth_tenant_id(req)

        for user_id in user_ids:
            #create
            data = {"team_id": pk, "user_id": user_id, "tenant_id": tenant_id }
            print (data)
            db.objects( self.model.insert() ).create(**data)

        resp.media = {}
        resp.status = falcon.HTTP_OK


class RemoveTeamMembers(CreateResource):
    """ To remove Members from specific team """

    login_required = True
    model = TeamUser
   
    def on_post(self,req, resp, pk):
        db = self.get_db(req)
        posted_data = req.media
        print (posted_data)
        user_ids = posted_data.pop("user_ids",[])
        tenant_id = self.get_auth_tenant_id(req)
        team_id = pk 

        for user_id in user_ids:
            #create
            db.objects( self.model.delete() ).filter(
                 tenant_id__eq=tenant_id, user_id__eq=user_id, team_id__eq=team_id
                ).delete()

        resp.media = {}
        resp.status =  falcon.HTTP_OK

class ListTeamMembers(ListResource):

    login_required = True
    model = TeamUser
    serializer_class = TeamUserSerializer

    def on_get(self,req, resp, pk):
        db = self.get_db(req)
        query_params = req.params 

        results, pagination = self.list(req,resp,db, team_id = pk)

        serializer = self.get_serializer_class()(results, many = True)


        resp.media = {"data": serializer.valid_read_data, "pagination": pagination}

    def list(self,req,resp,db, team_id):

        query_params = req.params
        #custom query
        queryset = select( [ User.id, User.first_name, User.last_name,User.email ] ).select_from( 
            User.__table__.join( TeamUser, TeamUser.user_id == User.id )
             ).where( TeamUser.team_id == team_id )

        queryset_object = db.objects( queryset )

        #1.filter
        filtered_queryset_object = self.filter_queryset(queryset_object, filter_params = query_params)

        #2. paginate and get results

        results, pagination = self.paginator_class().paginate(
                                          url = req.uri,
                                          url_query_params = query_params,
                                          queryset_object = queryset_object
                                          )

        #3. read db/ execute

        #results = filtered_queryset_object.fetch()

        return results, pagination
    