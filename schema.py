from graphene import ObjectType, Schema, Field
from graphene_mongo import MongoengineConnectionField
from graphene.relay import Node

from schemas.user import User as UserSchema
from mutations.user import UserMutation
from schemas.users import Users as UsersSchema
from mutations.users import UsersMutation


class Query(ObjectType):
    node = Node.Field()
    all_users = MongoengineConnectionField(UserSchema)
    user = Field(UserSchema)


class Mutation(ObjectType):
    add_user = UserMutation.Field()
    delete_user = UserMutation.Field()
    update_user = UserMutation.Field()

class CompanyQuery(ObjectType):
    node = Node.Field()
    all_users = MongoengineConnectionField(UsersSchema)
    user = Field(UsersSchema)

class CompanyMutation(ObjectType):
    add_user = UsersMutation.Field()
    delete_user = UsersMutation.Field()
    update_user = UsersMutation.Field()

schema = Schema(query=Query, types=[UserSchema], mutation=Mutation)
