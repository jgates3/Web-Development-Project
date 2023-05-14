from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_login import current_user, login_user, login_required, logout_user
import datetime
from datetime import date
import os
import hashlib
import json

URL = "http://127.0.0.1:5000/"
DB_NAME = "data.sqlite"
SALT = "r69u1811ok"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
app.config["FLASK_ADMIN_SWATCH"] = "cerulean" # Admin page theme
app.secret_key = "notSoSecretKey"
db = SQLAlchemy(app)

# Create admin instance
admin = Admin(app, name="Admin View", template_mode="bootstrap3")

# Create login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# TABLES
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique = True)
    full_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    user_password = db.Column(db.String, nullable=False)
    followers = db.Column(db.Integer, nullable = False, default = 0)

    def get_id(self):
        # Returns unicode that uniquely identidies the user. 
        return self.id

    def is_authenticated(self):
        # Returns true if user has provided valid credientials.
        return True

    def is_active(self):
        # Returns true if user's account has been authenticated and activated.
        return True

    def is_anonymous(self):
        # Returns true if user is anonymous.
        return False
    
    def setterpassword(self, p):
        # Salts password and encodes it using SHA256. Then stores the hased password.
        p += SALT
        self.user_password = hashlib.sha256(p.encode()).hexdigest()

    @hybrid_property
    def password(self):
        # Hybrid_property decorator allows expressions to work for python and SQL.
        return self.user_password

    @password.setter
    def password(self, p):
        # Salts password and encodes it using SHA256. Then stores the hased password.
        p += SALT
        self.user_password = hashlib.sha256(p.encode()).hexdigest()

    def checkPassword(self, p):
        # Checks if password matches the stored password.
        p += SALT
        return self.user_password == hashlib.sha256(p.encode()).hexdigest()

    def __repr__(self):
        return "<Users %r>" % self.full_name

class Follows(db.Model):
    __tablename__ = "follow"
    id = db.Column(db.Integer, primary_key=True, unique = True)
    name_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String, nullable = False)
    id_following = db.Column(db.Integer, nullable = False)
    name_following = db.Column(db.String, nullable = False)
        

    def __repr__(self):
        return "%r" % self.name

class Posts(db.Model):
    __tablename__ = "Posts"
    id = db.Column(db.Integer, primary_key=True, unique = True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    owner_name = db.Column(db.String, nullable = True)
    post_desc = db.Column(db.String,nullable = False)
    likes = db.Column(db.Integer, nullable = False, default = 0)
    dislikes = db.Column(db.Integer, nullable = False, default = 0)
    pics = db.Column(db.String, nullable = True)
    dates = db.Column(db.Integer, nullable = True)

class Dislikes(db.Model):
    __tablename__ = "Dislikes"
    id = db.Column(db.Integer, db.ForeignKey("Posts.id"), primary_key=True)
    d_username = db.Column(db.String, nullable = False)
    
class Likes(db.Model):
    __tablename__ = "Likes"
    id = db.Column(db.Integer, db.ForeignKey("Posts.id"), primary_key=True)
    l_username = db.Column(db.String, nullable = False)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable = False)
    user_comment = db.Column(db.String, nullable=False)
    date = db.Column(db.Integer, nullable=True)
    post_id = db.Column(db.String, nullable = True) 
    owner_id = db.Column(db.Integer, nullable = False)
    owner_name = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer, nullable = False, default = 0) #might be too complex but scrappable if needed
    dislikes = db.Column(db.Integer, nullable = False, default = 0)

class Shares(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable = False)
    user_name = db.Column(db.String, nullable=False)
    post_id = db.Column(db.String, nullable = True) 
    owner_id = db.Column(db.Integer, nullable = False)
    owner_name = db.Column(db.String, nullable=False)


# CUSTOM MODEL VIEWS
class UsersView(ModelView):
    # Password will display hashed password.
    form_columns = ("id", "full_name", "username", "password","followers") 
    column_searchable_list = ["username", "full_name"]
    can_export = True

class FollowsView(ModelView):
    can_export = True

class PostsView(ModelView):
    can_export = True

class LikesView(ModelView):
    can_export = True

class DislikesView(ModelView):
    can_export = True

class CommentsView(ModelView):
    can_export = True

class SharesView(ModelView):
    can_export = True
# FUNCTIONS--------------------------------------------------------------------------
# login/logout-----------------------------------------------------------------------
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    u = request.json["username"]
    p = request.json["password"]

    user = Users.query.filter_by(username=u).first()
    if not user or not user.checkPassword(p):
        # Redirect to login if user does not exist or typed incorrect password.
        return redirect(url_for("login"))

    #login
    login_user(user)
    return redirect(url_for("userView"))

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/user")
@login_required
def userView():
    return render_template("user.html")

@app.route("/register")
def registerView():
    return render_template("register.html")

@app.route("/postPage")
def postView():
    return render_template("post.html")

