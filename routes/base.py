from handlers.base import Index, Login, Signup


def setup_routes(app):
    app.router.add_get('/', Index.get, name='index')
    app.router.add_get('/login', Login.get, name='login')
    app.router.add_post('/login', Login.post)
    app.router.add_get('/signup', Signup.get, name='signup')
