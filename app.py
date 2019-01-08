import mongoengine
import datetime

def global_init():
    mongoengine.register_connection(alias='test_db', name='test_db')

class Booking(mongoengine.EmbeddedDocument):
    # meta = {
    #     'db_alias': 'test_db',
    #     'collection': 'extra_data'
    # }
    sex = mongoengine.StringField()
    marital = mongoengine.BooleanField()


class User(mongoengine.Document):
    meta = {
        'db_alias': 'test_db',
        'collection': 'users'
    }
    username = mongoengine.StringField(required=True)
    creation_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    email = mongoengine.StringField(required=True, unique=True)
    bookings = mongoengine.EmbeddedDocumentListField(Booking)



def create_new_user(name, email, extra=None):
    user = User()
    user.username = name
    user.email = email
    if extra:
        try:
            user.additional_info.sex = extra[0]
        except Exception:
            pass
    user.save()
    return user


def main():
    global_init()
    name = input("name")
    mail = input("mail")
    extra = ['F', 'M']
    create_new_user(name, mail, extra)
    print("great success")

if __name__ == "__main__":
    main()
