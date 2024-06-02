from http import HTTPStatus


from db import Tag, db


def create_tag(tag_name, db_session):
    tag = Tag(name=tag_name)
    db_session.add(tag)
    db_session.commit()
    return tag


def test_get_tag(client):
    tag = create_tag("Testowy tag", db.session)
    url = f"/v1/tags/{tag.id}/"

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
