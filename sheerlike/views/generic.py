from django.views.generic.base import TemplateView
from django.http import Http404

from elasticsearch import TransportError

from sheerlike.query import get_document 

class SheerTemplateView(TemplateView):
    def get_template_names(self,*args, **kwargs):
        # if template_name is configured, just do that
        if self.template_name is not None:
            return [self.template_name]

        # otherwise, try to infer a template name from
        # the url
        request = self.request
        if request.path.endswith('/'):
            return [(request.path[1:]+'index.html')]
        else:
            return [request.path[1:]]

class SheerDetailView(TemplateView):
    doc_type = None
    local_name = 'object'

    def get_context_data(self, **kwargs):
        doc_id = kwargs.pop('doc_id')
        context = super(SheerDetailView, self).get_context_data(**self.kwargs)
        try:
            document = get_document(doctype=self.doc_type,
                                    docid=doc_id)
            context[self.local_name] = document

            return context
        except TransportError:
            raise Http404("Document does not exist")

