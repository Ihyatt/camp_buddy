#Camp Buddy

Camp Buddy is a fun social platform that is designed to allow coding boot-campers the chance to connect and network. With it's visually appeasing layout, campers are able to access past written notes, and questions, edit their profile information, and search for questions or solutions relevant to them. Interacting with Camp Buddy is easy too! Once a comment is made on a camper's question, they are notified via email the username of the camper who commented and the comment that they wrote. Campers are also able to vote on each individual response, to better reflect the best solution to a difficult problem. When social platforms like stackoverflow feel too intimidating or overly advanced, then Camp Buddy is your solution.


![camp_buddy_demo](https://cloud.githubusercontent.com/assets/11432315/15886124/0ab8142c-2d10-11e6-87f1-92d420bf803e.gif)

##Contents

⋅⋅* Technologies Used
Features
User Profile Page
Search Function
Comment Forum

###Technologies Used

SQLAlchemy
PostgreSQL
Python
Flask
Jinja
Javascript
JQuery
JSON
HTML/CSS
Bootstrap
MailDev

###Features

####Current

User login and registration
Editable profile page with an image upload
User may ask questions which are then searchable by other users
User may view past questions
User my write private notes
User my edit or delete private notes
User may search for posted questions and then relayed on page using AJAX request
User may comment on other user's questions 

####Future

AJAX request on image upload where image upload reflects current uploaded image
Graphs using D3 to illustrate user interaction with Camp Buddy
Message inbox for each user
OAuth for user login

#####User Profile Page

When a user registers, their information is saved into a SQLAlchemy database. 

#####Search Function

Using an Ajax request, the value typed into the input box is then split and regerence with every word within both question and question title

#####Comment Forum

Comments may be added using an ajax request and then are appended to the page.
