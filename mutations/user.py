import graphene
from schemas.user import User as UserSchema
from models import User as UserModel
import datetime


class UserMutation(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)
        image = graphene.String(required=True)

    user = graphene.Field(UserSchema)

    def mutate(self, info, name, image):

        if info.field_name == "addUser":
            time = datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
            user = UserModel(name=name, image=image, time=time)
            user.save()

        if info.field_name == "deleteUser":
            user = UserModel.objects(name=name).first()
            user.delete()

        if info.field_name == "updateUser":
            user = UserModel.objects(name=name).first()
            user.image = image
            user.time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user.save()

        return UserMutation(user=user)
