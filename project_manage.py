# import database module
import random
import database
# start by adding the admin related code

# create an object to read an input csv file, persons.csv
persons_read = database.ReadCSV('persons').fetch
# create a 'persons' table
persons = database.Table('persons', persons_read)
# add the 'persons' table into the database
db = database.DB()
db.insert(persons)
# create a 'login' table
login = database.Table('login', [])
# the 'login' table has the following keys (attributes):

# person_id
# username
# password
# role

# a person_id is the same as that in the 'persons' table
# let a username be a person's first name followed by a dot and the first letter of that person's last name
# let a password be a random four digits string
# let the initial role of all the students be Member
# let the initial role of all the faculties be Faculty

# you create a login table by performing a series of insert operations; each insert adds a dictionary to a list
for i in persons.table:
    credentials = {}
    credentials['person_id'] = i['ID']
    credentials['username'] = i['fist'] + '.' + i['last'][0]
    credentials['password'] = ''.join([str((random.randrange(0, 10))) for _ in range(4)])
    if i['type'] == 'student':
        credentials['role'] = 'Member'
    elif i['type'] == 'faculty':
        credentials['roles'] = 'Faculty'
    login.insert(credentials)
print(login)
    # add the 'login' table into the database

# add code that performs a login task; asking a user for a username and password; returning [person_id, role] if valid, otherwise returning None
