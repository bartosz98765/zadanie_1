from http import HTTPStatus

from flask import make_response, abort
from marshmallow import Schema, fields, validate

from settings import TAG_NAME_VALIDATION_REGEX, INVALID_TAG_NAME_ERROR, INVALID_TAG_ID_ERROR


class TagRequestSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Regexp(regex=TAG_NAME_VALIDATION_REGEX),
    )

    def handle_error(self, exc, data, **kwargs):
        raise abort(make_response(INVALID_TAG_NAME_ERROR, HTTPStatus.BAD_REQUEST))


class TagSchema(Schema):
    id = fields.UUID()
    name = fields.String()


class TagIdSchema(Schema):
    id = fields.UUID(required=True)

    def handle_error(self, exc, data, **kwargs):
        raise abort(make_response(INVALID_TAG_ID_ERROR, HTTPStatus.BAD_REQUEST))