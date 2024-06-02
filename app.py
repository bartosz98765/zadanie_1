from http import HTTPStatus

from flask import request, url_for, make_response, Flask
from flask_smorest import Api, Blueprint

from db import init_db, Tag
from settings import (
    INVALID_DATA_FORMAT_ERROR,
    TAG_DOES_NOT_EXIST_ERROR,
)
from tag_schema import TagRequestSchema, TagSchema, TagIdSchema


class Config:
    API_TITLE = "TAGS"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    SQLALCHEMY_DATABASE_URI = "sqlite:///tags.db"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    api = Api(app)

    db = init_db(app)

    tags_app = Blueprint("tags", __name__, url_prefix="/v1")

    @tags_app.route("/tags/<tag_id>/", methods=["GET"])
    @tags_app.response(HTTPStatus.OK, TagSchema)
    def get_tag(tag_id: str):
        __validate_tag(tag_id)
        tag = db.get_or_404(Tag, tag_id)
        return {"id": tag.id, "name": tag.name}

    def __validate_tag(tag_id):
        TagIdSchema().validate({"id": tag_id})

    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def tag_does_not_exist_handler(error):
        return make_response(TAG_DOES_NOT_EXIST_ERROR, HTTPStatus.NOT_FOUND)

    @tags_app.route("/tags/", methods=["POST"])
    @tags_app.response(HTTPStatus.OK, TagSchema)
    def add_tag():
        tag_data = TagRequestSchema().load(request.json)
        tag = Tag(name=tag_data["name"])
        db.session.add(tag)
        db.session.commit()

        uri = url_for("tags.get_tag", tag_id=tag.id, _external=True)
        return {"id": tag.id, "name": tag.name}, {"Location": uri}

    @app.errorhandler(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    def invalid_tag_post_request_data_format_handler(error):
        return make_response(INVALID_DATA_FORMAT_ERROR, HTTPStatus.METHOD_NOT_ALLOWED)

    @tags_app.route("/tags/<tag_id>/", methods=["DELETE"])
    @tags_app.response(HTTPStatus.NO_CONTENT)
    def delete_tag(tag_id: str):
        __validate_tag(tag_id)
        if tag := db.session.get(Tag, tag_id):
            db.session.delete(tag)
            db.session.commit()

    api.register_blueprint(tags_app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
