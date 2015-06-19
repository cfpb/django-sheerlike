from django.views.generic.base import TemplateView
from django.http import Http404

from elasticsearch import TransportError

from sheerlike.query import get_document 

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

