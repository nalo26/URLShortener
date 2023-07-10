#!/bin/bash

source .env
echo "Creating database $DB_NAME"

echo "DROP DATABASE IF EXISTS $DB_NAME; CREATE DATABASE $DB_NAME; ALTER DATABASE $DB_NAME OWNER TO $DB_USER;" | sudo -u postgres psql

python3 -c "from src import db, create_app, models
from werkzeug.security import generate_password_hash
app = create_app()
with app.app_context():
    db.create_all()
    admin = models.Access(level=models.Level.WRITE, token=generate_password_hash('$WRITER_TOKEN'))
    db.session.add(admin)
    reader = models.Access(level=models.Level.READ, token=generate_password_hash('$READER_TOKEN'))
    db.session.add(reader)
    db.session.commit()"
