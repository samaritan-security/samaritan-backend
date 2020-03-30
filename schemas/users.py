from graphene_mongo import MongoengineObjectType
from graphene.relay import Node
from models import Users as UserModel


class Users(MongoengineObjectType):

    class Meta:
        model = UserModel
        interfaces = (Node,)