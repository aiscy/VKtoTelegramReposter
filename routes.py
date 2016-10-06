from endpoints import lc_callback

def setup_routes(app, project_root):
    app.router.add_post('/callback/lc', lc_callback)
