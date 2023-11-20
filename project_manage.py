# BEGIN part 1

# import database module

# define a funcion called initializing

def initializing():
    persons_read = database.ReadCSV('persons').fetch
    self.__persons = database.Table('persons', persons_read)
    self.__db = database.DB()
    self.__db.insert(self.__persons)
    self.__credentials = database.Table('credentials', [])
    for i in self.__persons.table:
        temp_dict = {}
        temp_dict['person_id'] = i['ID']
        temp_dict['username'] = i['fist'] + '.' + i['last'][0]
        temp_dict['password'] = ''.join([str((random.randrange(0, 10))) for _ in range(4)])
        if i['type'] == 'student':
            temp_dict['role'] = 'Member'
        elif i['type'] == 'faculty':
            temp_dict['role'] = 'Faculty'
        self.__credentials.insert(temp_dict)
        self.__db.insert(self.__credentials)
        print(self.__db.search('credentials'))

# here are things to do in this function:

    # create an object to read an input csv file, persons.csv

    # create a 'persons' table

    # add the 'persons' table into the database

    # create a 'login' table

    # the 'login' table has the following keys (attributes):
        # person_id
        # username
        # password
        # role

    # a person_id is the same as that in the 'persons' table

    # let a username be a person's fisrt name followed by a dot and the first letter of that person's last name

    # let a password be a random four digits string

    # let the initial role of all the students be Member

    # let the initial role of all the faculties be Faculty

    # create a login table by performing a series of insert operations; each insert adds a dictionary to a list

    # add the 'login' table into the database

# define a funcion called login

    def login(self):
        username = input('username: ')
        password = input('password: ')
        user = self.__credentials.filter(lambda x: x['username'] == username 
                and x['password'] == password).select(['person_id', 'role'])
        if user != []:
            return(user)
        else:
            return(None)

# here are things to do in this function:
   # add code that performs a login task
        # ask a user for a username and password
        # returns [person_id, role] if valid, otherwise returning None

# make calls to the initializing and login functions defined above

initializing()
val = login()

# END part 1

# CONTINUE to part 2 (to be done for the next due date)

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id

# if val[1] = 'admin':
    # do admin related activities
# elif val[1] = 'advisor':
    # do advisor related activities
# elif val[1] = 'lead':
    # do lead related activities
# elif val[1] = 'member':
    # do member related activities
# elif val[1] = 'faculty':
    # do faculty related activities
