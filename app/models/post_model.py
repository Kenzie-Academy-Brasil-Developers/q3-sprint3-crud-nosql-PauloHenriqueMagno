from datetime import datetime
import pymongo

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["kenzie"]

class Post:
    def __init__(self, *args, **data):
        date = datetime.now()
        date = date.strftime("%d/%m/%Y %H:%M:%S")
        posts_id_list = list([])

        for post in list(db.posts.find()):
            posts_id_list.append(post["id"])

        self.id = 1 if len(posts_id_list) == 0 else max(posts_id_list) + 1
        self.created_at = date
        self.last_update = date
        self.title = data["title"]
        self.author = data["author"]
        self.tags = data["tags"]
        self.content = data["content"]