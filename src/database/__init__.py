from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

from .models import Access, Level


def create_database(db: SQLAlchemy):
    db.drop_all()
    db.create_all()

    admin = Access(level=Level.WRITE, token=generate_password_hash("$WRITER_TOKEN"))
    db.session.add(admin)

    reader = Access(level=Level.READ, token=generate_password_hash("$READER_TOKEN"))
    db.session.add(reader)

    db.session.commit()
