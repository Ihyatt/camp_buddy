"""Camp Buddy"""
import os
from datetime import datetime
from jinja2 import StrictUndefined 

from flask import Flask, render_template, redirect, request, flash, session, jsonify, abort

from flask_debugtoolbar import DebugToolbarExtension

from model import User, ProfilePage, Image, Question, Note, Comment, Vote, connect_to_db, db
from werkzeug import secure_filename
import smtplib
from email.mime.text import MIMEText


UPLOAD_FOLDER = '/Users/Inashyatt1/desktop/camp-buddy/static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.secret_key = "19kittiesareawesome89"

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
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    age = int(request.form.get("age"))
    city = request.form.get("city")
    state = request.form.get("state")
    boot_camp_name = request.form.get("boot_camp_name")
    languages = request.form.get("languages")
    linkedin_url = request.form.get("languages")
    github_url = request.form.get("github_url")
    file_ = request.files.get("image-upload")
    about_user = request.form.get("about")


    if User.query.filter(User.email == email).all():
        flash('You are already a user!')
        return render_template("log_in.html")

    elif User.query.filter(User.username == username).all():
        flash('That username is taken!')
        return render_template("register_form.html")

    elif password == '':
        flash('Please type in a password')
        return render_template("register_form.html")

    elif boot_camp_name == '':
        flash('Please type in a bootcamp')
        return render_template("register_form.html")

    elif city == '':
        flash('Please type in a city')
        return render_template("register_form.html")

    elif state == '':
        flash('Please type in a state')
        return render_template("register_form.html")

    elif linkedin_url == '':
        flash('Please type in your LinkedIn address')
        return render_template("register_form.html")

    elif github_url == '':
        flash('Please type in your GitHub address')
        return render_template("register_form.html")

    elif languages == '':
        flash('Please type your skills')
        return render_template("register_form.html")

    elif about_user == '':
        flash('Please type about yourself')
        return render_template("register_form.html")

    elif email == '':
        flash('Please type in your email')
        return render_template("register_form.html")

    elif username == '':
        flash('Please type in your username')
        return render_template("register_form.html")


    else:
        
        flash('You were successfully logged in')
    
       
        if file_:
            filename = secure_filename(file_.filename)
            file_.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        


        date_string = datetime.today().strftime('%Y-%m-%d')
        user = User(username=username, member_since = date_string, email=email, password=password, age=age, city=city, state=state, boot_camp_name=boot_camp_name, languages=languages, linkedin_url=linkedin_url, github_url=github_url, about_user=about_user)
        db.session.add(user)
        db.session.commit()
      

       
        session["user_id"] = user.user_id

        user_image = Image(user_id=session["user_id"], image=filename)

        db.session.add(user_image)

        profile = ProfilePage(user_id=session["user_id"])
        
        db.session.add(profile)
        db.session.commit()


        flash("Hello %s!" % user.username)

        return redirect("/users/%s" % user.user_id)


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form"""

    return render_template("log_in.html")


@app.route('/login', methods=['POST'])
def login_process():
    "Process login"
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Your email is not recorded")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Welcome Back! %s" % user.username)

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
       
    return render_template("profile_page.html", user=user)




@app.route('/edit-profile')
def view_profile():
    """Allows user to edit their profile"""
    user_id = session.get("user_id")
    if user_id:
        user = User.query.get(session["user_id"])
       
        return render_template("editable_profile_page.html", user=user)
    else:
         return redirect("/login")


@app.route("/update-profile", methods=['POST'])
def update_user_data():
    """update user data"""


    user = User.query.get(session["user_id"])
    user_image = user.images[0]

    user.username = request.form.get("username")
    user.email = request.form.get("email")
    user.age = request.form.get("age")
    user.city = request.form.get("city")
    user.state = request.form.get("state")
    user.boot_camp_name = request.form.get("boot_camp_name")
    user.languages = request.form.get("languages")
    user.linkedin_url = request.form.get("linkedin_url")
    user.github_url = request.form.get("github_url")
    user.about_user = request.form.get("about")
    user.password = request.form.get("password")
    file_ = request.files["image-upload"]

    if password == '':
        flash('Please type in a password')
        return render_template("register_form.html")

    elif boot_camp_name == '':
        flash('Please type in a bootcamp')
        return render_template("register_form.html")

    elif city == '':
        flash('Please type in a city')
        return render_template("register_form.html")

    elif state == '':
        flash('Please type in a state')
        return render_template("register_form.html")

    elif linkedin_url == '':
        flash('Please type in your LinkedIn address')
        return render_template("register_form.html")

    elif github_url == '':
        flash('Please type in your GitHub address')
        return render_template("register_form.html")

    elif languages == '':
        flash('Please type your skills')
        return render_template("register_form.html")

    elif about_user == '':
        flash('Please type about yourself')
        return render_template("register_form.html")

    elif email == '':
        flash('Please type in your email')
        return render_template("register_form.html")

    elif username == '':
        flash('Please type in your username')
        return render_template("register_form.html")

    if file_:
            filename = secure_filename(file_.filename)
            file_.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            user_image.image = filename
            db.session.add(user_image)
    


    db.session.commit()    

    return redirect("/users/%s" % user.user_id)



@app.route("/ask_question", methods=['POST'])
def ask_question():
    """Allows user to ask questions and post to forum"""
    title_question = request.form.get("title")
    question = request.form.get("question")

    date_string = datetime.today().strftime('%Y-%m-%d')
    
    ask = Question(user_id = session["user_id"],question_created=date_string, title_question = title_question, question = question)

    db.session.add(ask)
    db.session.commit()

    return "question added"

@app.route("/write_note", methods=['POST'])
def write_note():
    """Allows user to write study notes"""

    title_note = request.form.get("title")
    note = request.form.get("note")

    date_string = datetime.today().strftime('%Y-%m-%d')
    diary = Note(user_id=session["user_id"],title_note = title_note, note_created=date_string, note=note)

    db.session.add(diary)
    db.session.commit()
   
    return "note added"


@app.route("/edit_current_note", methods=['POST'])
def edit_current_note():
    """Allows user to edit study notes"""
    note_id = request.form.get("note_id")

    edited_note = Note.query.get(note_id)

    edited_note.title_note = request.form.get("title")
    edited_note.note = request.form.get("note")


    db.session.commit()
   
    return "note edited"



@app.route("/view_questions")
def view_questions():
    """Allows user to view previously asked questions"""
    user_id = session.get("user_id")
   
    if user_id:
        questions = Question.query.filter_by(user_id = user_id).all()

        user_info = User.query.filter(User.user_id == user_id).first()
        image = user_info.images[0]

        return render_template("question_list.html", questions = questions, user_info=user_info, image=image)

    else: 
        return redirect("/login")

        
    

@app.route("/view_notes")
def view_notes():
    """Allows users to view past written notes"""
    
    user_id = session.get("user_id")

    if user_id:
        notes = Note.query.filter_by(user_id = user_id).all()

        user_info = User.query.filter(User.user_id == user_id).first()
        image = user_info.images[0]

        return render_template("notes.html", notes = notes, user_info=user_info, image=image)
    else:
        return redirect("/login")

@app.route("/view_note/<int:note_id>")
def view_note(note_id):
    """Allows user to view an individual note"""

    user_id = session.get("user_id")

    if user_id:
        notes = Note.query.filter_by(user_id = user_id).all()

        user_info = User.query.filter(User.user_id == user_id).first()
        image = user_info.images[0]
    
        user_note = Note.query.get(note_id)

        return render_template("view_note.html", user_note=user_note, user_info=user_info, image=image, notes=notes)
    else:
        return redirect("/login")

@app.route("/delete_note_from_list", methods=["POST"])
def delete_note_from_list():
    note_id = request.form.get("note_id")
    deleted_note = Note.query.filter(Note.note_id == note_id).first()
    db.session.delete(deleted_note)
    db.session.commit()

    return "note deleted"


@app.route("/delete-note/<int:note_id>")
def delete_note(note_id):
    """Deletes note"""

    user_id = session.get("user_id")

    if user_id:
        notes = Note.query.filter_by(user_id = user_id).all()
        user_note = Note.query.get(note_id)
        user_info = User.query.get(user_id)
        image = user_info.images[0]

        db.session.delete(user_note)
        db.session.commit()

    return redirect("/view_notes")



@app.route("/question_and_comment/<int:question_id>")
def view_question_comments(question_id):

    user_id = session.get("user_id")

    if user_id:
        
        user = User.query.get(session["user_id"])

        ask = Question.query.get(question_id) 
        user_asker = User.query.filter(User.user_id == ask.user_id).first()
        asker_image = user_asker.images[0]
        
        comments = ask.comments #comments related to the ask(question)
        comment_id = []
        for comment in comments:
            comment_id.append(comment.comment_id)
        comment_id.sort()

        comments = []
        for comm_id in comment_id:
            comment_deets = {}
            comment_obj = Comment.query.get(comm_id)
            comment_deets["comment"] = comment_obj.comment

            user_commenter = User.query.filter(User.user_id == comment_obj.user_id).first()
            comment_deets["comment_id"] = comm_id
            comment_deets["user"] = user_commenter.username
            comment_deets["image"] = user_commenter.images[0].image
            comment_deets["vote"] = comment_obj.vote_count()
            comment_deets["comment_timestamp"] = comment_obj.comment_timestamp
            comment_deets["user_id"] = user_commenter.user_id
           
        
            comments.append(comment_deets)
        

        return render_template("question_and_comment.html", ask=ask, comments=comments, user_asker=user_asker, asker_image=asker_image, user=user)

    else: 
        return redirect("/login")



@app.route("/add-comment.json", methods=['POST'])
def add_comment():
    
    comment = request.form.get("comment")
    question_id = request.form.get("question_id")

    question_info = Question.query.get(question_id)
    question_author = User.query.filter(User.user_id == question_info.user_id).first()

    date_string = datetime.today().strftime('%Y-%m-%d')
    commented_item = Comment(user_id = session["user_id"], comment_timestamp = date_string, question_id = question_id, comment = comment) 
    db.session.add(commented_item)
    db.session.commit()

    comment_author = User.query.filter(User.user_id == commented_item.user_id).first()
    comment_auth_image = comment_author.images[0]
    

    result = {'comment_id': commented_item.comment_id, 
              'vote': commented_item.vote_count(),
              'comment_author': comment_author.username,
              'comment_auth_image':comment_auth_image.image, 
              'comment_timestamp': commented_item.comment_timestamp,
              'user_id': comment_author.user_id}

    notify_author_comment(commented_item.comment, question_author.email, question_author.username, question_info.question, question_info.title_question, comment_author.username)


    return jsonify(result)


def notify_author_comment(comment, author_email, author_username ,question, question_title, comment_author):
    """notifies author of question when a user has commented on their question"""

    content = "Hello " + author_username + ","+ "\n" +  "\n" + "Fellow camper, " + comment_author + " has commented on your question:" + "\n" + question_title + "\n" + question + "!" + "\n" +  "\n" +"They have stated the following: " + "\n" + comment
    send_mail(to=author_email, from_="admin@campbuddy.com", content=content)

def send_mail(to=None, from_=None, content=None):
    

    msg = MIMEText(content)
   
    msg['Subject'] = 'Someone has commented on your question!' 
    msg['From'] = from_
    msg['To'] = to
    s = smtplib.SMTP('localhost')
    s.sendmail(from_, [to], msg.as_string())
    s.quit()



@app.route("/add-vote.json", methods=['POST']) 
def add_vote():
    """allows user to add a vote to a comment"""
    

    comment_id = request.form.get("comment_id")
    voted_item = request.form.get("voted_item")


    comment = Comment.query.get(int(comment_id))
    
    
    vote_check = Vote.query.filter(Vote.comment_id == int(comment_id), Vote.user_id == session['user_id']).first()
    if vote_check:
        db.session.delete(vote_check)
        db.session.commit()
    else:
        vote_added = Vote(user_id = session['user_id'], comment_id = int(comment_id), up_vote = True)
        db.session.add(vote_added)
        db.session.commit()

        
   
    result = {'vote': comment.vote_count(), "comment_id": comment_id}
    return jsonify(result)



@app.route("/search-questions")
def search_question(): 
    user_id = session.get("user_id")

    if user_id:
   
        return render_template("question_search.html")

    else: 
        return redirect("/login")



@app.route('/return-search')
def return_search_question(): 

   
    query_dict = {}
    search_list = []
    search = request.args.get("search_item")
  
    splitted_search = search.split(" ")
    
    for word in splitted_search:
        search_match = Question.query.filter(Question.question.like('%' + word + '%') ).all() 
        search_list.extend(search_match)
        search_match = Question.query.filter(Question.title_question.like('%' + word + '%') ).all()
        search_list.extend(search_match)

    for question in search_list:
        question_author = User.query.filter(User.user_id == question.user_id).first()
        question_auth_image = question_author.images[0]

        query_dict[question.question_id]=[question.question, question.title_question, question_author.username, question_auth_image.image, question.comment_on_question_count(), question_author.user_id, question.question_created]

    return jsonify(query_dict)



if __name__ == "__main__":
  
    app.debug = True

    connect_to_db(app)

  
    DebugToolbarExtension(app)

    app.run()


