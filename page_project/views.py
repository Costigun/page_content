import os
from query import MEDIA
from aiohttp import web
import db
import aiohttp_jinja2
from aiohttp import streamer
URL = "http://127.0.0.1:8080"


@aiohttp_jinja2.template('page.html')
async def page_view(request):
    async with db.pg_db.atomic_async():
        pages = db.Page.select().dicts()
        resp = [q for q in pages]
        return {'response':resp,'URL':URL}




@aiohttp_jinja2.template('page_content.html')
async def pagecontent_view(request):
    async with db.pg_db.atomic_async():
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
            db.PageContent.update(views=db.PageContent.views + 1).where(db.PageContent.id == c.id).execute()
            resp.append(c)
        return {'content':resp,'main_page':page,'URL':URL}




@streamer
async def file_sender(writer, file_path=None):

    with open(file_path, 'rb') as f:
        chunk = f.read(2 ** 16)
        while chunk:
            await writer.write(chunk)
            chunk = f.read(2 ** 16)


async def download_file(request):
    file_name = request.match_info['file_name']  # Could be a HUGE file
    headers = {
        "Content-disposition": "attachment; filename={file_name}".format(file_name=file_name)
    }

    file_path = os.path.join(MEDIA, file_name)
    print(file_path)
    if not os.path.exists(file_path):
        return web.Response(
            body='File <{file_name}> does not exist'.format(file_name=file_name),
            status=404
        )

    return web.Response(
        body=file_sender(file_path=file_path),
        headers=headers
    )