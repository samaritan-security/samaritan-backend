from graphene import ObjectType, Schema, Field
from graphene_mongo import MongoengineConnectionField
from graphene.relay import Node

from schemas.user import User as UserSchema
from mutations.user import UserMutation


class Query(ObjectType):
    node = Node.Field()
    all_users = MongoengineConnectionField(UserSchema)
    user = Field(UserSchema)


class Mutation(ObjectType):
    add_user = UserMutation.Field()
    delete_user = UserMutation.Field()
    update_user = UserMutation.Field()


schema = Schema(query=Query, types=[UserSchema], mutation=Mutation)
