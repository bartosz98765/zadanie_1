from http import HTTPStatus

from flask import Flask, request, url_for
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields

from db import init_db, Tag

app = Flask(__name__)
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_app.db"

api = Api(app)
name_app = Blueprint("tags", __name__, url_prefix="/v1")

db = init_db(app)


class TagSchema(Schema):
    id = fields.UUID()
    name = fields.String()


@name_app.response(HTTPStatus.OK, TagSchema)
@name_app.route("/tags/<tag_id>/", methods=["GET"])
def get_tag(tag_id: str):
    tag = db.get_or_404(Tag, tag_id)
    return {"id": tag.id, "name": tag.name}


@name_app.route("/tags/", methods=["POST"])
@name_app.response(HTTPStatus.OK, TagSchema)
def add_tag():
    name = request.json.get("name")
    if name:
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()

    uri = url_for("tags.get_tag", tag_id=tag.id)

    return {"id": tag.id, "name": tag.name}, {"Location": uri}


@name_app.route("/tags/<tag_id>/", methods=["DELETE"])
@name_app.response(HTTPStatus.NO_CONTENT)
def delete_tag(tag_id: str):
    tag = db.session.get(Tag, tag_id)
    db.session.delete(tag)
    db.session.commit()


api.register_blueprint(name_app)

if __name__ == "__main__":
    app.run()
