import os

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

# Achieve data from DATABASE
def main():
    books = db.execute(" SELECT isbn, title, author, public_year FROM books WHERE public_year = '2000'").fetchall()
    #for books in books:
        #print(f"{books.isbn}, {books.title}, {books.author}, {books.public_year}")
if __name__=="__main__":
    main()

@app.route("/")
def index():
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("index.html", books=books)

@app.route("/result", methods=["POST"])
def result():
    """Search the Book."""
    # Get from information
    author = request.form.get("name")
    # Make sure the book is exists.
    if db.execute("SELECT * FROM books WHERE author = :author", {"author": author}).rowcount == 0:
        return render_template("error.html", message="No book with this id.")
    result = db.execute("SELECT * FROM books WHERE author = :author", {"author": author}).fetchall()
    db.commit()

    return render_template("result.html", books=result)

@app.route("/books")
def books():
    """Lists all books."""
    books=db.execute("SELECT * FROM books").fetchall()
    return render_template("books.html", books=books)

@app.route("/books/<int:book_id>")
def book(book_id):
    """Lists information about a single book"""
    # Make sure the book is exists.
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    if book is None:
        return render_template("error.html", message="No such book.")
    return render_template("book.html", book=book)




# @app.route("/<string:name>")
# def hello(name):
#     return f"<h1>Hello,{name}!</h1>"

@app.route("/names")
def names():
    names = ["Alice", "Bob", "Charlie"]
    return render_template("index.html", names=names)

@app.route("/more")
def more():
    return render_template("more.html")

@app.route("/signup", methods=["POST"])
def signup():
    name = request.form.get("name")
    return render_template("signup.html", name=name)


@app.route("/signup", methods=["GET","POST"])
def signup():
    # Login and signup
    # Get from information
    username = request.form.get("username")
    # Login and signup
    if session.get("usernames") is None:
        session["usernames"] = []
    if request.method == "POST":
        username = request.form.get("username")
        session["usernames"].append(username)
    return render_template("login.html", usernames=session["usernames"])

    # Make sure the book is exists.
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 0:
        return render_template("error.html", message="Username not exist, please sign up")
    db.execute("INSERT INTO users(username) VALUES (:username)",
    {"username": username})
    db.commit()
    # mycursor = db.cursor()
    # sql = "SELECT * FROM boos WHERE isbn = %s"
    # mycursor.execute(sql, isbn)
    # mycursor.commit()
    return render_template("success.html")
