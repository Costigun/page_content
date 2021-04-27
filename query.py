import asyncio
import os
import pathlib
from db import objects,Page,loop,PageContent,PageBlock

BASE_DIR = pathlib.Path(__file__).parent.absolute()

MEDIA = os.path.join(BASE_DIR,'media')

def save_file(filename):
    return '/media/'+filename


pages = {'frodo_bio':'sad','tony':'stark','harry':'potter'}
content = {'philosoph':'choclate.jpg','ring of powerful':'mae.png','foofoo':'mse.png'}


async def populate_data():
    for key,value in pages.items():
        await objects.create(Page,title=key,text=value)
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