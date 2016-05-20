"""Models and database functions for Camp Buddy project"""

import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# psql -d camp_buddy

##############################################################################
#Model definitions 

class User(db.Model):
    """User login info for Camp Buddy"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(70), nullable=True)
    password = db.Column(db.String(70), nullable=True)
    age = db.Column(db.Integer, nullable = True)
    city = db.Column(db.String(15), nullable = True)
    state = db.Column(db.String(15), nullable = True)
    boot_camp_name = db.Column(db.String(200), nullable=True)

    user_profile = db.relationship('ProfilePage', uselist=False, backref=db.backref("users"))


    def __repr__(self):
        return "<User user_id=%s username=%s email=%s age=%s city=%s state=%s boot_camp_name=%s>" % (
            self.user_id, self.username, self.email, self.age, self.city, self.state, self.boot_camp_name)


##############################################################################

class ProfilePage(db.Model):
    """Profile page info"""

    __tablename__ = "profile_pages"

    profile_page_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    about_me = db.Column(db.String(1000), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    linkedin_url = db.Column(db.String(200), nullable=True)
    github_url = db.Column(db.String(200), nullable=True)

    

    def __repr__(self):
        return "<ProfilePage profile_page_id=%s user_id=%s about_me=%s linkedin_url=%s github_url=%s>" % (
            self.profile_page_id, self.user_id, self.about_me, self.linkedin_url, self.github_url)


##############################################################################

class Question(db.Model):
    """Comment page information"""

    __tablename__ = "questions"

    question_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    question = db.Column(db.String(1000), nullable=True)
    #when pages are rendered, do sql command to show num of comments

    user = db.relationship('User', backref="questions")
    
    def __repr__(self):
        return "<Question question_id=%s user_id=%s question=%s>" % (self.question_id, self.user_id, self.question)

##############################################################################

class Comment(db.Model):
    """Comment information"""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) #user replying to question
    comment_timestamp = db.Column(db.DateTime) #flask app will render current date and time once ran in templates through 
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    comment= db.Column(db.String(1000), nullable=True)
    # up_vote = db.column(db.Integer)
    #down_vote = db.column(db.Integer)
    

    question = db.relationship("Question", backref=db.backref("comments"))
    #make a test without question_id and keep backref
    #question gets you eerything in question table related to current comment
    #comments is everythin in comment table from question instance

    def up_vote_count(self):
        #query where commentid is = to comment id and where upvote is eqal to true and use comment to get therea and votes to get back
        count = 0 
        up_vote_count = db.session.query.filter(self.comment_id, Vote.up_vote).join(Vote).all()
        for comment_id, up_vote in up_vote_count:
            if comment_id == self.comment_id:
                if up_vote == t:
                    count += 1


        return count

    def down_vote_count(self):
        #query where commentid is = to comment id and where upvote is eqal to true and use comment to get therea and votes to get back
        count = 0 
        # down_vote_count = self.votes
        for vote in self.votes:
            if vote.up_vote is False:
                count += 1
            # if comment_id == self.comment_id:
            #     if up_vote == f:
            #         count += 1
        return count


    def __repr__(self):
        return "<Comment comment_id=%s user_id=%s comment_timestamp=%s question_id=%s comment=%s>" % (
            self.comment_id, self.user_id, self.comment_timestamp, self.question_id, self.comment) 

##############################################################################

class Vote(db.Model):
    """Vote information"""

    __tablename__ = "votes"

    vote_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) #from users table
    up_vote = db.Column(db.Boolean, nullable=True) #zeroes represent negative number
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'))

    #make backref from users table for user


    user = db.relationship("User", backref="votes")
    comment = db.relationship("Comment", backref="votes")


    def __repr__(self):
        return "<Vote vote_id=%s user_id=%s up_vote=%s comment_id=%s>" % (self.vote_id, self.user_id, self.up_vote, self.comment_id)

##############################################################################

 #Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///camp_buddy' 
    db.app = app
    db.init_app(app)


if __name__ == "__main__": ##allows you to play with data table within command line if result isn't '=='

    from server import app
    connect_to_db(app)
    print "Connected to DB."





