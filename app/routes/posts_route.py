from app.controllers import posts_controller

def posts_route(app):
    
    @app.get("/posts")
    def get_posts():
        return posts_controller.get_posts_list()

    @app.get("/posts/<id>")
    def get_post(id: int):
        id = int(id)
        return posts_controller.get_post_by_id(id)

    @app.delete("/posts/<id>")
    def delete_post(id: int):
        id = int(id)
        return posts_controller.delete_post_by_id(id)

    @app.patch("/posts/<id>")
    def change_post(id: int):
        id = int(id)
        return posts_controller.change_post_by_id(id)

    @app.post("/posts")
    def creat_post():
        return posts_controller.create_post()
