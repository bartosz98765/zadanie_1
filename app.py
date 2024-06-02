from http import HTTPStatus

from flask import Flask, request, url_for, abort, make_response
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields, validate, ValidationError

from db import init_db, Tag
from settings import (
    INVALID_DATA_FORMAT_ERROR,
    TAG_NAME_VALIDATION_REGEX,
    INVALID_TAG_NAME_ERROR,
)
from tag_schema import TagRequestSchema, TagSchema

app = Flask(__name__)
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_app.db"

api = Api(app)
tags_app = Blueprint("tags", __name__, url_prefix="/v1")

db = init_db(app)


@tags_app.route("/tags/<tag_id>/", methods=["GET"])
@tags_app.response(HTTPStatus.OK, TagSchema)
def get_tag(tag_id: str):
    tag = db.get_or_404(Tag, tag_id)
    return {"id": tag.id, "name": tag.name}


@tags_app.route("/tags/", methods=["POST"])
@tags_app.response(HTTPStatus.OK, TagSchema)
def add_tag():
    tag_data = TagRequestSchema().load(request.json)
    tag = Tag(name=tag_data["name"])
    db.session.add(tag)
    db.session.commit()

    uri = url_for("tags.get_tag", tag_id=tag.id)
    return {"id": tag.id, "name": tag.name}, {"Location": uri}


@tags_app.route("/tags/<tag_id>/", methods=["DELETE"])
@tags_app.response(HTTPStatus.NO_CONTENT)
def delete_tag(tag_id: str):
    tag = db.session.get(Tag, tag_id)
    db.session.delete(tag)
    db.session.commit()


@app.errorhandler(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
def invalid_data_format_handler():
    return make_response(INVALID_DATA_FORMAT_ERROR, HTTPStatus.METHOD_NOT_ALLOWED)


api.register_blueprint(tags_app)

if __name__ == "__main__":
    app.run()
