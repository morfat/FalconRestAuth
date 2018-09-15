
import datetime


from sqlalchemy.sql import select
from oauth.database import Schema
from oauth.lib.store import Store 


class ProjectStore(Store):
    table = Schema.projects 

    def get_by_uri(self,uri):
        query = select([self.table]).where(self.table.c.uri == uri)

        return self.fetch_one(query)
