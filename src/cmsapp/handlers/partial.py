from .select2 import Select2ErrorHandler
from datetime import datetime


class CollectionPostHandler:

    def __init__(self, request, form, *args, **kwargs):
        self.request = request
        self.prefix = kwargs.get('prefix', '')
        self.form = form(prefix=self.prefix)
        # self.document_initial = kwargs.get('document_initial', {})
        # self.svapi = kwargs.get('svapi', None)
        # self.docType = kwargs.get('docType', '')
        # self.docID = kwargs.get('docID', '')
        self.cleaned_data = {}

    def handle(self):

        print("## self.document initial", )
        for field in self.form.fields:
            print("## field")
            print("## self.prefix", self.prefix)
            data = self.request.POST.getlist(f"{self.prefix}-{field}", [])
            self.cleaned_data[field] = data
            print("## cleaned data", self.cleaned_data)


class DocumentPostHandler:

    def __init__(self, *args, **kwargs):
        self.document_initial = kwargs.get('document_initial', {})
        self.cleaned_data = {}

    def handle(self):
        """Validates and hydrates 'document' fields."""
        doc = self.document_initial
        cd = self.cleaned_data
        cd['ID'] = doc.get('ID', '')
        cd['parentID'] = doc.get('parentID', '')
        cd['type'] = doc.get('type', 'image')
        cd['title'] = doc.get('title', 'test title')
        cd['lexi'] = doc.get('lexi', 'and lexi')
        cd['description'] = doc.get('description', 'and description')
        cd['index'] = doc.get('index', '')
        cd['createdAt'] = doc.get('createdAt', datetime.now())
        cd['updatedAt'] = doc.get('updatedAt', datetime.now())


PARTIAL_HANDLERS_BY_DOCTYPE = {
    'image': DocumentPostHandler,
}
