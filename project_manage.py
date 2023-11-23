# BEGIN part 1
import database
import os
# import database module

# define a funcion called initializing

def initializing():
    global DB
    DB = database.DB()
    for file in os.listdir():
        if file.endswith('.csv'):
            filename = ''.join(list(file)[:-4])
            content = database.ReadCSV(filename).fetch
            table = database.Table(filename, content)
            DB.insert(table)
    print(DB.search('login'))
    print()
    print(DB.search('persons').table[0])


# here are things to do in this function:

    # create an object to read all csv files that will serve as a persistent state for this program

    # create all the corresponding tables for those csv files

    # see the guide how many tables are needed

    # add all these tables to the database


# define a funcion called login

def login():
    username = input('username: ')
    password = input('password: ')
    user = DB.search('login').filter(lambda x: x['username'] == username 
            and x['password'] == password).select(['ID', 'role'])
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
    import csv
    for table in DB.database:
        myFile = open(table.table_name + '.csv', 'w', newline = '')
        writer = csv.writer(myFile)
        writer.writerow([key for key in table.table[0]])
        for dictionary in table.table:
            writer.writerow(dictionary.values())
        myFile.close()

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
