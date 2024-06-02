from http import HTTPStatus

from flask import Flask, request, url_for, abort, make_response
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields, validate, ValidationError

from db import init_db, Tag

app = Flask(__name__)
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_app.db"

api = Api(app)
tags_app = Blueprint("tags", __name__, url_prefix="/v1")

db = init_db(app)

# Nazwa musi składać się z jednego lub więcej słów w skład których wchodza jedynie litery i cyfry
TAG_NAME_VALIDATION_REGEX = "^[\w\d](?:\s?[\w\d])*$"
INVALID_TAG_NAME_ERROR = {
    "code": "invalid_tag_name",
    "type": "https://127.0.0.1/v1/docs/problem-details/invalid_tag_name",
    "detail": "Nieprawna nazwa taga. Nazwa musi składać się z jednego lub więcej słów w skład których wchodza jedynie litery i cyfry.",
    "status": HTTPStatus.BAD_REQUEST,
}


class TagSchema(Schema):
    id = fields.UUID()
    name = fields.String()


@tags_app.route("/tags/<tag_id>/", methods=["GET"])
@tags_app.response(HTTPStatus.OK, TagSchema)
def get_tag(tag_id: str):
    tag = db.get_or_404(Tag, tag_id)
    return {"id": tag.id, "name": tag.name}


class TagRequestSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Regexp(regex=TAG_NAME_VALIDATION_REGEX),
    )

    def handle_error(self, exc, data, **kwargs):
        raise abort(make_response(INVALID_TAG_NAME_ERROR, HTTPStatus.BAD_REQUEST))


@tags_app.route("/tags/", methods=["POST"])
@tags_app.arguments(TagRequestSchema, location="json")
@tags_app.response(HTTPStatus.OK, TagSchema)
def add_tag(data: dict):
    name = data["name"]
    tag = Tag(name=name)
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


api.register_blueprint(tags_app)

if __name__ == "__main__":
    app.run()
