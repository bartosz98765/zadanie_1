from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UUID
from uuid_extensions import uuid7

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    return db


class Tag(db.Model):

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    name = db.Column(db.String(256), unique=False, nullable=False)

    def __repr__(self):
        return f"Tag o id: {self.id} nazwa: {self.name}>"
