"""Camp Buddy"""
from datetime import datetime
from jinja2 import StrictUndefined 

from flask import Flask, render_template, redirect, request, flash, session, jsonify, abort

from flask_debugtoolbar import DebugToolbarExtension

from model import User, ProfilePage, Question, Note, Comment, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def localhost():

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Shows user sign-up"""

    return render_template("register_form.html")

@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    age = int(request.form["age"])
    city = request.form["city"]
    state = request.form["state"]
    boot_camp_name = request.form["boot_camp_name"]
    languages = request.form["languages"]
    linkedin_url = request.form["languages"]
    github_url = request.form["github_url"]


    if User.query.filter(User.email == email).all():
        flash('You are already a user!')
        return render_template("log_in.html")

    elif User.query.filter(User.username == username).all():
        flash('That username is taken!')
        return render_template("register_form.html")

    else:
        
        flash('You were successfully logged in')
    
        new_user = User(username=username, member_since = datetime.now(), email=email, password=password, age=age, city=city, state=state, boot_camp_name=boot_camp_name, languages=languages, linkedin_url=linkedin_url, github_url=github_url)
        db.session.add(new_user)
        db.session.commit()


        profile = ProfilePage(user_id=new_user.user_id)
        
        db.session.add(profile)
        db.session.commit()

        user = User.query.filter_by(email=email).first()
        session["user_id"] = user.user_id

        flash("User %s added." % username)

        return redirect("/users/%s" % new_user.user_id)

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form"""

    return render_template("log_in.html")


@app.route('/login', methods=['POST'])
def login_process():
    "Process login"
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Your email is not recorded")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")

    return redirect("/users/%s" % user.user_id)


@app.route('/logout')
def logout():
    """user logout"""

    del session["user_id"]
    flash("Logged Out")

    return redirect("/login")


@app.route("/users/<int:user_id>")
def user_page(user_id):
    """Users profile"""

    user = User.query.get(user_id)
    profile = user.user_profile
    
    return render_template("profile_page.html", user=user, profile=profile)


@app.route('/edit-profile')
def view_profile():
    """Allows user to edit their profile"""
    user = User.query.get(session["user_id"])
    profile = user.user_profile

    return render_template("editable_profile_page.html", user=user, profile=profile)


@app.route("/update-profile", methods=['POST'])
def update_user_data():
    """update user data"""
    user = User.query.get(session["user_id"])
    profile = user.user_profile

    user.username = request.form.get("username")
    user.email = request.form.get("email")
    user.age = request.form.get("age")
    user.city = request.form.get("city")
    user.state = request.form.get("state")
    user.boot_camp_name = request.form.get("boot_camp_name")
    profile.languages = request.form.get("languages")
    profile.linkedin_url = request.form.get("linkedin_url")
    profile.github_url = request.form.get("github_url")
    profile.profile_image = request.files.get("profile_image")


    db.session.commit()    

    return redirect("/users/%s" % user.user_id)

@app.route("/ask_question", methods=['POST'])
def ask_question():
    """Allows user to ask questions and post to forum"""

    ask = Question(user_id = session["user_id"], title_question = "", question = "")
    user = User.query.get(session["user_id"])

    db.session.add(ask)
    db.session.commit()

    ask.title_question = request.form.get("title_question")
    ask.question = request.form.get("question")
    db.session.commit()

    return redirect("/users/%s" % user.user_id)

@app.route("/write_note", methods=['POST'])
def write_note():
    """Allows user to write study notes"""
    diary = Note(user_id=session["user_id"],title_note = "", note="")
    user = User.query.get(session["user_id"])

    db.session.add(diary)
    db.session.commit()

    diary.title_note = request.form.get("title_note")
    diary.note = request.form.get("note")
    db.session.commit()
    print "im here"

    return redirect("/users/%s" % user.user_id)



@app.route("/view_questions")
def view_questions():
    """Allows user to view previously asked questions"""
    user_id = session.get("user_id")
    skip = request.args.get('skip', 0)
    if user_id:
        questions = Question.query.filter_by(user_id = user_id).all()
        
        
        
    return render_template("question_list.html", questions = questions)


@app.route("/view_notes")
def view_notes():
    """Allows users to view past written notes"""
    user_id = session.get("user_id")

    if user_id:
        notes = Note.query.filter_by(user_id = user_id).all()

    return render_template("notes.html", notes = notes)


@app.route("/question_and_comment/<int:question_id>")
def view_question_comments(question_id):
    ask = Question.query.get(question_id) 
    
    comments = ask.comments
    comment_id = []
    for comment in comments:
        comment_id.append(comment.comment_id)
    comment_id.sort()

    comments = []
    for id in comment_id:
        comment = Comment.query.get(id)
        comments.append(comment)

    return render_template("question_and_comment.html", ask=ask, comments=comments)


@app.route("/add-comment.json", methods=['POST'])
def add_comment():
    
    comment = request.form.get("comment")
    question_id = request.form.get("question_id")

    commented_item = Comment(user_id = session["user_id"], comment_timestamp = datetime.now(), question_id = question_id, comment = comment, vote = 0) 
    db.session.add(commented_item)
    db.session.commit()

    result = {'comment_id': commented_item.comment_id, 
              'vote': commented_item.vote}


    return jsonify(result)

@app.route("/add-vote.json", methods=['GET']) # pass in comment id
def add_vote():
    """allows user to add a vote to a comment"""
    

    comment_id = request.args.get("comment_id")
    voted_item = request.args.get("voted_item")

    comment = Comment.query.get(int(comment_id))
    
    if voted_item == "up":
        comment.vote += 1


    db.session.commit()
        
    result = {'vote': comment.vote, "comment_id": comment_id}
    return jsonify(result)


    


# @app.route("/more-questions")
# def get_more_questions():
#     offset = request.args.get("offset")
#     print "OFFSET IS %s" % offset
#     # db query for actual questions, wiht limit and offset
#     return jsonify({"questions": ["what is a dictionary", "how do you make a list?"]})








if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()


