import falcon 

from .pagination import Paginator

class ListResourceMixin:

    filterable_fields = ()

    searchable_fields = ()

    """ List model and also filter and search  """


    def list(self,req,resp,db,**kwargs):

        query_params = req.params
        queryset = self.get_queryset()
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
    
    def filter_queryset(self, queryset_object,filter_params):
        filter_params = dict(filter_params) #since we donot want to inteferere with global query_params

        """ for the filter params we expect example dict:
           { 'name__startswith': ' mosoti' , 'age': 20, 'gender__ne':'M' } e.t.c.

           for search, we apply or

        """

        search_text =  filter_params.pop(self.SEARCH_QUERY_PARAM_NAME , None )
        

        if search_text:
            #filter queryset with or
            search_params = {}
            for field in self.searchable_fields:
                field__condition = "{field}__contains".format(field = field)

                search_params.update({ field__condition: search_text })

            
            queryset_object = queryset_object.or_filter( **search_params )
        
        
        filter_params_copy = dict(filter_params)

        for field_and_condition, field_value in filter_params_copy.items():
            field_name = field_and_condition.split("__")[0]
            
            if field_name not in self.filterable_fields:
                #remove the fiilter as is not allowed

                del filter_params[field_name]
        
        #apply AND filter
        queryset_object = queryset_object.filter( **filter_params )

        return queryset_object




            


            
        

class BaseResource:

    login_required = True
    model = None
    queryset = None
    serializer_class = None

    SEARCH_QUERY_PARAM_NAME = 'q'

    paginator_class = Paginator
  

    def get_queryset(self,**kwargs):
        try:
            return self.queryset or self.model.all()
        except TypeError:
            return self.queryset
    
    def get_serializer_class(self,**kwargs):
        return self.serializer_class



    def get_db(self, req):
        return req.context['db']
    

    def on_post(self,req, resp):
        db = self.get_db(req)
        posted_data = req.media

        data = self.get_serializer_class()(posted_data).data

        print (data)

        print(self.get_serializer_class().write_protected_fields)
        


        created_data = self.create(req,resp,db,posted_data)
        resp.media = { "data": [ created_data ] }

        resp.status = falcon.HTTP_CREATED
    
    def create(self,req,resp,db,posted_data, **kwargs):

        created_data = db.objects( self.model ).create(**posted_data)

        return created_data
    



class ListResource(ListResourceMixin , BaseResource):

    def on_get(self,req, resp):
        db = self.get_db(req)
        query_params = req.params 

        results, pagination = self.list(req,resp,db)

        resp.media = {"data": results, "pagination": pagination}
