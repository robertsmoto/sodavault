from cmsapp.constants import GENALPHA
from datetime import datetime
from django.forms import ChoiceField, MultipleChoiceField
from django_select2.forms import Select2TagWidget
from nanoid import generate
from svapi_py.api import SvApi


class Select2WidgetUpdater:

    def __init__(self, request, form, **kwargs):
        self.request = request
        self.form = form
        self.docType = kwargs.get('docType', '')
        self.docID = kwargs.get('docID', '')
        self.svapi = SvApi(request)
        self.fields = self.form.fields

    def _make_choices(self):
        for field, obj in self.fields.items():
            isChoiceField = [
                isinstance(obj, ChoiceField),
                isinstance(obj, MultipleChoiceField),
            ]
            if not any(isChoiceField):
                continue
            docType = field
            if self.form.prefix == 'document':
                docType = self.docType
            params = {'qs': f'@docType:{{{docType}}}'}
            results, err = self.svapi.getMany('search', params=params)
            if err == 'no data':
                print("## no data", err)
                continue
            choices = self.svapi.makeChoices(results, self.docID)
            self.form.fields[field].choices = choices

    def handle(self):
        self._make_choices()


class Select2ErrorHandler:

    def __init__(self, request, form, **kwargs):
        self.request = request
        self.form = form
        self.svapi = SvApi(request)
        self.choices_index = {}
        self.post_values = []
        self.field_name = ''

    def _inspect_cleaned_data(self):
        """Adds field to the form.cleaned_data if it does not exist."""
        self.form.cleaned_data[self.field_name] = self.form.cleaned_data.get(
            self.field_name, [])
        return self

    def _create_chioces_index(self):
        """Creates a choices index."""
        choices = self.form.fields[self.field_name].choices
        for cid, ctext in choices:
            self.choices_index[cid] = ctext
        return self

    def _get_post_values(self):
        """Gets the exiting request.POST values for given field_name."""
        self.post_values = self.request.POST.getlist(
            f"{self.form.prefix}-{self.field_name}", [])
        return self

    def _add_to_SODAvault(self, tag: str):
        now = datetime.now()
        new_pid = generate(GENALPHA, 16)
        key_data = {
            'document': {
                'ID': new_pid,
                'type': self.field_name,
                'title': tag,
                'description': f"{tag.title()} autoGen",
                'lexi': f"{self.field_name[0:3]}_{self.field_name[0:3]}_"
                        f"{tag[0:3]}",
                'index': '',
                'createdAt': now,
                'updatedAt': now,
            }}

        if not self.svapi:
            print("ERROR: Needs svapi instance")
        else:
            response = self.svapi.add('document', data=key_data)
            if response.status_code != 200:
                print(f"ERROR {response}")

        return new_pid

    def _add_to_cleaned_data(self, pid: tuple):
        self.form.cleaned_data[self.field_name].append(pid)

    def _append_field_chioces(self, data: tuple):
        self.form.base_fields[self.field_name].choices.append(data)

    def _process_existing_choices(self):
        """Adds existing choices back into the cleaned data."""
        for pid in self.post_values:
            ctext = self.choices_index.get(pid, '')
            if ctext:
                self._add_to_cleaned_data(pid)

    def _process_new_terms(self):
        """Adds new terms to sodaVault as document, and adds to choices."""
        for pid in self.post_values:
            ctext = self.choices_index.get(pid, '')
            if ctext:
                continue
            tag = pid
            new_pid = self._add_to_SODAvault(tag)
            self._add_to_cleaned_data(new_pid)
            self._append_field_chioces((new_pid, tag))
            # print("## new_pid, tag", new_pid, tag)

    def handle(self):
        """Finds and processes new Select2 Terms."""

        # print("## Select2 ERROR handler begin")
        for f, error in self.form.errors.as_data().items():
            field_instance = self.form.fields.get(f, None)
            field_widget = None
            if field_instance:
                field_widget = field_instance.widget
            if not isinstance(field_widget, Select2TagWidget):
                continue
            self.field_name = f
            self._inspect_cleaned_data()
            self._create_chioces_index()
            self._get_post_values()
            self._process_existing_choices()
            self._process_new_terms()
