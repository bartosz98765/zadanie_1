from http import HTTPStatus

from db import Tag, db
from settings import (
    INVALID_TAG_ID_ERROR,
    TAG_DOES_NOT_EXIST_ERROR,
    INVALID_TAG_NAME_ERROR,
    INVALID_DATA_FORMAT_ERROR,
)


def create_tag(tag_name, session):
    tag = Tag(name=tag_name)
    session.add(tag)
    session.commit()
    return tag


def test_get_tag_returns_tag_when_exist(client):
    tag = create_tag("Testowy tag", db.session)
    url = f"/v1/tags/{tag.id}/"

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert response.json["id"] == tag.id
    assert response.json["name"] == tag.name


def test_get_tag_returns_bad_request_when_invalid_tag_id(client):
    tag_id = "0665ca92-invalid-tag-id"
    url = f"/v1/tags/{tag_id}/"

    response = client.get(url)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == INVALID_TAG_ID_ERROR


def test_get_tag_returns_not_found_when_tag_not_exist(client):
    tag_id = "0665ca92-4695-75a3-8000-f6494aef40c6"
    url = f"/v1/tags/{tag_id}/"

    response = client.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == TAG_DOES_NOT_EXIST_ERROR


def test_add_tag_successfully(client):
    tag_name = "Poprawna 111 nazwa taga22"
    url = "/v1/tags/"

    response = client.post(url, json={"name": tag_name})

    tag = db.session.query(Tag).filter_by(name=tag_name).first()
    assert response.status_code == HTTPStatus.OK
    assert tag.name == tag_name
    assert response.json["id"] == tag.id
    assert response.headers["Location"] == f"http://localhost/v1/tags/{tag.id}/"


def test_add_tag_returns_bad_request_when_invalid_tag_name(client):
    tag_name = "Tag z  niedozwolonymi #$%#   znakami  "
    url = "/v1/tags/"

    response = client.post(url, json={"name": tag_name})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == INVALID_TAG_NAME_ERROR


def test_add_tag_returns_method_not_allowed_when_data_not_json_format(client):
    tag_name = "Poprawny tag"
    url = "/v1/tags/"

    response = client.post(url, data={"name": tag_name})

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert response.json == INVALID_DATA_FORMAT_ERROR


def test_delete_tag_successfully(client):
    tag = create_tag("Testowy tag", db.session)
    url = f"/v1/tags/{tag.id}/"

    response = client.delete(url)

    assert response.status_code == HTTPStatus.NO_CONTENT
    tag_in_repository = db.session.get(Tag, tag.id)
    assert tag_in_repository is None

