In the shell:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
sudo -u postgres psql
```

In the postgres shell:

```sql
CREATE DATABASE url_shortener;
CREATE USER url_shortener WITH PASSWORD 'url_shortener';
ALTER TABLE url_shortener OWNER TO url_shortener;
```

Back in the shell:

```bash
echo "DATABASE_URL=postgresql://url_shortener:url_shortener@localhost:5432/url_shortener?password=url_shortener" >> .env`
python
```

In the python shell:

```py
from src import db, create_app, models
from werkzeug.security import generate_password_hash
app = create_app()
with app.app_context():
    db.create_all()
    admin = models.Access(level=models.Level.WRITE, token=generate_password_hash('admin'))
    db.session.add(admin)
    reader = models.Access(level=models.Level.READ, token=generate_password_hash('reader'))
    db.session.add(reader)
    db.session.commit()
```
