
import falcon

from .models import Role, RolePermission
from .serializers import RoleSerializer  , RolePermissionSerializer
from ..permissions.serializers import PermissionSerializer
from ..permissions.models import Permission
from ..content_types.models import ContentType

from falchemy_rest.resources import ListCreateResource ,RetrieveUpdateResource,CreateResource, ListResource, UpdateResource

from sqlalchemy import select

class ListCreateRoles(ListCreateResource):
    
    login_required = True
    model = Role
    serializer_class = RoleSerializer

class RetrieveUpdateRole(RetrieveUpdateResource):
    #login_required = False

    model = Role

    serializer_class = RoleSerializer



class ListRolePermissions(ListResource, UpdateResource):

    login_required = True
    model = RolePermission
    serializer_class = RolePermissionSerializer

    def on_patch(self,req, resp,pk):
        """ Adds or removes permissions to a role """
        print ( req.media)
        db = self.get_db(req)
        request_data = req.media
        direction = request_data.pop("to")
        permissions = request_data.get("list")

        if direction == 'left':
            #assign permissions
            for p in permissions:
                permission_id = p.get("id")
                db.objects( self.model.delete() ).filter( permission_id__eq=permission_id, role_id__eq=pk).delete()

        else:
            #remove permissions. direction is right
            for p in permissions:
                data = { "tenant_id": self.get_auth_tenant_id(req), "permission_id": p.get("id"), "role_id": pk }
                db.objects( self.model.insert() ).create(**data)

        resp.status =  falcon.HTTP_OK


    def on_get(self,req, resp, pk):
        db = self.get_db(req)
        query_params = req.params 

        results = self.list(req,resp,db, role_id = pk)

        serializer = self.get_serializer_class()(results, many = True)


        resp.media = {"data": serializer.valid_read_data}
    
    def get_queryset(self, role_id):
        #custom query
        return select( [ Permission.id, Permission.display_name, Permission.code_name,
            Permission.content_type_id ] 
            ).select_from( Permission.__table__.join(
                RolePermission, RolePermission.permission_id == Permission.id )
             ).where( RolePermission.role_id == role_id)
    
    def get_permissions_queryset(self):
        #all
        return select( [ ContentType.display_name.label('content_type_display_name'),
                         ContentType.code_name.label('content_type_code_name'),
                         Permission.id, Permission.display_name, Permission.code_name,
                         Permission.content_type_id 
                        ] 
            ).select_from( Permission.__table__.join(
                ContentType, ContentType.id == Permission.content_type_id )
            ) #.where( RolePermission.role_id == role_id)




    def list(self,req,resp,db, role_id):
        role_permissions = db.objects( self.get_queryset(role_id) ).fetch()
        permissions = db.objects( self.get_permissions_queryset() ).fetch()

        #make permissions
        role_permissions_ids = [ p.get("id") for p in role_permissions ]

        for p in permissions:
            direction = "left"
            if p.get("id") in role_permissions_ids:
                #mark the permission as assigned.
                direction = "right"
            p.update({"direction": direction })       
        return permissions