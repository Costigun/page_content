import asyncio
import os
import pathlib
from db import objects,Page,loop,PageContent

BASE_DIR = pathlib.Path(__file__).parent.absolute()

MEDIA = os.path.join(BASE_DIR,'media')

def save_file(filename):
    return '/media/'+filename


pages = {'frodo_bio':'sad','tony':'stark','harry':'potter'}
content = ['choclate.jpg','mae.png','mse.png']

async def create_page():
    async with objects.atomic():
        for page in pages:
            await objects.create(Page,title=page,text=pages[page])


async def create_content():
    async with objects.atomic():
        for page in pages:
            for block in content:
                p = await objects.get(Page,title=page)
                await objects.create(PageContent,page=p,video=save_file(block))


if __name__ == '__main__':
    coros = []
    coros.append(create_page())
    coros.append(create_content())
    loop.run_until_complete(asyncio.gather(*coros))
    loop.close()