
from falchemy_rest.urls import urlpatterns
from .settings import PROJECT_NAME 


routes = urlpatterns(
    project_name = PROJECT_NAME,
    version = 'v1',
    app_routes = [
        ('/applications','applications'),
        ('/tenants','tenants'),
        ('/organizations','organizations'),
        ('/clients','clients'),
        ('/users','users'),
        ('/apis','apis'),
        ]
    )


