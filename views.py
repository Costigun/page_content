from aiohttp import web,ClientSession
import db
import jinja2
import aiohttp_jinja2
import aiofiles
import asyncio

@aiohttp_jinja2.template('page.html')
async def page_view(request):
    pages = db.Page.select().dicts()
    resp = [q for q in pages]
    return {'response':resp}

@aiohttp_jinja2.template('page_content.html')
async def pagecontent_view(request):
    page_name = request.match_info['name']
    page = await db.objects.get(db.Page,title=page_name)
    content = db.PageContent.select().where(db.PageContent.page == page.id).dicts()
    resp = []
    for c in content:
        resp.append(c)
    return {'content':resp}

