from flask import jsonify, request
from datetime import datetime
import pymongo
from app.models.post_model import Post
from app.excepts.missing_property_error import MissingPropertyError
from app.excepts.wrong_value_error import WrongValueError
from app.excepts.content_not_found import ContentNotFound
from app.services.check_necessary_info import check_necessary_info
from app.services.check_tags import check_tags
from app.services.get_type import get_type

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["kenzie"]
necessary_info = ["title","author","tags","content"]
info_type = {"title": "string", "author": "string", "tags": "list", "content": "string"}

def get_posts_list():
    posts = list(db.posts.find())
    for post in posts:
        del post["_id"]
    return jsonify(posts), 200

def get_post_by_id(id):
    try:
        post = list(db.posts.find({"id": id}))
        post = post[0]
        del post["_id"]
        return jsonify(post), 200

    except ContentNotFound:
        return jsonify({"error": "Id not found"}), 404

def create_post():
    data = request.json

    try:
        if not check_necessary_info(data, necessary_info, {}):
            raise MissingPropertyError

        if not check_necessary_info(data, necessary_info, info_type):
            raise WrongValueError

        new_post = Post(**data)
        new_post = new_post.__dict__

        db.posts.insert_one(new_post)

        del new_post["_id"]

        return new_post, 201

    except MissingPropertyError:
        return jsonify({"error": "title, author, tags, content are necessary"}), 400

    except WrongValueError:
        resp = {"wrong fields": []}

        for value in necessary_info:
            type = get_type(data[value])

            if type != info_type[value]:
                resp["wrong fields"].append({value: type})

            if value == "tags" and not check_tags(data[value]):
                resp["wrong fields"].append({value: check_tags(data[value], True)})

        return jsonify(resp), 400

def delete_post_by_id(id):
    try:
        deleted = db.posts.delete_one({"id": id})
        if deleted.deleted_count == 0:
            raise ContentNotFound
        
        return jsonify(""), 204

    except ContentNotFound:
        return jsonify({"error": "Id not found"}), 404

def change_post_by_id(id):
    data = request.json

    try:

        post_changes = {}
        new_necessary_info = []
        for value in necessary_info:
            if not data.get(value):
                ...
            else:
                new_necessary_info.append(value)
                post_changes[value] = data[value]

        if post_changes == {}:
            raise MissingPropertyError

        if not check_necessary_info(data, new_necessary_info, info_type):
            raise WrongValueError

        date = datetime.now()
        date = date.strftime("%d/%m/%Y %H:%M:%S")
        post_changes["last_update"] = date

        try_to_change = db.posts.update_one({"id": id}, {"$set": post_changes})

        if try_to_change.matched_count == 0:
            raise ContentNotFound
        
        changed_post = db.posts.find_one({"id": id})

        del changed_post["_id"]

        return jsonify(changed_post), 200

    except MissingPropertyError:
        return jsonify({"error": "title, author, tags or content is necessary"}), 400

    except WrongValueError:
        resp = {"wrong fields": []}

        for value in necessary_info:
            data_value = data.get(value)
            data_value_type = get_type(data_value)

            if not data_value:
                pass

            elif data_value_type != info_type[value]:
                resp["wrong fields"].append({value: data_value_type})

            elif data_value_type == "list" and check_tags(data_value):
                resp["wrong fields"].append({value: data_value})

        return jsonify(resp), 400

    except ContentNotFound:
        return jsonify({"error": "Id not found"}), 404