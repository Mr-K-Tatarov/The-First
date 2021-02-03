import os


class SQLiteConfig:
    name = os.getenv("dbname", "db.sqlite")
    url = f"sqlite:///{name}"
