# BEGIN part 1
import random
import database
# import database module

# define a funcion called initializing

def initializing():
    persons_read = database.ReadCSV('persons').fetch
    persons = database.Table('persons', persons_read)
    global db
    db = database.DB()
    db.insert(persons)
    credentials = database.Table('credentials', [])
    for i in persons.table:
        temp_dict = {}
        temp_dict['person_id'] = i['ID']
        temp_dict['username'] = i['fist'] + '.' + i['last'][0]
        temp_dict['password'] = ''.join([str((random.randrange(0, 10))) for _ in range(4)])
        if i['type'] == 'student':
            temp_dict['role'] = 'Member'
        elif i['type'] == 'faculty':
            temp_dict['role'] = 'Faculty'
        credentials.insert(temp_dict)
        db.insert(credentials)
        print(db.search('credentials'))

# here are things to do in this function:

    # create an object to read all csv files that will serve as a persistent state for this program

    # create all the corresponding tables for those csv files

    # see the guide how many tables are needed

    # add all these tables to the database


# define a funcion called login

def login():
    username = input('username: ')
    password = input('password: ')
    user = db.search('credentials').filter(lambda x: x['username'] == username 
            and x['password'] == password).select(['person_id', 'role'])
    if user != []:
        return(user)
    else:
        return(None)

# here are things to do in this function:
   # add code that performs a login task
        # ask a user for a username and password
        # returns [ID, role] if valid, otherwise returning None

# define a function called exit
def exit():
    pass

# here are things to do in this function:
   # write out all the tables that have been modified to the corresponding csv files
   # By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:
   
   # https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python


# make calls to the initializing and login functions defined above

initializing()
val = login()
print(val)

# END part 1

# CONTINUE to part 2 (to be done for the next due date)

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id

# if val[1] = 'admin':
    # see and do admin related activities
# elif val[1] = 'student':
    # see and do student related activities
# elif val[1] = 'member':
    # see and do member related activities
# elif val[1] = 'lead':
    # see and do lead related activities
# elif val[1] = 'faculty':
    # see and do faculty related activities
# elif val[1] = 'advisor':
    # see and do advisor related activities

# once everyhthing is done, make a call to the exit function
exit()
