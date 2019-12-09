"""This contains the model used by the flask application and flask_sqlalchemy.

Make sure to update it if the database schema is changed.
"""
from datetime import datetime
from uuid import UUID as PythonStandardUUID

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from sqlalchemy.dialects.postgresql import UUID
from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(PythonStandardUUID(id))

# DEFINE MODELS BELOW:


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    email = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    creationdate = db.Column(db.DateTime, default=datetime.now)
    events = db.relationship('Event', backref='owner')
    tasks = db.relationship('Task', backref='owner')

    def __repr__(self):
        return f"<User {self.email}>"

    def set_password(self, password):
        db.session.query(User).get(self.id).password = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    title = db.Column(db.Text)
    location = db.Column(db.Text)
    start = db.Column(db.DateTime, index=True)
    end = db.Column(db.DateTime)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    tasks = db.relationship('Task', backref='requiredby')

    def __repr__(self):
        return f"<Event title={self.title}, start={self.start}, end={self.end}>"


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    title = db.Column(db.Text)
    link = db.Column(db.Text)
    event_id = db.Column(UUID(as_uuid=True),
                         db.ForeignKey("events.id"),
                         nullable=True)
    user_id = db.Column(UUID(as_uuid=True),
                        db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<Task {self.title}>"
