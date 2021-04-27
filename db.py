import asyncio
from peewee import *
import logging
from peewee_async import Manager, PooledPostgresqlDatabase

pg_db = PooledPostgresqlDatabase('pw_db', user='pw_user', password='123456',
                           host='localhost', port=5432,max_connections=10)

loop = asyncio.get_event_loop()
objects = Manager(pg_db, loop=loop)


class BaseModel(Model):
    class Meta:
        database = pg_db


class PageContent(BaseModel):
    title = CharField()
    video = CharField()
    views = IntegerField(default=0)


class Page(BaseModel):
    title = CharField()
    text = TextField()
    slug = CharField(unique=True,max_length=10)


class PageBlock(BaseModel):
    content = ForeignKeyField(PageContent)
    page = ForeignKeyField(Page)




