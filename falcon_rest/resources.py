import falcon 


class BaseResource:

    login_required = True
    model = None
    queryset = None
    serializer_class = None


    def get_queryset(self,**kwargs):
        try:
            return self.queryset or self.model.all()
        except TypeError:
            return self.queryset


    def get_db(self, req):
        return req.context['db']
    

    def on_get(self,req, resp):
        db = self.get_db(req)
        query_params = req.params 

        results, pagination = self.list(req,resp,db)

        resp.media = {"data": results, "pagination": pagination}

    
    def list(self,req,resp,db,**kwargs):
        
        results = db.objects( self.get_queryset() ).fetch()
        #do filtering, implement pagination
        pagination = {}

        return results, pagination 


    def on_post(self,req, resp):
        db = self.get_db(req)
        posted_data = req.media

        created_data = self.create(req,resp,db,posted_data)
        resp.media = { "data": [ created_data ] }

        resp.status = falcon.HTTP_CREATED
    
    def create(self,req,resp,db,posted_data, **kwargs):

        created_data = db.objects( self.model ).create(**posted_data)

        return created_data
    


