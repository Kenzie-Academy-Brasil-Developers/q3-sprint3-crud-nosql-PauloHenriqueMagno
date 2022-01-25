from app.routes.posts_route import posts_route

def init_app(app):
    posts_route(app)