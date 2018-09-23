

from .resources import *

routes = [
    ('',ListCreateUsers() ),
    ('/{pk}',RetrieveUpdateUser() ),
    ('/login',LoginUser() ),
    ('/register',RegisterUser() ),
    ('/changePassword',UserChangePassword()),
    ('/resetPassword',UserResetPassword())

]

