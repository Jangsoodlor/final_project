import random
import database
# start by adding the admin related code
class Admin:
    def __init__(self) -> None:
        # create an object to read an input csv file, persons.csv
        # create a 'persons' table
        # add the 'persons' table into the database
        # create a 'login' table
        # add the 'login' table into the database
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

    # add code that performs a login task; asking a user for a username and password; returning [person_id, role] if valid, otherwise returning None
    def login(self):
        username = input('username: ')
        password = input('password: ')
        user = self.__credentials.filter(lambda x: x['username'] == username 
                and x['password'] == password).select(['person_id', 'role'])
        if user != []:
            return(user)
        else:
            return(None)


if __name__ == '__main__':
    admin = Admin()
    print(admin.login())
    
# the 'login' table has the following keys (attributes):

# - person_id
# - username
# - password
# - role

# a person_id is the same as that in the 'persons' table
# let a username be a person's first name followed by a dot and the first letter of that person's last name
# let a password be a random four digits string
# let the initial role of all the students be Member
# let the initial role of all the faculties be Faculty

# you create a login table by performing a series of insert operations; each insert adds a dictionary to a list