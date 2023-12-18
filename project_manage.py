# BEGIN part 1
import os
import database as dp
import persons as p
# import database module

# define a funcion called initializing

def initializing():
    global DB
    DB = dp.DB()
    try:
        for file in os.listdir('database'):
            if file.endswith('.csv'):
                content = dp.ReadCSV(os.path.join('database', file)).fetch
                table = dp.Table(''.join(list(file)[:-4]), content)
                DB.insert(table)
        check = ['member_pending_request',
                 'advisor_pending_request',
                 'project',
                 'project_to_eval']
        for i in check:
            if DB.search(i) == None:
                print(f'{i} table Does not exists. Creating {i} table')
                DB.insert(dp.Table(i, []))
    except FileNotFoundError:
        raise FileNotFoundError('Please make sure that you have a folder named "database" in the program\'s directory.')
    except (DB.search('login') == None, DB.search('persons') == None):
        raise FileNotFoundError('login.csv" and "persons.csv" Files Does Not Exists. Please contact Administrator')

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
        else:
            try:
                os.remove(os.path.join(os.path.join(os.getcwd(), 'database'),
                                   table.table_name + '.csv'))
            except FileNotFoundError:
                pass

# here are things to do in this function:
   # write out all the tables that have been modified to the corresponding csv files
   # By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:

   # https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python


# make calls to the initializing and login functions defined above

print("""Graduation Project Management System. Version 0.0.1-beta
Copyright (C) 2023 Jangsoodlor. All Rights Reserved.
This program is part of 01219114/15 Computer Programming I Course
Semester 1 Academic Year 2566 B.E. (2023 A.D.)
Kasetsart University

DO NOT copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this Software.
UNLESS you're a Kasetsart University Computer Engineering Department's Professor or Teacher Assistant.
THERE IS NO WARRANTY FOR THE PROGRAM. IN NO EVENT WILL THE COPYRIGHT HOLDER BE LIABLE TO YOU FOR DAMAGES.

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
""")
initializing()
print()
while True:
    val = login()
    if val is None:
        break
    else:
        print('Login Failed.')
        print('Please recheck your ID and Password again')

# END part 1

# CONTINUE to part 2 (to be done for the next due date)

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id
print(f'Welcome! {val[1]} {val[0]}')

while True:
    try:
        session = p.Main(val[0], val[1], DB)
    except (PermissionError, ValueError):
        print('Please choose a valid option.')
    except InterruptedError:
        print('Saving and Exiting....')
        break

# once everyhthing is done, make a call to the exit function
exit()
