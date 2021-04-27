from aiohttp import web,ClientSession
import db
import jinja2
import aiohttp_jinja2
import aiofiles
import asyncio
from peewee import *



@aiohttp_jinja2.template('page.html')
async def page_view(request):
    pages = db.Page.select().dicts()
    resp = [q for q in pages]
    return {'response':resp}




@aiohttp_jinja2.template('page_content.html')
async def pagecontent_view(request):
    async with db.objects.atomic():
        param = request.rel_url.query
        page_name = request.match_info['name']
        page = await db.objects.get(db.Page,title=page_name)
        content = await db.objects.execute(
            db.PageContent.select().join(db.PageBlock).where(db.PageBlock.page == page)
        )
        resp = []
        for c in content:
            print(type(c))
            db.PageContent.update(views=db.PageContent.views + 1).where(db.PageContent.id == c.id).execute()
            resp.append(c)
        return {'content':resp}
