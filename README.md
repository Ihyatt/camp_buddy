#Camp Buddy

Camp Buddy is a fun social platform that is designed to allow coding boot-campers the chance to connect and network. With it's visually appeasing layout, campers are able to access past written notes, and questions, edit their profile information, and search for questions or solutions relevant to them. Interacting with Camp Buddy is easy too! Once a comment is made on a camper's question, they are notified via email the username of the camper who commented and the comment that they wrote. Campers are also able to vote on each individual response, to better reflect the best solution to a difficult problem. When social platforms like stackoverflow feel too intimidating or overly advanced, then Camp Buddy is your solution.


![camp_buddy_demo](https://cloud.githubusercontent.com/assets/11432315/15886124/0ab8142c-2d10-11e6-87f1-92d420bf803e.gif)

##Contents

* Technologies Used
* Features
* User Profile Page
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

- [x] User login and registration which are tracked by sessions
- [x] Editable profile page with a Flask image upload 
- [x] User may ask questions which are then searchable by other users
- [x] User may view past questions
- [x] User my write private notes
- [x] User my edit or delete private notes. Notes are deleted in real time using an AJAX request
- [x] User may search for posted questions and then relayed on page using AJAX request
- [x] User may comment on other user's questions in a comment forum. Comments are posted through an AJAX request 

####Future

- [ ] AJAX request on image upload where visually the upload reflects current uploaded image
- [ ] Graphs using D3 to illustrate user interaction with Camp Buddy
- [ ] Message inbox for each user
- [ ] OAuth for user login using either Facebook or Google

#####User Profile Page

When a user registers with Camp Buddy, their information is immediately saved into a SQLAlchemy database. This information is both editable and displayed on their profile page. 

#####Search Function

When a user is on the "search" page, they are able to input a set of keywords seperated by commas to search past written questions. The result of this search is then rendered in real time on the search page via an AJAX request. Within the AJAX request url, there is a query, that queries the question database. The matches along with the relevant information of the author is placed into a JSON object and then deleviered back to the search page.  

#####Comment Forum

The comment forum is one of my favorie features of Camp Buddy. Next to the comment box, there is the current user's profile image. When a user comments on a question, the author of th question is immediatley notified via MailDev. This notification includes the username of the commenter and the comment that they wrote. Another feature I love about the comment forum is the shape of the commet box which is made to mimick Iphone chat.
