import mongoengine
import datetime


def global_init():
    mongoengine.register_connection(alias='test_db', name='test_db')


class ExtraUserInfo(mongoengine.EmbeddedDocument):
    sex = mongoengine.StringField(default=None)
    marital = mongoengine.StringField(default=None)


class User(mongoengine.Document):
    meta = {
        'db_alias': 'test_db',
        'collection': 'users'
    }
    username = mongoengine.StringField(required=True)
    creation_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    email = mongoengine.StringField(required=True, unique=True)
    extra_info = mongoengine.EmbeddedDocumentField(ExtraUserInfo)


def create_new_user():
    name = input("name ")
    email = input("mail ")
    print("add confidential data? ")
    extra = input("Y/N: ")
    user = User()
    user.username = name
    user.email = email
    if extra in ['y', 'Y']:
        additional = ExtraUserInfo()
        additional.marital = input('marital: ')
        additional.sex = input('sex: ')
        user.extra_info = additional
    user.save()
    return user


def show_user_info(username):
    user = User.objects(username=username).all()
    return user.to_json()


def show_all_users():
    users = [item.to_json() for item in User.objects().all()]
    return users


def delete_user(username):
    user = User.objects(username=username).first()
    try:
        user.delete()
    except AttributeError:
        print("no such user")


def main():
    while True:
        global_init()
        print("\n select what to do from available commands: create, read, delete. \n")
        choice = input("Your choice: ")
        if choice == "create":
            create_new_user()
            print('user created')
        elif choice == "read":
            name = input('name: ')
            user_data = show_user_info(name)
            print(user_data)
        elif choice == "delete":
            name = input('name: ')
            delete_user(name)
        elif choice == "showall":
            print(show_all_users())
        else:
            print('no such command. quit')
            return False


if __name__ == "__main__":
    main()
