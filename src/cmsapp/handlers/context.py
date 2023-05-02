class ContextHandler:

    def __init__(self, *args, **kwargs):
        self.initial_data = kwargs.get('initial_data', None)
        self.svapi = kwargs.get('svapi', None)
        self.prefix = kwargs.get('prefix', '')
        if 'collection' in self.prefix:
            self.prefix = self.prefix.split("_")[0]
        self.data = {}  # will be sent to context

    def handle(self):
        ids = self.initial_data.get(self.prefix, [])

        if not ids:
            self.data = {}
            return

        ids_str = " | ".join(ids)
        params = {
            'qs': f"@docID:{{{ids_str}}}",
            'sortBy': "docCreatedAt:ASC"
        }
        results, err = self.svapi.getMany('search', params)
        if err:
            print("ERROR context.ContextHandler", err)
        self.data = results


CONTEXT_HANDLER_BY_PREFIX = {
    'image_collection': ContextHandler,
    'file_ection': ContextHandler,
}
