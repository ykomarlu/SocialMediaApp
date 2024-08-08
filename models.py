from app import db

# class Users(db.Model):
#     userId = db.Column(db.Integer, primary_key=True)
#     friendId = db.Column(db.Integer, db.ForeignKey('Friend.friendId'), nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.userId

# class Friend(db.Model):
#     friendId = db.Column(db.Integer, primary_key=True)
#     userId = db.Column(db.Integer, db.ForeignKey('Users.userId'), nullable=False)

#     def __repr__(self):
#         return '<Friend %r>' % self.friendId