#Camp Buddy

Camp Buddy is a fun social platform that is designed to allow coding boot-campers the chance to connect and network. With it's visually appeasing layout, campers are able to access past written notes, and questions, edit their profile information, and search for questions or solutions relevant to them. Interacting with Camp Buddy is easy too! Once a comment is made on a camper's question, they are notified via email the username of the camper who commented and the comment that they wrote. Campers are also able to vote on each individual response, to better reflect the best solution to a difficult problem. When social platforms like stackoverflow feel too intimidating or overly advanced, then Camp Buddy is your solution.



##Contents

* [Technologies Used](#technologiesused)
* [Features](#feautures)
* [User Profile Page](#profile)
* [Questions](#questions)
* [Notes](#notes)
* [Search Function](#search)
* [Comment Forum](#comment)
* [How to locally run Camp Buddy](#run)

###<a name="technologiesused"></a>Technologies Used

* [SQLAlchemy](http://www.sqlalchemy.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [Python](https://www.python.org/)
* [Flask](http://flask.pocoo.org/)
* [Jinja](http://jinja.pocoo.org/)
* [Javascript](https://www.javascript.com/)
* [JQuery](https://jquery.com/)
* [JSON](http://www.json.org/)
* [AJAX](http://api.jquery.com/jquery.ajax/)
* [HTML/CSS](http://www.w3schools.com/html/html_css.asp)
* [Bootstrap](http://getbootstrap.com/)
* [MailDev](https://www.npmjs.com/package/maildev)
* [Sessions](http://www.allaboutcookies.org/cookies/session-cookies-used-for.html)

###<a name="features"></a>Features

####Current

- [x] User login and registration
- [x] Editable profile information
- [x] Search page that renders matched query results
- [x] User may view past written questions
- [x] User may write private notes
- [x] Editable or deletable notes
- [x] Comment forum where comments are voteable and comments on a question are counted
- [x] Author of questions are notified whenever a comment is made in response to a question
- [x] Database checks to ensure a user gets one vote per comment

####Future

- [ ] Page that shows all questions within Camp Buddy with real time updates


#####<a name="profile"></a>User Profile Page
![campbuddy_prof](https://cloud.githubusercontent.com/assets/11432315/18407840/6e392eae-76d1-11e6-9136-8f4f39d72132.gif)

The user's profile information is saved within a PostgreSQL database. User interaction with Camp Buddy  such as questions asked and questions answered are measured by a set of methods within my model.py. Information from the database is queried using flask-SQLAlchemy based on user's id and displayed via jinja. 

#####<a name="questions"></a>Questions
![campbuddy_questions](https://cloud.githubusercontent.com/assets/11432315/18407845/8aecb25a-76d1-11e6-9c4f-5ed13bef9d2f.gif)


User questions again are queried based on a specific user, iterated over using a flask loop and displayed using jinja. The users image is a clickable link that links to a user's profile page and a questions is a clickable link that links to a question's comment forum. When a user asks a questions, a modal window appears and the question is taken into the flask server via an AJAX request and then committed into the database. 

#####<a name="notes"></a>Notes
![campbuddy_notes](https://cloud.githubusercontent.com/assets/11432315/18407847/9ba0cae6-76d1-11e6-8452-ef6fe21a7d2a.gif)


User notes are queried based on a specific user, iterated over using a flask loop and displayed using jinja. The user's image is a clickable link that links to a user's profile page. Notes that apear on the list of notes are deletable via an AJAX request. A user may also view a single note and edit that note via an AJAX request. When a user writes a note, a modal window appears and the note is taken into the flask server via an AJAX request and then committed into the database. 

#####<a name="search"></a>Search Function
![campbuddy_search](https://cloud.githubusercontent.com/assets/11432315/18407851/a84657f2-76d1-11e6-8c9b-0b86105d53a9.gif)


Once a user types set of phrases seperated by commas and clicks search, that information is then taken via an AJAX request, queried within my flask server, returned as a JSON object, iterated over by question id and displayed on the search page

#####<a name="comment"></a>Comment Forum
![campbuddy_comment](https://cloud.githubusercontent.com/assets/11432315/18407853/b88ca56c-76d1-11e6-8336-49f05803e919.gif)


Every question has its own comment forum. When a page is reloaded or visited, comments that are associated to a questions are displayed on the page with a flask loop. There are two event listeners that trigger AJAX requests on this page, the first is for a comment and the other is for votes. The value of the comment is put into an object, taken to the AJAX route, jsonified and then returned. When a comment is created, there is a ".click" event listener for votes which allows for the votes to be interacted with. Once a comment is posted, the author of the question is notified via email through MailDev.  

###<a name="run"></a>How to locally run Camp Buddy

####Run Camp Buddy Flask App

#####General Setup
* Set up and activate a python virtualenv, and install all dependencies:
    * `pip install -r requirements.txt`
  * Make sure you have PostgreSQL running. Create a new database in psql named camp_buddy:
	* `psql`
  	* `createdb camp_buddy`
 * Create the tables in your database:
    * `python -i model.py`
    * While in interactive mode, create tables: `db.create_all()`
 * Start up the flask server:
    * `python server.py`
 * Go to localhost:5000 to see the web app

#####Maildev Setup
* Open two new tabs on your currently running terminal. First terminal
  * initialize port`sudo maildev -s 25 -w 8081`
  * Then type password
* Second Terminal
  * type `telnet localhost 25`
* Go to localhost:5000 to see the comments posted
