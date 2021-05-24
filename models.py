from peewee import *
from playhouse.shortcuts import model_to_dict

db = SqliteDatabase('db.sqlite3', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db

    @property
    def as_dict(self):
        return model_to_dict(self)


class User(BaseModel):
    name = TextField(unique=True)


class Note(BaseModel):
    user = ForeignKeyField(User, on_delete='CASCADE', backref='notes')
    text = TextField()
