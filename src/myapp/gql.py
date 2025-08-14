import graphene
from graphene_django import DjangoObjectType

from myapp.models import MyModel as DjangoModel


class MyModel(DjangoObjectType):
    class Meta:
        model = DjangoModel

    status = graphene.Field('myapp.gql.MyModelStatus')

    def resolve_status(self, info):
        return # TODO


class MyModelStatus(graphene.ObjectType):
    mymodel = graphene.Field(MyModel)
    presence = graphene.Boolean()
    id = graphene.ID()

    def resolve_id(self, info):
        return None # TODO

    def resolve_mymodel(self, info):
        return None # TODO

    def resolve_presence(self, info):
        return None # TODO


class MyModelQuery(graphene.ObjectType):
    models = graphene.List(MyModel)
    models_status = graphene.List(MyModelStatus)

    def resolve_models(self, info):
        return DjangoModel.objects.all()

    def resolve_models_status(self, info):
        return None # TODO