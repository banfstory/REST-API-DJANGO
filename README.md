# Django-REST-API

The RESTful API allows users to create their own forums which gives a place for other users to create post

FLASK RESTFUL API INSTRUCTIONS: To run the Flask API, it needs to run on a local server and it will be running the application from a virtual environment so that all packages will be already pre-installed within the whole folder itself.

To run the virtual environment do the following (instructions for windows OS only), start with going into command prompt:

1. Go to root directory of this folder
2. Enter '.\Scripts\activate' to activate the virtual 
3. Go to src folder 
4. Enter 'python manage.py runserver 127.0.0.1:8000' to run the local server or choose whatever address or port number you want

RESTFUL API AUTHENTICATION
In order to access certain resources or perform certain actions, the user needs to authenticate themselves by providing their username and password where they will be given an access token and a refesh token. The access token provides authorization for the user to access to resources and perform actions that are otherwised restricted if no access token was provided. The refresh token will be required to refresh the access token that has expired (access token expires in 7 days but can be changed in the settings.py file located in the django_api folder). These tokens are represented as JSON web tokens (JWT) and these tokens are separated by period in between representing encoded header data and payload data with the signature to ensures that no one can create their own tokens and pretend to be someone else.

To authenticate a user and get the tokens use http:<span></span>//127.0.0.1:8000/api/token/ as a POST method with the header as 'Content-Type: application/json' and data as '{"username":"your username","password":"your password"}', for example in curl you can use 'curl -X POST -H 'Content-Type: application/json' -d '{"username":"admin","password":"pass"}' http:<span></span>//127.0.0.1:8000/api/token/' to authenticate. 

To refresh an expired token, you can use http:<span></span>//127.0.0.1:8000/api/token/refresh/ as a POST method with the header 'Content-Type: application/json' and data as '{"refresh":"your refresh token"}', for example in curl you can use 'curl -X POST -H 'Content-Type: application/json' -d '{"refresh":"your refresh token"}' http:<span></span>//127.0.0.1:8000/api/token/refresh/'

Certain endpoints are only accessible if you provide the access token. To provide an access token, provide the header with "Authorization: Bearer *Your access token*", for example in curl you can use 'curl -X PUT -H 'Content-Type: application/json' -H "Authorization: Bearer *Your access token*" -d '{"username":"admin", "email":"admin@gmail.<span></span>com"}' http:<span></span>//127.0.0.1:8000/api/users/1/'

NOTE: You can authenticate as admin with the username 'admin' and password 'pass'

<h2>RESTFUL API ENDPOINTS</h2>

The API endpoints are broken down into catrgories, these are USERS, FORUMS, POSTS, COMMENTS, REPLYS

Endpoints that return multiple results will only show 10 results per page. To navigate through each page, add the query param 'page' with the page number into URL endpoint </br>

When sending files with data, both the files and data must be sent as form data with header Content-Type: multipart/form-data instead of Content-Type: application/json, for example in curl you can use 'curl -X PUT -H 'Content-Type: multipart/form-data' -H "Authorization: Bearer *Your access token*" -F 'image=@*your file path*' -F 'username=admin' -F 'email=admin@gmail.<span></span>com' http:<span></span>//127.0.0.1:8000/api/users/1/'
 
<h3>USERS ENDPOINTS</h3>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/users/ <br/>
METHOD: GET <br/>
DESCRIPTION: Get details of all users accounts <br/>
QUERY PARAMS: q, username, page <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/users/ <br/>
METHOD: POST <br/>
DESCRIPTION: Register a user account <br/>
HEADER: Content-Type: application/json <br/>
DATA: username, email, password <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/users/<int:pk>/ <br/>
METHOD: GET <br/>
DESCRIPTION: Get a user account <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/users/<int:pk>/ <br/>
METHOD: PUT <br/>
DESCRIPTION: Update user account details <br/>
HEADER: Content-Type: application/json (without image file), 'Content-Type: multipart/form-data' (with image file), Authorization: Bearer *Your access token* <br/>
FILE: image <br/>
DATA: username, email <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/users/followers/ <br/>
METHOD: GET <br/>
DESCRIPTION: Get followers list of which users are following which forums <br/>
PARAM: user, forum <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/users/followers/ <br/>
METHOD: POST <br/>
DESCRIPTION: User follows a forum <br/>
HEADER: Content-Type: application/json, Authorization: Bearer *Your access token* <br/>
DATA: forum <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/users/<int:pk>/followers/ <br/>
METHOD: GET <br/>
DESCRIPTION: Get a instance of a user who is following a forum <br/>
DATA: forum <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/users/<int:pk>/followers/ <br/>
METHOD: DELETE <br/>
DESCRIPTION: User unfollows a forum <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/users/default-image/ <br/>
METHOD: PUT <br/>
DESCRIPTION: Set user image to default image <br/>
HEADER: Authorization: Bearer *Your access token* <br/>

