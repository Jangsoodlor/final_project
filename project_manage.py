# BEGIN part 1
import database
import os
import persons as p
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
    # print(DB.search('persons'))
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
        return user[0]['ID'], user[0]['role']
    else:
        return None

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
print("""Graduation Project Management System. Version 0.0.0-alpha
Copyright (C) 2023 Jangsoodlor. All Rights Reserved.
This program is part of 01219114/15 Computer Programming I Course
Semester 1 Academic Year 2566 B.E. (2023 A.D.)
Kasetsart University
""")
while True:
    try:
        val = login()
        if val != None:
            break
        else:
            raise AssertionError
    except AssertionError:
        print('Login Failed.')
        print('Please recheck your ID and Password again')

# END part 1

# CONTINUE to part 2 (to be done for the next due date)

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id
print(f'Welcome! {val[1]} {val[0]}')

if val[1] == 'student':
    print("""S1: Accept/Reject Member Requests
S2: Become a Leader and Create a New Project""")
elif val[1] == 'member':
    print("""M1: View Project Status
M2: View Request Status
M3: Modify the Project's title""")
elif val[1] == 'leader':
    print("L1: Requests Member/Advisor")
    print("""M1: View Project Status
M2: View Request Status
M3: Modify the Project's title""")
elif val[1] == 'faculty':
    print("F1: Accept/Reject Advisor Requests")
elif val[1] == 'advisor':
    print("""A1: Approve the Project for Evaluation
A2: GIVE FINAL APPROVAL FOR THE PROJECT""")
elif val[1] == 'admin':
    print('Gomenasai, coming soon desu!')
choice = (input('Please choose one of the options above to proceed: '))

session = p.Main(val[0], val[1], ''.join([choice[0].capitalize(), choice[1]]), DB)

# once everyhthing is done, make a call to the exit function
exit()
