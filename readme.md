--------------------
# Postgres DB Updater

Postgres DB Updater is a tool which task is to facilitate bulk modifications on multiple Postgres DBs'.  

After finishing specific tasks it sends a notification email with a log file and a summary containing 
the number of successful and failed operations and most common errors. 

Postgres DB Updater gathers the provided tasks and executes them one by one on each of the databases 
asynchronously. Once a task is executed on all databases the notification email is being sent and 
the next task processed.

## Prerequisites

Before you begin, ensure you have met the following requirements
(if you do not wish to install anything use the attached *docker-compose* file.):
* Python 3.8
* Pipenv
* an email account compatible with *smtplib*


## Installing Postgres DB Updater

To install Postgres DB Updater, follow these steps:
* Clone the repository and create a virtual environment with pipenv to install all the needed libraries
```
$ pipenv install
```
Set up the *.env* file with:
```
PRODUCTION=[False for running tasks on test DBs, True for normal usage]
TASKS_PATH=[yourpath/tasks.json - path to you tasks.json file]
TOP_ERROR_COUNT=[10 - number of most common errors to be send in the email]
PG_HOST=[your postgres db url]
PG_USER=[your postgres db admin user]
PG_PASSWORD=[your postgres db password]
PG_PORT=[5432 - postgres db port]
SMTP_SERVER=[smtp.gmail.com - in case of gmail]
SMTP_PORT=[587]
SENDER_EMAIL=[your google email account address]
EMAIL_PASSWORD=[your google email password]
RECEIVER_EMAIL=[recievers email address]
```

## Using Postgres DB Updater

Before running the app you must configure the *tasks.json* file correctly:

*tasks.json*
```
{
  "exclude": [],
  "databases": [],
  "tasks": {}
}
```
The *tasks.json* file contains three categories: exclude, databases and tasks.

In the *exclude* you can enter a list of names of the databases you do not wish to modify.
Defaulty you may wish to exclude the postgres, template and template0 DBs'.
```
"exclude": ["postgres", "template1", "template0"]
```
In the *databases* category you can enter a list of databases names you wish to modify.
If you leave it blank, the application will query the server for all the databases and
run the tasks on them.
```
"databases": ['Customer_10001', 'Archive_2016]
```
*tasks* is a dictionary containing the tasks you want to perform.
It's key->value based where the key stands for the name of the task, and the value is the
SQL query you want to execute.
```
  "tasks": {
    "create_table_persons": "CREATE TABLE Persons (PersonID int,LastName varchar(255),FirstName varchar(255),Address varchar(255),City varchar(255));",
    "create_table_animals": "CREATE TABLE Animals (AnimalID int,Name varchar(255));",
    "drop_table_persons": "DROP TABLE Persons",
    "drop_table_yolo": "DROP TABLE YOLO",
    "insert_into_animals": "INSERT INTO Animals VALUES (1, 'Maciej')"
  }
```


To use Postgres DB Updater simply start it with:
```
python app/main.py 
```

Or use the provided `docker-compose.yml`.

For both you need to point the app to the *tasks.json* file.
If you choose to use the `docker-compose` option you will need to set up the *volumes* 
for the Docker container to be able to reach it from your local drive.
 ```
    volumes:
      - /Users/user/repositories/db_updater:/tasks
```
The first part of the path (until the ```:```) point to the directory on your local drive.
The second part points to a directory set up within the container.
Matching *.env* setting:
```
TASKS_PATH=/tasks/tasks.json
```


### Testing Postgres DB Updater

To test Postgres DB Updater prepare you *tasks.json* and point the app to the correct file.
Set up the *PRODUCTION* environmental variable to False and:
PG_DB=db
PG_USER=postgres=
PG_PASSWORD=postgres
PG_PORT=5432

Then uncomment the *adminer* and *db* services in the `docker-compose.yml` file and
*depends_on* and *links* categories in the *updater* service.

Finally run `docker-compose run`.

Your list of tasks will be ran against 101 dbs created by the testing program.
With the adminer you can check the state of the db server and the dbs.
