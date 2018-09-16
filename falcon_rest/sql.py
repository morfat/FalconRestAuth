class QuerySet:

    def __init__(self,connection,queryset):
        self._queryset = queryset
        self._connection = connection

    
    def filter(self,**filters):
        #implement filters
        return self._queryset
    
    def fetch(self, limit = None):
        results = self._connection.execute(self._queryset).fetchall()
        return results

        
    def count(self):
        pass
    
    def create(self, **data):
        result =  self._connection.execute( self._queryset.insert().values(**data) )
        
        pk = result.inserted_primary_key[0]

        data.update({"id": pk })

        return data
        





class Db:
    
    def __init__(self,connection):
        self._connection = connection
    
    def objects(self,queryset):
        #can be queryset or table
        return QuerySet(self._connection,queryset)
    
  