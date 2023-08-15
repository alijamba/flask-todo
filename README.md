# flask-todo
# How to set up the project
# Basic installments
1. Install Python3
2. Install pip
3. Install virtualenv
4. Create virtual envriment
5. Install all the requirements from the requirement.txt file present in the project repo.

# Setup database (postgres)
I use Ubuntu for development and follow this link to create database https://www.cherryservers.com/blog/how-to-install-and-setup-postgresql-server-on-ubuntu-20-04
You can use it according to your OS.
1. Install Postgresql on your system
2. Create a new database named "todo_app"
3. Create a user named "postgres" with the password "postgres"
   You can create a user with any name and password.
   If you create a user with a different name and password then update it in the "development.py" file under the "todo_app.env_conigs" folder.
4. After successfully setup of the database and user you need to create and run migrations.
5. Run these commands
6. flask db migrate
7. flask db upgrade

# After successfully setting up the project you need to create the User to start testing it.
1. Create a new user using this endpoint
    POST   "localhost:5000/user/
     payload: {
            "username": "ABC"
             "password": "ABC"
             "admin": true/false
               }
2. To log in or get token use this endpoint
    POST   "localhost:5000/user/
     payload: {
            "username": "ABC"
             "password": "ABC"
               }
3. These are different endpoints for the user
   To get all users GET "localhost:5000/user/"
   To get particular user GET "localhost:5000/user/<str:user_uuid>/"
   To delete particular user POST "localhost:5000/user/<str:user_uuid>/"


# These are different endpoints to use the TODO APIs
1. To create a new todo
    POST "localhost:5000/todo/"
     payload: { "title": "Abc", "description": "Asdas", "complete": false}
2. To get all todos against particular users (users that are currently in the session)
     GET "localhost:5000/todo/"
3. To get particular todo
     GET "localhost:5000/todo/<int:task_id>/
4. To update the todo
     PUT "localhost:5000/todo/int:task_id>/
     payload: { "title": "Abc", "description": "Asdas", "complete": false}
     keys in the payloads are optional you can use all three at the same time and can use only one also.
5. To delete the todo
   DELETE "localhost:5000/todo/int:task_id>/"


# All of these endpoints are secured with JWT authentication except the user creation endpoint and login endpoint.



# ENCRYPTION
I use cryptography.fernet library to encrypt the data and decrypt it.

For now, I just encrypt two endpoint response
1. GET all todos
2. GET a particular todo
3. This encryption creates a secret key and encrypts the data using this key.
4. To decrypt the data I made an endpoint and you need to call the end.
5. endpoint:  POST "localhost:5000/decrypt/"
6. payload: 
            {
          "encrypted_data": "b'gAAAAABk2wHOQpzWYZCnkmoQZ1tLyJdiYYxSob5qEWR1-EZ5RXOuRFDisu-kgcSvLb8N1Em1K9AtBIdAaFlGca05M5TpyGQr7YxeKPSb7P8UzKLOyxaQr3W1hAAgbAw2PHfQ-oxk-RFgBs4gCRqrtg0qW9Q4DoG--         W4Xqp6aIyvCVNtczRYYBUNY5Z2JwEVFm3pTO-4aTK40Shm-bcypGhGZnN7UN8WCTrGWguruRJT50eeoXkj86j8T-AWFF9WTJ6xWo6SqvKk1IlrCrBe2IUjJPmUth_xwT9YNv80IQwVu06Ns8umHQOWk47WrtJ9OIRZTYlTW9-         eKBOxyVLAy3RaOHHoiJT8OL2ykEvkiHlhG8om-EOjY4e_sPzJ7iXEe-VNd8mRwykeB'"
   }


Just copy the encrypted response as it is and pass it to the endpoint as JSON. just like above and by hitting the endpoint you will get the decrypted response.




#----------------------------------------------------END-----------------------------------------------------------------
