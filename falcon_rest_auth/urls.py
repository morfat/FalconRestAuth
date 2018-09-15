
from falcon_rest.urls import urlpatterns


routes = urlpatterns(
    project_name = 'falcon_rest_auth',
    version = 'v1',
    app_routes = [
        ('/applications','applications'),
        ]
    )


