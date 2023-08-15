# flask-todo
# How to setup the project
# Basic intallements
1. Install Python3
2. Install pip
3. Install virtualenv
4. Create virtual envriment
5. Install all the requiremnts from requirement.txt file present in the project repo.

# Setup database (postgres)
I use ubuntu for development and follow this link to create database https://www.cherryservers.com/blog/how-to-install-and-setup-postgresql-server-on-ubuntu-20-04
You can use according to your OS.
1. Install postgresql on your system
2. Create new database named "todo_app"
3. Create user named "postgres" with password "postgres"
   You can create user with any name and password.
   If you create user with different name and password then update it in "development.py" file under "todo_app.env_conigs" folder.
4. After successfull setup of database and user you need to create and run migrartions.
5. Run these commands
6. flask db migrate
7. flask db upgrade

# After successfully setting up the project you need to create the User to start testing it.
1. Create new user using this endpoint
    POST   "localhost:5000/user/
     payload: {
            "username": "abc"
             "password": "abc"
             "admin": true/false
               }
2. To login or get token use this end point
    POST   "localhost:5000/user/
     payload: {
            "username": "abc"
             "password": "abc"
               }
3. These are different end points for the user
   To get all users GET "localhost:5000/user/"
   To get particular user GET "localhost:5000/user/<str:user_uuid>/"
   To delete particular user POST "localhost:5000/user/<str:user_uuid>/"


# These are different end point to use the TODO APIs
1. To create new todo
    POST "localhost:5000/todo/"
     payload: { "title" : "Abc", "description": "Asdas", "complete": false}
2. To get all todos against particualr user (user that are currently in the session)
     GET "localhost:5000/todo/"
3. To get particaular todo
     GET "localhost:5000/todo/<int:task_id>/
4. To update the todo
     PUT "localhost:5000/todo/int:task_id>/
     payload: { "title" : "Abc", "description": "Asdas", "complete": false}
     keys in the payloads are optional you can use all three at the same time and can use only one also.
5. To delete the todo
   DELETE "localhost:5000/todo/int:task_id>/"


# All of these end points are secured with JWT authetication except user creation end point and login end point.
