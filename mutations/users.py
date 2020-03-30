import graphene
from schemas.users import Users as UsersSchema
from models import Users as UsersModel
import datetime


class UsersMutation(graphene.Mutation):

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    users = graphene.Field(UsersSchema)

    def mutate(self, info, username, password):

        if info.field_name == "addUser":
            time = datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
            users = UsersModel(username=username, password=password, time=time)
            users.save()

        if info.field_name == "deleteUser":
            users = UsersModel.objects(username=username).first()
            users.delete()

        if info.field_name == "updateUser":
            users = UsersModel.objects(username=username).first()
            users.password = password
            users.time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            users.save()

        return UsersMutation(users=users)
