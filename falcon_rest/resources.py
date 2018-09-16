

class BaseResource:

    login_required = True
    model = None
    queryset = None

    def get_queryset(self):
        return self.queryset
    

    def get_db(self, req):
        return req.context['db']

