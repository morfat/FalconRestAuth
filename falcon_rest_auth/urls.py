
from falchemy_rest.urls import urlpatterns
from .settings import PROJECT_NAME 


routes = urlpatterns(
    project_name = PROJECT_NAME,
    version = 'v2.0',
    app_routes = [
        ('/applications','applications'),
        ('/tenants','tenants'),
        ('/sites','sites'),
        ('/organizations','organizations'),
        ('/clients','clients'),
        ('/users','users'),
        ('/apis','apis'),
        ('/emails','emails'),
        ('/roles','roles'),
        ('/teams', 'teams'),
        ('/contentTypes','content_types')
        ]
    )


