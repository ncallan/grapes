"""This is a helper program to create a database schema.

It will add all necessary tables to the database,
as defined in the db.metadata object (in this case defined in db_model.py
and imported in __init__.py). All pre-existing tables will be ignored.
"""

from app import db

print(db.metadata.tables)

db.metadata.bind = db.engine
db.metadata.create_all()
