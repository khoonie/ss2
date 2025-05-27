## FastAPI backend with JWT and MySQL access 
### Modular
This is the framework which would form the basis of a modular, multi-user system that separates the front end (Web, Mobile, etc.) from the backend
The database is also abstracted, meaning MySQL, PostGreSQL, SQLite, etc. can be used
### Flexibility
The front end can be an interface written in any language that displays the status from the backend, and perform changes by sending requests to the backend through API calls
Example front ends are iOS, Android apps, Web Browsers, Windows App, Mac App, Linux App, etc.
All API routes and their corresponding logic are contained in the server
Roughly, it is in this configuration:

Front End <----> API + Logic <----> Database

### Scalability
The API + Logic layer is stateless, and can be behind a load balancer to scale horizontally; likewise, so can the database layer

Note: include a .env file that lists the following parameters for database connections and secret key for JWT
#--------------------------
DB_USER=
DB_PASSWORD=
DB_PORT=
DB_NAME=
DB_HOST=
SECRET_KEY=
#--------------------------



