
class PostFileHandler:

    def __init__(self, request, form, **kwargs):
        self.request = request
        self.form = form
        self.cleaned_data = {}

    def handle(self):
        self.form.cleaned_data = {}
        return


class PostFilesHandler:

    def __init__(self, request, form, **kwargs):
        self.request = request
        self.form = form
        self.form_inst = None
        self.initial_data_unpkd = {}
        self.values_index = {}
        self.cleaned_data = []

    def handle(self):
        self.form.cleaned_data = {}
        return
