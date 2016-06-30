#Camp Buddy

Camp Buddy is a fun social platform that is designed to allow coding boot-campers the chance to connect and network. With it's visually appeasing layout, campers are able to access past written notes, and questions, edit their profile information, and search for questions or solutions relevant to them. Interacting with Camp Buddy is easy too! Once a comment is made on a camper's question, they are notified via email the username of the camper who commented and the comment that they wrote. Campers are also able to vote on each individual response, to better reflect the best solution to a difficult problem. When social platforms like stackoverflow feel too intimidating or overly advanced, then Camp Buddy is your solution.


![camp_buddy_demo](https://cloud.githubusercontent.com/assets/11432315/15886124/0ab8142c-2d10-11e6-87f1-92d420bf803e.gif)

##Contents

* Technologies Used
* Features
* User Profile Page
* Questions
* Notes
* Search Function
* Comment Forum

###Technologies Used

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

###Features

####Current

- [x] User login and registration
- [x] Editable profile information
- [x] Search page that renders matched query results
- [x] User may view past written questions
- [x] User my write private notes
- [x] Editable or deletable notes
- [x] Comment forum where comments are voteable and comments on a question are counted
- [x] Author of questions are notified whenever a comment is made in response to a question

####Future

- [ ] AJAX request for image upload
- [ ] Include Chart.js to illustrate user interaction with Camp Buddy
- [ ] Message inbox for each user
- [ ] OAuth for user login using either Facebook or Google
- [ ] Private chat messaging for users
- [ ] Page that shows all questions within Camp Buddy with real time updates

#####User Profile Page

The user's profile information is saves within a PostgreSQL. User interaction with Camp Buddy which includes questions asked and questions answered are a set of methods within my model.py (where my classes are where database information is instantiated). Information from the database is queried using flask-SQLAlchemy based on user's id and displayed via jinja. 

#####Questions

User questions again are queried based on a specific user, iterated over using a flask loop and displayed using jinja. The users image is a clickable link that links to a user's profile page and a questions is a clickable link that links to a question's comment forum. When a user asks a questions, a modal window appears and the question is taken into the flask server via an AJAX request and then committed into the database. 

#####Notes

User notes gain are queried based on a specific user, iterated over using a flask loop and displayed using jinja.The users image is a clickable link that links to a user's profile page. Notes that apear on the list of notes are deletable via an AJAX request. A user may also view a single note and edit that note via an AJAX request. When a user writes a note, a modal window appears and the note is taken into the flask server via an AJAX request and then committed into the database. 

#####Search Function

When a user types in a set of phrases seperated by sentences and the search button is pressed, that information is then taken via JQuery and an AJAX request, queried within my flask server, returned as a JSON object, and the results are iterated over  by question id and displayed on the search page

#####Comment Forum

Every question has its own comment forum. When a page is reloaded or visited, comments that are back referenced to a questions are displayed on the page with a flask loop. There are two AJAX requests on this page, the first is an AJAX request for a comment and the other is for votes. The value of the comment is put into an object, taken to the AJAX route, jsonified and then returned. When a comment is created, the ".click" event for the vote is nested within the success function within the comment AJAX request success function so that the vote is interactable with the comment is created.  
