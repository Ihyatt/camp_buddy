"""Models and database functions for Camp Buddy project"""

import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


##############################################################################
#Model definitions 

class User(db.Model):
    """User login info for Camp Buddy"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(100), nullable=True)
    member_since = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(70), nullable=True)
    password = db.Column(db.String(70), nullable=True)
    age = db.Column(db.Integer, nullable = True)
    city = db.Column(db.String(15), nullable = True)
    state = db.Column(db.String(15), nullable = True)
    boot_camp_name = db.Column(db.String(200), nullable=True)
    languages = db.Column(db.String(1000), nullable=True)
    linkedin_url = db.Column(db.String(200), nullable=True)
    github_url = db.Column(db.String(200), nullable=True)

    user_profile = db.relationship('ProfilePage', uselist=False, backref=db.backref("users"))

    def question_count(self):
        count = 0 
        for question in self.questions:
            count += 1
        return count

    def comment_count(self):
        count = 0 
        for comment in self.comments:
            count += 1
        return count


    def __repr__(self):
        return "<User user_id=%s username=%s email=%s age=%s city=%s state=%s boot_camp_name=%s>" % (
            self.user_id, self.username, self.email, self.age, self.city, self.state, self.boot_camp_name)


##############################################################################

class ProfilePage(db.Model):
    """Profile page info"""

    __tablename__ = "profile_pages"

    profile_page_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):
        return "<ProfilePage profile_page_id=%s user_id=%s linkedin_url=%s github_url=%s>" % (
            self.profile_page_id, self.user_id, self.linkedin_url, self.github_url)


##############################################################################
class Image(db.Model):
    """points to direction of users image"""
    __tablename__ = "images"

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    image = db.Column(db.String(1500), nullable=True)

    user = db.relationship("User", backref=db.backref("images"))

##############################################################################


class Note(db.Model):
    """Allows user to keep and review study notes written"""

    __tablename__ = "notes"

    note_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    title_note = db.Column(db.String(1500), nullable=True)
    note_created = db.Column(db.String(100), nullable=True)
    note = db.Column(db.String(1500), nullable=True)
   

    user = db.relationship('User', backref="notes")

    def __repr__(self):
        return "Note note_id=%s user_id=%s note=%s" % (self.note_id, self.user_id, self.note)

##############################################################################


class Question(db.Model):
    """Question page information"""

    __tablename__ = "questions"

    question_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    title_question = db.Column(db.String(1000), nullable=True)
    question_created = db.Column(db.String(100), nullable=True)
    question = db.Column(db.String(1000), nullable=True)
    

    user = db.relationship('User', backref="questions")


    
    def __repr__(self):
        return "<Question question_id=%s user_id=%s question=%s>" % (self.question_id, self.user_id, self.question)

##############################################################################

class Comment(db.Model):
    """Comment information"""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) #user replying to question
    comment_timestamp = db.Column(db.String(100), nullable=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    comment = db.Column(db.String(1000), nullable=True)
    vote = db.Column(db.Integer)
    

    question = db.relationship("Question", backref=db.backref("comments"))
    #comments is everythin in comment table from question instance

    user = db.relationship('User', backref = db.backref('comments'))

    def __repr__(self):
        return "<Comment comment_id=%s user_id=%s comment_timestamp=%s question_id=%s comment=%s>" % (
            self.comment_id, self.user_id, self.comment_timestamp, self.question_id, self.comment) 



##############################################################################

 #Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///camp_buddy' 
    db.app = app
    db.init_app(app)


if __name__ == "__main__": 

    from server import app
    connect_to_db(app)
    print "Connected to DB."





