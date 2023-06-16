class Service(object):
    def __init__(self, request):
        self.request = request
        self.user = request.user
