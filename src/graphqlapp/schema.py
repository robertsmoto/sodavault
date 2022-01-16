import graphene
import advertisingapp.schema


class Query(
        advertisingapp.schema,):
    pass


schema = graphene.Schema(query=Query)
