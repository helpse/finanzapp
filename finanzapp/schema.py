import graphene
from graphene_django.debug import DjangoDebug

from core.schema import Query as CoreQuery, Mutation as CoreMutation


class Query(
            CoreQuery,
            graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(
            CoreMutation,
            graphene.ObjectType):
    """
    Mutation
    """
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
