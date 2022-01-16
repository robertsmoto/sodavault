import graphene
import advertisingapp.schema
import blogapp.schema


class Query(
        advertisingapp.schema.Query,
        blogapp.schema.Query,
        ):
    pass


schema = graphene.Schema(query=Query)