@app.route("/loadPostPage",methods=["GET"])
def loadPostPage():
    return redirect(url_for("postView"))

@app.route("/loadUser",methods=["GET"])
def loadUserView():
    return redirect(url_for("userView"))


#Display List Functions(not tested)---------------------------------------------
@app.route("/getallpost", methods = ["GET"])
@login_required
def allposts():
    data = []
    results = Posts.query.all()
    print(results)
    for result in results:
        data2 = []
        comments = Comments.query.filter_by(post_id = result.id)
        for comment in comments:
            commenter = Users.query.filter_by(id = comment.user_id).first()
            data2.append({"Commenter": commenter.username,
            "Comment": comment.user_comment,
            "Date": str(comment.date)})
        
        if result.pics =="":
            result.pics = 0
        data.append({
        "Id": result.id,
        "Poster":result.owner_name,
        "Picture": result.pics,
        "Description": result.post_desc, 
        "Likes":result.likes, 
        "Dislikes": result.dislikes,
        "Date": result.dates,
        "Comments": data2})
    print(data)
    return json.dumps(data)

@app.route("/followpost", methods = ["GET"])
@login_required
def followposts():
    user_id = current_user.id
    data = []
    infos = Follows.query.filter_by(name_id = user_id).all()              #get all ppl the user is following
    #print(infos)
    for info in infos:                                                        #for each person followed
        posts = Posts.query.filter_by(owner_id = info.id_following).all()      #query their posts

        for post in posts:                                                  #for every post in every person followed
            data2 = []
            comments = Comments.query.filter_by(post_id = post.id)
            for comment in comments:
                commenter = Users.query.filter_by(id = comment.user_id).first()
                data2.append({"Commenter": commenter.username,
                "Comment": comment.user_comment,
                "Date": str(comment.date)})
            if post.pics =="":
                post.pics = 0
            data.append({
            "Id": post.id,                                                  #compile into list and send
            "Poster": post.owner_name,
            "Picture": post.pics,
            "Description": post.post_desc,
            "Likes": post.likes,
            "Dislikes": post.dislikes,
            "Date": post.dates,
            "Comments":data2})
    print(data)
    return json.dumps(data)

@app.route("/myPost", methods = ["GET"])
@login_required
def myposts():
    user_id = current_user.id
    results = Posts.query.filter_by(owner_id = user_id).all()

    list = []
    for result in results:
        data2 = []
        comments = Comments.query.filter_by(post_id = result.id)
        for comment in comments:
            commenter = Users.query.filter_by(id = comment.user_id).first()
            data2.append({"Commenter": commenter.username,
            "Comment": comment.user_comment,
            "Date": str(comment.date)})
        if result.pics =="":
            result.pics = 0
        list.append({
        "Id": result.id,
        "Poster":result.owner_name,
        "Picture": result.pics,
        "Description": result.post_desc, 
        "Likes":result.likes, 
        "Dislikes": result.dislikes,
        "Date": result.dates,
        "Comments": data2})
    print(list)
    return json.dumps(list)

@app.route("/getshared", methods = ["GET"])
@login_required
def getshared():

    data = []
    s_posts =  Shares.query.all()      #get all shared post
    for s_post in s_posts:  #for all  shared posts
        posts = Posts.query.filter_by(id = s_post.post_id)
        for post in posts:
            data2 = []
            comments = Comments.query.filter_by(post_id = post.id)      #get their comments
            for comment in comments:
                commenter = Users.query.filter_by(id = comment.user_id).first()
                data2.append({"Commenter": commenter.username,
                "Comment": comment.user_comment,
                "Date": str(comment.date)})
            data.append({                                           #append everything
            "Id": post.id,                                                  
            "Poster": post.owner_name,
            "Picture": post.pics,
            "Description": post.post_desc,
            "Likes": post.likes,
            "Dislikes": post.dislikes,
            "Date": post.dates,
            "SharingPerson":s_post.user_name,
            "Comments":data2})
    print(data)
    return json.dumps(data)           



#Post Functions(not tested)------------------------------------------------------
@app.route("/newUser", methods = ["POST"])
def newUser():
    fullname = request.json["fullname"]
    username2 = request.json["username2"]
    password = request.json["password2"]

    add = Users(full_name = fullname, username = username2, user_password = password, followers = 0)
    db.session.add(add)
    salt = Users.query.filter_by(full_name = fullname).first()
    Users.setterpassword(salt,salt.user_password)
    db.session.commit()
    print("added!")
    return redirect(url_for("login"))




@app.route("/dislike", methods = ["POST"])
@login_required
def dislike():
    user_id = current_user.id
    p_id = request.json["Id"]

    user_info = Users.query.filter_by(id = user_id).first()
    check = Dislikes.query.filter_by(id = p_id, d_username = user_info.username).first()
    post = Posts.query.filter_by(id = p_id).first()

    if user_id == post.owner_id:
        return json.dumps("You can't dislike your own post!")
    if not check:
        add = Dislikes(id = p_id, d_username = user_info.username)
        db.session.add(add)
        post.dislikes = post.dislikes + 1
        db.session.commit()
        return json.dumps("Disliked the Post!") 
    else:
        db.session.delete(check)
        post.dislikes = post.dislikes - 1
        db.session.commit()
        return json.dumps("Removed Disliking the Post")     

