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
* update : to change student infos,move studnet, update amenity
* insert student: Randomly base on his country, insert manuelly
* Get: to retrieve all infos from db exampe: student, room, buidings, amenety of the room, hostel residents, report (normal report)
* all : To retrieve all objects
* report: to report an issue
* count: to list the number of students(following some criteria)

## Part1 : delete, insert (Antoine)
## Part2 : get, report, count, update  (Amadou)
