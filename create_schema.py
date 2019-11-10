import os
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
dbModel = declarative_base()
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
#db = SQLAlchemy(app)

class User(dbModel):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    email = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    creationdate = db.Column(db.DateTime, default=datetime.now)
    events = relationship('Event', backref='owner')
    tasks = relationship('Task', backref='owner')
    blocks = relationship('Block', backref='owner')

    def __repr__(self):
            return f"<User {self.email}>"

class Event(dbModel):
    __tablename__ = "events"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    title = db.Column(db.Text)
    location = db.Column(db.Text)
    alert = db.Column(db.Boolean, default=False)
    start = db.Column(db.DateTime, index=True)
    end = db.Column(db.DateTime)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    block_id = db.Column(UUID(as_uuid=True), db.ForeignKey("blocks.id"))
    tasks = relationship('Task', backref='requiredby')

    def __repr__(self):
            return f"<Event title={self.title}, location={self.location}, start={self.start}, end={self.end}>"

class Task(dbModel):
    __tablename__ = "tasks"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    title = db.Column(db.Text)
    event_id = db.Column(UUID(as_uuid=True), db.ForeignKey("events.id"), nullable=True)
    block_id = db.Column(UUID(as_uuid=True), db.ForeignKey("blocks.id"), nullable=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))

    def __repr__(self):
            return f"<Task {self.title}>"

class Block(dbModel):
    __tablename__ = "blocks"
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    title = db.Column(db.Text)
    location = db.Column(db.Text)
    alert = db.Column(db.Boolean)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    events = relationship('Event', backref='parent')

    def __repr__(self):
            return f"<Block {self.title}>"

t = db.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
dbModel.metadata.create_all(t)


##import psycopg2
##
##exe = ["""
##CREATE TABLE Users
##(
##  user_id INT NOT NULL,
##  username VARCHAR(32) NOT NULL,
##  name TEXT NOT NULL,
##  password TEXT NOT NULL,
##  creationdate TIMESTAMP NOT NULL,
##  PRIMARY KEY (user_id),
##  UNIQUE (username)
##);
##""",
##"""
##CREATE TABLE Events
##(
##  event_id INT NOT NULL,
##  start_time TIMESTAMP NOT NULL,
##  end_time TIMESTAMP,
##  event_name INT NOT NULL,
##  send_alert INT NOT NULL,
##  owner_id INT NOT NULL,
##  PRIMARY KEY (event_id),
##  FOREIGN KEY (owner_id) REFERENCES Users(user_id)
##);
##""",
##"""
##CREATE TABLE Tasks
##(
##  task_id INT NOT NULL,
##  task_name INT NOT NULL,
##  owner_id INT NOT NULL,
##  required_by INT NOT NULL,
##  PRIMARY KEY (task_id),
##  FOREIGN KEY (owner_id) REFERENCES Users(user_id),
##  FOREIGN KEY (required_by) REFERENCES Events(event_id)
##);"""]
##
##def connect(exe):
##    try:
##        conn = psycopg2.connect("postgres://mthhzuxmhpgela:073cc8921ceeeb8a1c21b592da0b6eb2febe87daf26bfbb533478ce11369a278@ec2-54-83-33-14.compute-1.amazonaws.com:5432/d3fhnsfu3433lo")
##        cur = conn.cursor()
##
##        for i in exe:
##            cur.execute(i)
##            #print(cur.fetchone())
##        conn.commit()
##
##        out = None
##        out = cur.fetchall()
##        cur.close()
##    except (Exception, psycopg2.DatabaseError) as error:
##        print(error)
##    finally:
##        if conn is not None:
##            conn.close()
##            print('Database connection closed.')
##            return out
##
##class Id:
##	id_cols_and_tables = {"user_id": "users",
##			      "event_id": "events",
##			      "task_id": "tasks",
##			      "block_id": "blocks",
##			      "session_id": "sessions"}
##	valid_types = tuple(i for i in id_cols_and_tables.keys())
##
##	def __init__(self, int, type, db):
##		self.int = int
##		if type not in self.valid_types:
##			raise TypeError("type must be set to \"" + "\", \"".join(self.valid_types[:-1]) + "\", or \"" + self.valid_types[-1] + "\"")
##
##	def isUnique(self):
##		if self.db.cursor().execute("sadsdas") == None:
##			return True
##		return False
##
##	def generate(type, db):
##		while True:
##			output = Id(int.from_bytes(os.urandom(16), "big"), type, db)
##			if output.isUnique():
##				break
##		return output
##
##	def fromHex(hex, type, db):
##		return Id(int(hex, 16), type, db)
