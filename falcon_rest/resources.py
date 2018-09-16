import falcon 


class BaseResource:

    login_required = True
    model = None
    queryset = None

    def get_queryset(self,**kwargs):
        queryset = self.queryset or self.model.all()

        return queryset
    

    def get_db(self, req):
        return req.context['db']
    

    def on_post(self,req, resp):
        db = self.get_db(req)
        posted_data = req.media

        created_data = self.create(req,resp,db,posted_data)
        resp.media = { "data": [ created_data ] }

        resp.status = falcon.HTTP_CREATED
    
    def create(self,req,resp,db,posted_data, **kwargs):

        created_data = db.objects( self.model ).create(**posted_data)

        return created_data
    


