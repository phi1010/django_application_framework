import logging

from django.conf import settings
import graphene
from graphql import GraphQLError
from icecream import ic

from accounts.gql import UsersQuery
from myapp.gql import MyModelQuery

log = logging.getLogger(__name__)


class SecurityMiddleware(object):
    """
    Properly capture errors during query execution and send them to Sentry.
    Then raise the error again and let Graphene handle it.
    """

    def resolve(self, next, root, info, **args):
        return next(root, info, **args)


class Query(
    MyModelQuery,
    UsersQuery,
    graphene.ObjectType
):
    if settings.DEBUG:
        from graphene_django.debug import DjangoDebug
        debug = graphene.Field(DjangoDebug, name='_debug')


schema = graphene.Schema(query=Query)
