from views import page_view,pagecontent_view,download_file


def setup_routes(app):
    app.router.add_get('/',page_view,name='page')
    app.router.add_get('/{slug}',pagecontent_view,name='content'),
    app.router.add_get('/file/{file_name}', download_file)

