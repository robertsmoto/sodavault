import graphene
import advertisingapp.schema


class Query(
        advertisingapp.schema.Query,):
    pass


schema = graphene.Schema(query=Query)
