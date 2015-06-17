from threading import local

_active = local()

def get_request():
    return _active.request

class GlobalRequestMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        _active.request = request
        return None
