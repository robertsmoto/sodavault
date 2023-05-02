from typing import Tuple


class PostIngredientsHandler:

    def __init__(self, request, form, **kwargs):
        self.request = request
        self.form = form
        self.form_inst = None
        self.prefix = kwargs.get('prefix', '')
        self.svapi = kwargs.get('svapi', None)
        self.docType = kwargs.get('docType', '')
        self.docID = kwargs.get('docID', '')
        self.document_initial = kwargs.get('document_initial', {})

        self.initial_data_unpkd = {}
        self.values_index = {}
        self.cleaned_data = []

    def _unpack_initial_data(self):
        unpkd_data = {}
        data = self.document_initial.get('ingredients', [])
        for d in data:
            for k, v in d.items():
                if k == 'quantity':
                    v = int(v)
                if k not in unpkd_data:
                    unpkd_data[k] = []
                unpkd_data[k].append(v)

        self.initial_data_unpkd = unpkd_data

    def _get_comparison_data(self, idx: int) -> Tuple[dict, dict]:
        idata = {}
        pdata = {}
        for field in self.form().fields:
            # initial data
            ikey = field
            ival = self.initial_data_unpkd.get(ikey, [])
            if len(ival) - 1 >= idx:
                ival = ival[idx] if ival[idx] else ''
                idata[ikey] = ival
            # post data
            pkey = f"{self.prefix}-{field}"
            pval = self.request.POST.getlist(pkey, [])[idx]
            pdata[pkey] = pval
        return idata, pdata

    def _handle_valid_data(self):
        self.cleaned_data.append(self.form_inst.cleaned_data)

    def _handle_error(self):
        raise Exception("PostIngredientsHandler Error", self.form_inst.errors)

    def handle(self):
        """Data is posted in lists, need to unpack them and return a dict."""

        # unpack the initial data
        self._unpack_initial_data()

        # determine the length based on a field
        lenkey = ''
        if self.prefix == 'ingredients':
            lenkey = 'ingredients-name'

        for idx in range(
                len(self.request.POST.getlist(lenkey, []))):
            # get comparison data
            idata, pdata = self._get_comparison_data(idx)

            self.form_inst = self.form(
                pdata,
                self.request.FILES,
                initial=idata,
                prefix=self.prefix,
                svapi=None,
                docType=None,
                docID=None)

            valid = self.form_inst.is_valid()
            changed = self.form_inst.has_changed()

            if not valid:
                self._handle_error()

            elif valid and changed:
                self._handle_valid_data()

            else:
                self.cleaned_data.append(self.form_inst.initial)
