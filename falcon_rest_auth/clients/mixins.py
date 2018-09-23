import falcon

from .models import Client

class ClientMixin:

    def get_client(self, db,client_id):
        if not client_id:
            raise falcon.HTTPBadRequest(title="Missing client_id Field", description="client_id field is needed")
        
        client =  db.objects( Client.get(client_id) ).fetch()[0]
        if not client:
            raise falcon.HTTPBadRequest(title="Invalid Client", description="Valid client_id is needed")
        
        return client