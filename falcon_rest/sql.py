 
from sqlalchemy import  or_ , and_,column , desc, asc 



class QuerySet:

    def __init__(self,connection,queryset):
        self._queryset = queryset
        self._connection = connection
    
    def __get_column_filter(self,col_name,col_condition,col_value):
        #example input => ('name','contains','mosoti',)

        col = column( col_name ) #to sqlalchemy column

        ops_dict = {
            'startswith':col.startswith(col_value),
            'endswith': col.endswith(col_value),
            'contains': col.contains(col_value),
            'eq': col.op("=")(col_value),
            'lt': col.op("<")(col_value),
            'lte': col.op("<=")(col_value),
            'gt': col.op(">")(col_value),
            'gte': col.op(">=")(col_value)
        }   
    
        return ops_dict[col_condition]
    

    def __get_col_filters(self, **filters):
        """ for the filters params we expect example dict:
           { 'name__startswith': ' mosoti' , 'age': 20, 'gender__ne':'M' } e.t.c.
        """

        col_filters = []

        for field_and_condition, field_value in filters.items():
            field__condition = field_and_condition.split("__")
            
            field_name = field__condition[0]
            condition = 'eq' #by default we expect this

            try:
                condition = field__condition[1]
            except IndexError:
                pass
            
            col_filters.append( self.__get_column_filter(field_name , condition ,field_value) )
        return col_filters

    def filter(self,**filters):
        """ this applies AND """

        col_filters = self.__get_col_filters(**filters)
        #apply the filters

        self._queryset = self._queryset.where( 
            and_( *col_filters ) 
            )
        
        return self

    
    def or_filter(self, **filters):
        """ this applies OR to the queryset """

        col_filters = self.__get_col_filters(**filters)
        self._queryset = self._queryset.where( 
            or_( *col_filters ) 
            )
        
        return self
    
    def order_by_desc(self, column_name):

        """
         uses - for desc and without (-) for asc
         ASC is the default order by 
         Data type is String
        """

        self._queryset = self._queryset.order_by( desc( column( column_name ) ) )
      
        return self
    
    def order_by_asc(self, column_name):

        """
         ASC is the default order by 
         Data type is String
        """

        self._queryset = self._queryset.order_by( asc( column( column_name ) ) )
      
        return self

    
    




    def fetch(self, limit = None):
        
        queryset = self._queryset
        results = []

        if limit:
            queryset = self._queryset.limit(limit)
            if limit > 1:
                results = self._connection.execute(queryset).fetchall()
            else:
                result = self._connection.execute(queryset).fetchone()

                return result

        else:
            results = self._connection.execute(queryset).fetchall()

        
        return [ dict(r) for r in results ]
    
        
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
    
  