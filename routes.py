from views import page_view,pagecontent_view

def setup_routes(app):
    app.router.add_get('/',page_view)
    app.router.add_get('/{name}',pagecontent_view)