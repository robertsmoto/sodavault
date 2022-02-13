import advertisingapp.schema
import blogapp.schema
import configapp.schema
import contactapp.schema
import graphene


class Query(
        advertisingapp.schema.Query,
        blogapp.schema.Query,
        configapp.schema.Query,
        contactapp.schema.Query,
        ):
    pass


schema = graphene.Schema(query=Query)
