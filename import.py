import os
import csv

from flask import Flask, session, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
#db.create_all()
# Achieve data from DATABASE
def main():
    f = open("books2.csv")
    reader = csv.reader(f)
    for id, isbn, title, author, public_year in reader:
        db.execute("INSERT INTO  books(id, isbn, title, author, public_year) VALUES (:id, :isbn, :title, :author, :public_year)",
        {"id": id, "isbn": isbn, "title": title, "author": author, "public_year": public_year})
    print(f"Added {id} {isbn} {title} {author} {public_year}")
    db.commit()

if __name__=="__main__":
    main()
