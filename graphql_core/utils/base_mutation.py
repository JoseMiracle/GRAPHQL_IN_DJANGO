import graphene

from graphql_core.schema_types import ErrorType

class BaseMutation(graphene.Mutation):

    success = graphene.Boolean()
    errors = graphene.Field(ErrorType)
    message = graphene.String()


    @classmethod
    def mutate(cls, root, info, **kwargs):
        """To be overriden method"""