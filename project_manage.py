# BEGIN part 1
import database
import os
# import database module

# define a funcion called initializing

def initializing():
    #TODO find a more fancy (and less confusing) way to define DB
    global DB
    DB = database.DB()
    for file in os.listdir('database'):
        if file.endswith('.csv'):
            #TODO IMPORTANT fix the content variable because it should send only file name
            content = database.ReadCSV(os.path.join('database', file)).fetch
            table = database.Table(''.join(list(file)[:-4]), content)
            DB.insert(table)
            
    # Code for testing that database ACTUALLY works.
    # print(DB.search('login'))
    # print()
    # DB.search('persons').insert({'ID': '0001', 'first': 'Arma', 'last': 'Agong', 'type': 'Yaaaaa'})
    print(DB.search('persons'))
    # print(type(DB.search('persons')))
    # print(DB.search('persons').table)


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
        if len(table.table) != 0:
            myFile = open(os.path.join(os.path.join(os.getcwd(), 'database'),
                                       table.table_name + '.csv'), 'w', newline = '')
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

# if val[1] == 'admin':
#     pass
# elif val[1] == 'student':
#     print('Options')
# elif val[1] == 'member':
#     pass
# elif val[1] == 'leader':
#     pass
# elif val[1] == 'faculty':
#     pass
# elif val[1] == 'advisor':
#     pass

# once everyhthing is done, make a call to the exit function
exit()
