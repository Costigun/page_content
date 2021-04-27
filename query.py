import asyncio
import os
import pathlib
from db import objects,Page,loop,PageContent,PageBlock
from peewee import PostgresqlDatabase

BASE_DIR = pathlib.Path(__file__).parent.absolute()

MEDIA = os.path.join(BASE_DIR,'media')


def save_file(filename):
    return '/media/'+filename

pages = [('Гастро блог','В Венеции круто!Все рестораны достойны мишлен!','gastro'),
         ('Блог переводчика!','Очень сложно знать много языков, сам путаюсь!','translator'),
         ('Блог программиста','Почему так?','wtf')]
content = {'Пилотный пост':'choclate.jpg',
           'Yandex или google':'mae.png',
           'stackoverflow or github gist':'mse.png'}


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