import asyncio
import os
import pathlib
from db import *
from peewee import PostgresqlDatabase

BASE_DIR = pathlib.Path(__file__).parent.parent
MEDIA = os.path.join(BASE_DIR, 'media')

pg_db.connect()
pg_db.create_tables([Page, PageContent,PageBlock])

pages = [('Гастро блог','В Венеции круто!Все рестораны достойны мишлен!','gastro'),
         ('Блог переводчика!','Очень сложно знать много языков, сам путаюсь!','translator'),
         ('Блог программиста','Почему так?','wtf')]
content = {'Пилотный пост':'video1.mp4',
           'Yandex или google':'video2.mp4',
           'stackoverflow or github gist':'video3.mp4'}


async def populate_data():
    for title,text,slug in pages:
        await objects.create(Page,title=title,text=text,slug=slug)
    for key,value in content.items():
        await objects.create(PageContent,title=key,video=value)

    pages_query = await objects.execute(Page.select())
    content_query = await objects.execute(PageContent.select())
    for page in pages_query:
        for con in content_query:
            await objects.create(PageBlock,content=con,page=page)

if __name__ == '__main__':
    loop.run_until_complete(populate_data())
    loop.close()
    pg_db.close()