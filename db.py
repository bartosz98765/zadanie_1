from flask_sqlalchemy import SQLAlchemy
from uuid_extensions import uuid7str

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    return db


class Tag(db.Model):

    id = db.Column(db.String(64), primary_key=True, default=uuid7str)
    name = db.Column(db.String(256), unique=False, nullable=False)

    def __repr__(self):
        return f"Tag o id: {self.id} nazwa: {self.name}>"
