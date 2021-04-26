import asyncio
from peewee import *
import logging
from peewee_async import Manager,PostgresqlDatabase
pg_db = PostgresqlDatabase('pw_db',user='pw_user',password='123456',
                           host='localhost',port=5432)

loop = asyncio.get_event_loop()
objects = Manager(pg_db,loop=loop)


class BaseModel(Model):
    class Meta:
        database = pg_db


class Page(BaseModel):
    title = CharField(unique=True)
    text = TextField()



class PageContent(BaseModel):
    page = ForeignKeyField(Page,backref='content')
    video = CharField()
    views = IntegerField(default=0)