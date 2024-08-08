from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# from models import Users, Friend

app = Flask(__name__)
# Calls on flask on the current file
# pymsql is the python equivalent of mysql jdbc
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Incantat3m@ygk-mysqldb-instance.cvwgim0iaj9b.us-east-1.rds.amazonaws.com:3306/social_media'
db = SQLAlchemy(app)
# creates a sqlalchemy object that can be used to init the table in the current file
    
class Users(db.Model):
    __tablename__ = 'Users'
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)

    # basically the constructor of the class, what I previously had was just the listing of the class instance variables but 
    # no way to create the object
    def __init__(self, userId, username):
        self.userId = userId
        self.username = username

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.userId

class Posts(db.Model):
    __tablename__ = 'Posts'
    postId = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)
    content = db.Column(db.String)
    hashtag = db.Column(db.String)
    userId = db.Column(db.Integer, db.ForeignKey('Users.userId'), nullable=False)
    likes = db.Column(db.Integer)

# need a constructor to create a new post whenever I want to insert a new post entity into the post table

    def __init__(self, postId, image, content, hashtag, userId, likes):
        self.likes = likes
        self.content = content
        self.postId = postId
        self.image = image
        self.userId = userId
        self.hashtag = hashtag

    def __repr__(self):
        return '<Posts %r>' % self.postId

class UserFriends(db.Model):
    __tablename__ = 'UserFriends'
    friendId = db.Column(db.Integer, db.ForeignKey('Users.userId'), primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('Users.userId'), primary_key=True, nullable=False)

    def __init__(self, friendId, userId):
        self.userId = userId
        self.friendId = friendId

    def __repr__(self):
        return '<Friend %r>' % self.friendI

@app.route("/", methods=["GET"])
# creates route for the default url
# Creates method that I assume gets ran when the default url is called??
def index():
    return render_template('index.html')

@app.route("/", methods=["POST"])
# creates route for the default url
# Creates method that I assume gets ran when the default url is called??
def add_user():
    # request keyword retrieves the endpoint request and the body of it to initialize user obj
    username=request.json['username']

    user = Users(username)

    db.session.add(user)
    db.session.commit()
    return "able to add user"

# delete users
@app.route("/delete/<int:userId>", methods=["DELETE"])
def deleteUsers(userId):
    # first need to retireve user entity from the table that contains the parameter as an attribute
    # What I learned: you need to query the database using the model class
    user = Users.query.get_or_404(userId)

    db.session.delete(user)
    db.session.commit()
    
    return "able to delete user"

@app.route("/add/post", methods=["POST"])
def createPost():

    # So I still need to create a instance of the Post Model and then insert it
    # see when I create a post, I need to add a post entity to the table so I need to 
    # provide all the necessary post info to create an instance

    # request.get_json returns all the json data as a dictionary
    # 
    postId = request.json['postId']
    image = request.json['image']
    content = request.json['content']
    hashtag = request.json['hashtag']
    userId = request.json['userId']
    likes = request.json['likes']

    try:
        post = Posts(postId, image, content, hashtag, userId, likes)
        # db.session.add(), it adds the post instance to the session
        db.session.add(post)
        # it adds whatever is in the session to the database
        db.session.commit()
        return "able to add post"

    except:
        return "unable to create post"

    

@app.route("/like/<int:postId>", methods=["PUT"])
def addLike(postId):
    post = "select * from post where post.postId = :postId"
    post = db.session.execute(post, {"postId": postId})
    try:
        db.session.execute("update set likes = (post.likes + 1) where (posts.postId) = id")
        text = "Post found: {} likes".format(post.likes)
        return text
    except:
        return "Post not found", 404
        
    # If I were doing this in sql within Springboot, I would 
    # i would isolate the post wit the specific post id
    # then increase the number of likes by 1 and re-insert it

    # or i think what I did for my db project was that the posts were
    # in their own table and the likes were in their own table with foreign key
    # to the post table. So I ended up 

    #Isolating a post based on postId: Select * from post where post.postid = postId;
@app.route("/unlike/<int:postId>", methods=["PUT"])
def removeLike(postId):
    post = db.session.execute("select * from post where post.postId = self.postId")
    if post is None:
        return "Post not found", 404
    if post.likes != 0:
        db.session.execute("update set likes = (post.likes - 1) where (posts.postId) = id")

# add posts and delete posts

if __name__ == "__main__":
    app.run(debug=True)


