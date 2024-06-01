from flask import Flask

from db import init_db, Tag

app = Flask(__name__)
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_app.db"

db = init_db(app)


@app.route('/tags/<tag_id>/', methods=['GET'])
def get_tag(tag_id: str):
    tag = db.get_or_404(Tag, id=tag_id)
    return f"Tag o id: {tag.id} nazwa: {tag.name}>"


if __name__ == "__main__":
    app.run()
