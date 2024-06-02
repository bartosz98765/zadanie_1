from http import HTTPStatus

from db import Tag, db
from settings import INVALID_TAG_ID_ERROR, TAG_DOES_NOT_EXIST_ERROR


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
    tag_name = "Poprawna nazwa taga"
    url = f"/v1/tags/"

    response = client.post(url, json={"name": tag_name})

    tag = db.session.query(Tag).filter_by(name=tag_name).first()
    assert response.status_code == HTTPStatus.OK
    assert tag.name == tag_name
    assert response.json["id"] == tag.id
    assert response.headers["Location"] == f"http://localhost/v1/tags/{tag.id}/"
