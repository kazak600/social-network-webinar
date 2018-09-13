from handlers.base import Index, Login, Signup, Logout


def setup_routes(app):
    app.router.add_get('/', Index.get, name='index')
    app.router.add_get('/login', Login.get, name='login')
    app.router.add_post('/login', Login.post)
    app.router.add_get('/signup', Signup.get, name='signup')
    app.router.add_post('/signup', Signup.post)
    app.router.add_get('/logout', Logout.get, name='logout')