<h3>FORUMS ENDPOINTS</h3>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/forums/ <br/>
METHOD: GET <br/>
DESCRIPTION: Get details of all forums <br/>
QUERY PARAMS: q, name, owner, page <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/forums/ <br/>
METHOD: POST <br/>
DESCRIPTION: Create forum <br/>
HEADER: Content-Type: application/json <br/>
DATA: name, about <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/forums/<int:pk>/ <br/>
METHOD: GET <br/>
DESCRIPTION: Get a user account <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/forums/<int:pk>/ <br/>
METHOD: PUT <br/>
DESCRIPTION: Update user's forum details <br/>
HEADER: Content-Type: application/json (without image file), 'Content-Type: multipart/form-data' (with image file), Authorization: Bearer *Your access token* <br/>
FILE: image <br/>
DATA: name, about <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/forums/<int:pk>/ <br/>
METHOD: DELETE <br/>
DESCRIPTION: Delete forum <br/>
HEADER: Authorization: Bearer *Your access token* <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/forums/<int:pk>/default-image/ <br/>
METHOD: PUT <br/>
DESCRIPTION: Set forum image to default image <br/>
HEADER: Authorization: Bearer *Your access token* <br/>

<h3>POSTS ENDPOINT</h3>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/posts/ <br/>
METHOD: GET <br/>
DESCRIPTION: Get details of all posts <br/>
QUERY PARAMS: forum, user <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/posts/ <br/>
METHOD: POST <br/>
DESCRIPTION: Create post for the forum <br/>
HEADER: Content-Type: application/json, Authorization: Bearer *Your access token* <br/>
DATA: title, content, forum <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/posts/<int:pk>/ <br/>
METHOD: GET <br/>
DESCRIPTION: Get details of a post <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/posts/<int:pk>/ <br/>
METHOD: PUT <br/>
DESCRIPTION: Update user's post details <br/>
HEADER: Content-Type: application/json, Authorization: Bearer *Your access token* <br/>
DATA: title, content <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/posts/<int:pk>/ <br/>
METHOD: DELETE <br/>
DESCRIPTION: Delete user's post <br/>
HEADER: Authorization: Bearer *Your access token* <br/>

<h3>COMMENTS ENDPOINT</h3>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/comments/ <br/>
METHOD: GET <br/>
DESCRIPTION: Get details of all comments <br/>
QUERY PARAMS: post, user <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/comments/ <br/>
METHOD: POST <br/>
DESCRIPTION: Create comment for the post <br/>
HEADER: Content-Type: application/json, Authorization: Bearer *Your access token* <br/>
DATA: content, post <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/comments/<int:pk>/ <br/>
METHOD: GET <br/>
DESCRIPTION: Get details of a comment <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/comments/<int:pk>/ <br/>
METHOD: PUT <br/>
DESCRIPTION: Update user's comment details <br/>
HEADER: Content-Type: application/json, Authorization: Bearer *Your access token* <br/>
DATA: content <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/comments/<int:pk>/ <br/>
METHOD: DELETE <br/>
DESCRIPTION: Delete user's comment <br/>
HEADER: Authorization: Bearer *Your access token* <br/>

<h3>REPLYS ENDPOINT</h3>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/replys/ <br/>
METHOD: GET <br/>
DESCRIPTION: Get details of all replys <br/>
QUERY PARAMS: comment, user <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/replys/ <br/>
METHOD: POST <br/>
DESCRIPTION: Create reply for the comment <br/>
HEADER: Content-Type: application/json, Authorization: Bearer *Your access token* <br/>
DATA: content, comment <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/replys/<int:pk>/ <br/>
METHOD: GET <br/>
DESCRIPTION: Get details of a reply <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/comments/<int:pk>/ <br/>
METHOD: PUT <br/>
DESCRIPTION: Update user's reply details <br/>
HEADER: Content-Type: application/json, Authorization: Bearer *Your access token* <br/>
DATA: content <br/>

ENDPOINT: http:<span></span>//127.0.0.1:8000/api/replys/<int:pk>/ <br/>
METHOD: DELETE <br/>
DESCRIPTION: Delete user's reply <br/>
HEADER: Authorization: Bearer *Your access token* <br/>

