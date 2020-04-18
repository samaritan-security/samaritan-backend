from graphene_mongo import MongoengineObjectType
from graphene.relay import Node
from models import User as UserModel


class User(MongoengineObjectType):

    class Meta:
        model = UserModel
        interfaces = (Node,)
