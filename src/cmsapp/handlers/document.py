from .select2 import Select2ErrorHandler
from datetime import datetime


class GenericPostHandler:

    def __init__(self, request, form, *args, **kwargs):
        self.request = request
        self.form = form  # this is not instantiated
        self.form_inst = None
        self.prefix = kwargs.get('prefix', '')
        self.svapi = kwargs.get('svapi', None)
        self.docType = kwargs.get('docType', '')
        self.docID = kwargs.get('docID', '')
        self.document_initial = kwargs.get('document_initial', {})
        self.cleaned_data = {}

    def _handle_error(self):
        if 'collection' in self.prefix:
            handler = Select2ErrorHandler(self.request, self.form_inst)
            handler.handle()
            self.cleaned_data = handler.form.cleaned_data
        else:
            raise Exception("GenericPostHandler Error")

    def _handle_valid_data(self):
        self.cleaned_data = self.form_inst.cleaned_data

    def handle(self):

        self.form_inst = self.form(
            self.request.POST,
            self.request.FILES,
            initial=self.document_initial.get(self.prefix, {}),
            prefix=self.prefix,
            svapi=self.svapi,
            docType=self.docType,
            docID=self.docID,
        )

        valid = self.form_inst.is_valid()
        changed = self.form_inst.has_changed()

        if not valid:
            self._handle_error()

        elif valid and changed:
            self._handle_valid_data()

        else:
            self.cleaned_data = self.form_inst.initial