@app.route("/like", methods = ["POST"])
@login_required
def like():
    user_id = current_user.id
    p_id = request.json["Id"]

    user_info = Users.query.filter_by(id = user_id).first()
    check = Likes.query.filter_by(id = p_id, l_username = user_info.username).first()
    post = Posts.query.filter_by(id = p_id).first()

    if user_id == post.owner_id:
        return json.dumps("You can't like your own post!")

    if not check:
        add = Likes(id = p_id, l_username = user_info.username)
        db.session.add(add)
        post.likes = post.likes + 1
        db.session.commit()
        return json.dumps("Liked the Post!") 
    else:
        db.session.delete(check)
        post.likes = post.likes - 1
        db.session.commit()
        return json.dumps("Removed Liking the Post")    

@app.route("/follow", methods = ["POST","DELETE"])
@login_required
def follow():

    user_id = current_user.id
    usernamef = request.json["name"]
    print(user_id)
    print(usernamef)

    info = Users.query.filter_by(id = user_id).first()
    info2 = Users.query.filter_by(username = usernamef).first()
    check = Follows.query.filter_by(name_following = usernamef,name = info.username).first()
    

    if info.id == info2.id:
        return json.dumps("You can't follow yourself!")

    
    if not check:
        add = Follows(name_id = info.id, name = info.username, id_following = info2.id, name_following = info2.username)
        db.session.add(add)
        info2.followers = info2.followers + 1
        db.session.commit()
        return json.dumps("Now Following!") #have code in js file where if response text greateer than 0, highlight dislike button
    else:
        db.session.delete(check)
        info2.followers = info.followers - 1
        db.session.commit()
        return json.dumps("Now Unfollowing!")    #have else statement where highlighted button is no longer highlighted

@app.route("/createPost", methods = ["POST"])
@login_required
def create():
    user_id = current_user.id
    pic = request.json["pic"]
    desc = request.json["desc"]
    today = date.today()
    #print(user_id)
    #print(pic)
    #print(desc)
    info = Users.query.filter_by(id = user_id).first()
    add = Posts(owner_id = info.id, owner_name = info.username, post_desc = desc, likes = 0, dislikes = 0, pics = pic, dates = today)
    db.session.add(add)
    db.session.commit()
    return json.dumps("Success!")

@app.route("/deletepost", methods = ["DELETE"])
@login_required
def delete():
    p_id = request.json["id"]
    delete = Posts.query.filter_by(id = p_id).first()
    db.session.delete(delete)
    deletes2 = Comments.query.filter_by(post_id = p_id).all()
    if deletes2:
        for delete2 in deletes2:
            db.session.delete(delete2)
    else:
        delete2 = ""
    db.session.commit()
    return json.dumps("Delete Success!")

@app.route("/sharepost",methods = ["POST", "DELETE"])
@login_required
def sharepost():
    p_id = request.json["id"]
    u_id = current_user.id
    checker = Shares.query.filter_by(user_id = u_id,post_id = p_id).first()
    
    if not checker:
        u_info = Users.query.filter_by(id = u_id).first()
        p_info = Posts.query.filter_by(id = p_id).first()

        add = Shares(user_id = u_info.id, user_name = u_info.username, post_id = p_info.id, owner_id = p_info.owner_id, owner_name = p_info.owner_name)
        db.session.add(add)
        db.session.commit()
        return json.dumps("Post Shared!")
    else:
        db.session.delete(checker)
        db.session.commit()
        return json.dumps("Post Unshared!")




@app.route("/addComment", methods = ["POST"])
@login_required
def addComment():
    user_i = current_user.id
    post_id = request.json["Id"]
    comment = request.json["comment"]
    user_info = Users.query.filter_by(id = user_i).first()
    poster_info = Posts.query.filter_by(id = post_id).first()
    today = date.today()
    

    add = Comments(user_id = user_info.id, user_comment = comment,date = today, post_id = poster_info.id, owner_id = poster_info.owner_id, owner_name = poster_info.owner_name)
    db.session.add(add)
    db.session.commit()
    return json.dumps("Comment Added!")


    



# Driver code
if __name__ == "__main__":
    # Add administrative views
    admin.add_view(UsersView(Users, db.session))
    admin.add_view(FollowsView(Follows, db.session))
    admin.add_view(PostsView(Posts, db.session))
    admin.add_view(DislikesView(Dislikes, db.session))
    admin.add_view(LikesView(Likes, db.session))
    admin.add_view(CommentsView(Comments, db.session))
    admin.add_view(SharesView(Shares, db.session))

    # If tables are not made, create them.
    with app.app_context():
        db.create_all()
    app.run(debug=True)