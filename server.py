"""Camp Buddy"""
from datetime import datetime
from jinja2 import StrictUndefined 


from flask import Flask, render_template, redirect, request, flash, session, jsonify, abort

from flask_debugtoolbar import DebugToolbarExtension

from model import User, ProfilePage, Question, Comment, Vote, connect_to_db, db

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
    #datime.now and store to a variable
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    age = int(request.form["age"])
    city = request.form["city"]
    state = request.form["state"]
    boot_camp_name = request.form["boot_camp_name"]

    if User.query.filter(User.email == email).all():
        flash('You are already a user!')
        return render_template("log_in.html")

    elif User.query.filter(User.username == username).all():
        flash('That username is taken!')
        return render_template("register_form.html")

    else:
        
        flash('You were successfully logged in')
    
        new_user = User(username=username, email=email, password=password, age=age, city=city, state=state, boot_camp_name=boot_camp_name)
        db.session.add(new_user)
        db.session.commit()


        profile = ProfilePage(user_id=new_user.user_id, about_me="", image_url="http://cdn.someecards.com/posts/cat-banana-year-of-the-monkey-costume-tY9.jpg", linkedin_url="", github_url="")
        
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
    profile.about_me = request.form.get("about_me")
    profile.image_url = request.form.get("image_url")
    profile.linkedin_url = request.form.get("linkedin_url")
    profile.github_url = request.form.get("github_url")


    db.session.commit()

    profile_info = {
        "email":user.email,
        "age" : user.age, 
        "city" : user.city,
        "boot_camp_name" : user.boot_camp_name,
        "about_me" : profile.about_me,
        "image_url" : profile.image_url,
        "linkedin_url" : profile.linkedin_url,
        "github_url" : profile.github_url

    }
    

    return redirect("/users/%s" % user.user_id)

@app.route('/view-profile')
def view_profile():
    """Allows user to view their profile"""
    user = User.query.get(session["user_id"])
    profile = user.user_profile

    return render_template("view_profile_page.html", user=user, profile=profile)



#question 
#instantiate question when created, question route
#todo get question running for render template and do modal later
#make a notification whenever a question is answered 
#allow user acces to their own question
@app.route("/ask_question", methods=['POST'])
def ask_question():
    """Allows user to ask questions and post to forum"""

    ask = Question(user_id = session["user_id"], question = "")
    user = User.query.get(session["user_id"])

    db.session.add(ask)
    db.session.commit()

    ask.question = request.form.get("question")
    db.session.commit()

    return redirect("/users/%s" % user.user_id)

@app.route("/view_questions")
def view_questions():
    """Allows user to view previously asked questions"""
    user_id = session.get("user_id")
    if user_id:
        questions = Question.query.filter_by(user_id = user_id).all()

    return render_template("question_list.html", questions = questions)


@app.route("/add-comment", methods=['POST'])
def add_comment():
    
    comment = request.form.get("comment")
    question_id = request.form.get("question_id")

    commented_item = Comment(user_id = session["user_id"], comment_timestamp = datetime.now(), question_id = question_id, comment = comment, up_vot= 0, down_vote = 0) 
    db.session.add(commented_item)
    db.session.commit()

    result = {'comment_id': commented_item.comment_id}

    print result

    return jsonify(result)


@app.route("/question_and_comment/<int:question_id>")
def view_question_comments(question_id):
    ask = Question.query.get(question_id) 

    return render_template("question_and_comment.html", ask=ask)


@app.route("/add_vote/<int:comment_id>", methods=['POST'])
def add_vote(comment_id):

    direction = request.form.get("direction")
    comment = Comment.query.get(comment_id)
    if direction == "up":
        comment.up_vote += 1
    elif direction == "down":
        comment.down_vote += 1
    else: 
        abort(400)

    vote = Vote(user_id = session["user_id"], up_vote=up_vote, comment_id=comment_id)
    db.session.add(vote)
    db.session.commit()

    # return "vote counted"
    retu































if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()