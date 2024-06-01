from flask import Flask, request, url_for

from db import init_db, Tag

app = Flask(__name__)
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_app.db"

db = init_db(app)


@app.route("/tags/<tag_id>/", methods=["GET"])
def get_tag(tag_id: str):
    tag = db.get_or_404(Tag, tag_id)
    return f"Tag o id: {tag.id} nazwa: {tag.name}>"


@app.route("/tags/", methods=["POST"])
def add_tag():
    name = request.json.get("name")
    if name:
        p = Tag(name=name)
        db.session.add(p)
        db.session.commit()

    uri = url_for("get_tag", tag_id=p.id)

    return p.id, 200, {"Location": uri}


if __name__ == "__main__":
    app.run()
