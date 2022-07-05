from mongoengine import *  

# BooleanField  #по идеи да или нет
# IntField  #цифры
# DateTimeField #время
# StringField #текст
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


#class 
#t1=Teacher.get_or_create(tid = 'T3', name = 'Mur')
#print(t1.id)
#t2=Teacher.get_or_skip(tid = 'T5', name = 'Mur')
#if t2 != None:
#    print(t2.id)
#else:
#    print('None')

print('Done')