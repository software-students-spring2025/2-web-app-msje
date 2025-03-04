import pymongo
import os
import flask_login
from flask import Flask, redirect, render_template, request, url_for
from bson.objectid import ObjectId
from dotenv import load_dotenv
from users import load_user, check_user, User


app = Flask(__name__)

# from flask-login description 
# need to change this (shouldn't be hardcoded)
app.secret_key = os.getenv("SECRET_KEY")

login_manager = flask_login.LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'login'

# make a connection to the database server
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

connection = pymongo.MongoClient(mongo_uri)
db = connection["Forum"]


@login_manager.user_loader
def user_loader(user_id):
    return load_user(db, user_id)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    # user input
    username = request.form.get('username')
    password = request.form.get('password')

    # check if it taken
    valid_user = check_user(db, username, password)

    if valid_user:
        flask_login.login_user(valid_user)
        return redirect(url_for('index'))
    
    return render_template("login.html")

@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('index')) #return to index (index is public?)

@app.route("/register", methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        return render_template("create_account.html")
    
    username = request.form.get('username')
    password = request.form.get('password')

    # username is taken
    if db["users"].find_one({"username": username}):
        return render_template("create_account.html")
    new_user = {
        "username": username,
        "password": password 
    }

    user = db["users"].insert_one(new_user)

    user = User(str(user.inserted_id), username, password)
    flask_login.login_user(user)
    return redirect(url_for('index'))

# with data from database
@app.route("/")
def index():
    posts = db["posts"].find() 
    return render_template("index.html", data=posts)

# with database
@app.route("/post/<string:post_id>")
def post_detail(post_id):
    # Find the post by ID
    post = db["posts"].find_one({"_id": ObjectId(post_id)})
    if post:
        return render_template("post.html", post=post)
    else:
        return "<h1>Post Not Found</h1>", 404


@app.route("/create_post", methods = ['GET','POST'])
@flask_login.login_required
def create_post():

    user = None
    title = None
    content = None
    
    if request.method == "POST":
        # form fields the user fills out
        user = request.form.get("user")
        title = request.form.get("title")
        content = request.form.get("content")

        new_post = {
            "user": user,
            "title": title,
            "content": content,
            "comment": [] # new post will have no comments
        }

        result = db["posts"].insert_one(new_post) # add post to database

        if result.inserted_id:
            # after making a post, where should user go?
            return redirect(url_for('index')) # this can change
        else:
            # check error code?
            return "<h1>Failed to add post</h1>", 404
    
    return render_template("create_post.html") 

@app.route("/post/<string:post_id>/comment", methods=['POST'])
@flask_login.login_required
def add_comment(post_id):
    new_comment = {
        "user": flask_login.current_user.username,  # Use the current logged-in user's username
        "comment": request.form.get("content")  # Get the comment content from the form
    }

    db["posts"].update_one(
        {"_id": ObjectId(post_id)},
        {"$push": {"comment": new_comment}}
    )

    return redirect(url_for('post_detail', post_id=post_id))

@app.route("/post/<string:post_id>/edit", methods=['GET','POST'])
@flask_login.login_required
def edit_post(post_id):
    post = db["posts"].find_one({"_id": ObjectId(post_id)}) #find post (for get)

    if request.method == 'POST':
        result = db["posts"].update_one(
            {"_id": ObjectId(post_id)},
            {"$set": {
                "title": request.form.get("title"),
                "content": request.form.get("content")
            }}
        )

        if result.modified_count >= 1:
            return redirect(url_for('post_detail', post_id=post_id))
        else:
            return "<h1>Failed to edit post</h1>", 404
        
    return render_template("edit_post.html", post=post)


@app.route("/post/<string:post_id>/delete", methods=['GET', 'POST'])
@flask_login.login_required
def delete_post(post_id):
    if request.method == 'GET':
        # Show confirmation page
        post = db["posts"].find_one({"_id": ObjectId(post_id)})
        if post:
            return render_template("delete_confirmation.html", post=post)
        else:
            return "<h1>Post Not Found</h1>", 404
    else:
        # Handle the actual deletion
        db["posts"].delete_one({"_id": ObjectId(post_id)})
        return redirect(url_for('index'))

@app.route("/search")
def search():
    query = request.args.get("q", "")
    if query:
        # Search in title, content, and user fields
        results = db["posts"].find({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"content": {"$regex": query, "$options": "i"}},
                {"user": {"$regex": query, "$options": "i"}}
            ]
        })
        return render_template("search.html", results=results, query=query)
    return render_template("search.html", results=None, query=None)

if __name__ == "__main__":
    app.run(debug=True)