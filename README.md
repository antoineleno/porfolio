# Classes
## BaseModel

## Db_storage
## User
* first_name
* last_name
* email
* passowrd

## Building 
* RoomNumber
* RoomID(primary key)
* Hostel(Male/Female)
* Block name

## Student
* Student_name
* Student_ID
* Country(Uniq for same block id)
* Room_ID(Foreign key)
* Zone (A, B, C, D)

## Facilities
* bed,etc ......

* part1: BaseModel, User, Buidling (Antoine)
* part2: db_storage, student, facilities (Amadou)

# Console 
* create : To create all objects 
* delete : to manage everything : delete buidling, students, room, zone
* update : to change student infos, update amenity
* insert student: Randomly base on his country, insert manuelly
* Get: to retrieve all infos from db exampe: student, room, buidings, amenety of the room, hostel residents, report (normal report)
* all : To retrieve all objects
* report: to report an issue
* count: to list the number of students(following some criteria)

<<<<<<< HEAD
## Part1 : delete, insert, update (Antoine)
## Part2 : get, report, count  (Amadou)




# Database setting up
## Run the following command to set up the database
* cat requirements/setup_mysql_dev.sql | sudo mysql -hlocalhost -uroot -p

# To Run the console
* CAMPUS_MYSQL_USER=campus_dev CAMPUS_MYSQL_PWD=campus_dev_pwd CAMPUS_MYSQL_HOST=localhost CAMPUS_MYSQL_DB=campus_dev_db CAMPUS_TYPE_STORAGE=db ./console.py
# Route fro admin page
* http://127.0.0.1:5000/campusstay/admin/dashboard
# To run unitest
* HBNB_ENV=test CAMPUS_MYSQL_USER=campus_dev CAMPUS_MYSQL_PWD=campus_dev_pwd CAMPUS_MYSQL_HOST=localhost CAMPUS_MYSQL_DB=campus_dev_db CAMPUS_TYPE_STORAGE=db python3 -m unittest discover tests
=======
## Part1 : delete, insert (Antoine)
## Part2 : report,  update  (Amadou)
>>>>>>> f7a7211ebb636cae434febacaa9df943dcc7ffba
