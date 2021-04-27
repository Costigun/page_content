from aiohttp import web,ClientSession
import db
import jinja2
import aiohttp_jinja2
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
        k_slug = request.match_info['slug']
        page = await db.objects.get(db.Page, slug=k_slug)

        if 'sort_by' in param:
            ordering = ['asc','desc']
            sort_value = param['sort_by']
            if sort_value in ordering:
                if sort_value == 'desc':
                    query = (db.PageContent
                             .select().join(db.PageBlock).where(db.PageBlock.page == page)
                             .order_by(db.PageContent.title.desc()))
                else:
                    query = (db.PageContent
                             .select().join(db.PageBlock).where(db.PageBlock.page == page)
                             .order_by(db.PageContent.title.asc()))
        else:
            query = (db.PageContent
                     .select().join(db.PageBlock).where(db.PageBlock.page == page))
        content = await db.objects.execute(query)
        resp = []
        for c in content:
            print(type(c))
            db.PageContent.update(views=db.PageContent.views + 1).where(db.PageContent.id == c.id).execute()
            resp.append(c)
        return {'content':resp,'main_page':page}
