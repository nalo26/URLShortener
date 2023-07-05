import enum

from flask_login import UserMixin

from . import db


class Level(enum.Enum):
    READ = "read"
    WRITE = "write"


class Access(UserMixin, db.Model):
    __tablename__ = "access"
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Enum(Level), nullable=False, default=Level.READ)
    token = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    last_access = db.Column(db.DateTime)
