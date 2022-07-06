from mongoengine import *  

connect("Minister-of-Justice")

class MyDocument(Document):
    @classmethod
    def get_or_create(cls, **kwargs):
        if len(cls.objects.filter(**kwargs)) == 1:
            return cls.objects.get(**kwargs)
        else:
            return cls.objects.create(**kwargs)
    @classmethod
    def get_or_skip(cls, **kwargs):
        if len(cls.objects.filter(**kwargs)) == 1:
            return cls.objects.get(**kwargs)
        else:
            return None
    meta = {
        'allow_inheritance' : True,
        'abstract' : True
    }

class AdminStaff (MyDocument):
    member= IntField(required=True)

class Guilds (MyDocument):
    guild = IntField(required=True)
    role= IntField(default=0)
    number = IntField(default=0)
    city = StringField(default='-')
    verified = BooleanField(default=False)

class Streets(MyDocument):
    city = ReferenceField(Guilds)
    number = IntField()
    name = StringField()
    deleted = BooleanField(default=False)
    @classmethod
    def get_number(cls, city):
        data = cls.objects.filter(city=city)
        if len(data) >= 1:
            return data[len(data) - 1].number + 1
        else:
            return 1

class Premises(MyDocument):
    streetsname = ReferenceField(Streets)
    house = IntField()
    frame = IntField()
    сadastral_number = IntField()
    premises = StringField()
    type = StringField()
    owner = StringField(default="Имущество города")
    owner_id = IntField(default="0")