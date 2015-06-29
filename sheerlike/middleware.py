from threading import local
from django.http import HttpResponse

_active = local()

def get_request():
    return _active.request

class FlaskyHeaderGetter(object):
    def __init__(self, request):
        self.request= request

    def __getitem__(self, key):
        django_key = 'HTTP_' + key.upper().replace('-','_')
        return self.request.META.get(django_key)

    def get(self, key):
        return self.__getitem__(key)



class GlobalRequestMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        _active.request = request
        request.headers = FlaskyHeaderGetter(request)
        request.url = "%s://%s%s" % (request.scheme, request.get_host(),
                request.get_full_path())
        return None
