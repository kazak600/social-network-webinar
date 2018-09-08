from handlers.base import Index, Login, Signup


def setup_routes(app):
    app.router.add_get('/', Index.get)
    app.router.add_get('/login', Login.get)
    app.router.add_post('/login', Login.post)
    app.router.add_get('/signup', Signup.get)
