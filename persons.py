#  To minimize bugs, include this comment:
#  
#  
#                        _oo0oo_
#                       o8888888o
#                       88" . "88
#                       (| -_- |)
#                       0\  =  /0
#                     ___/`---'\___
#                   .' \|     |// '.
#                  / \|||  :  |||// \
#                 / _||||| -:- |||||- \
#                |   | \\  -  /// |   |
#                | \_|  ''\---/''  |_/ |
#                \  .-\__  '-'  ___/-. /
#              ___'. .'  /--.--\  `. .'___
#           ."" '<  `.___\_<|>_/___.' >' "".
#          | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#          \  \ `_.   \_ __\ /__ _/   .-` /  /
#      =====`-.____`.___ \_____/___.-`___.-'=====
#                        `=---='
#  
#  
#      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
#  
#         Buddha for debugging without suffering
#
class Container:
    def __init__(self, table) -> None:
        self._table = table

    @property
    def get_table(self):
        return self._table
    
    def __str__(self) -> str:
        return str(self._table)

#TODO make printing dicts a nice-looking table
class Request(Container):
    """_summary_
    This class do everything which relates to doing requests and dealing with
    the request table.
    """
    def __init__(self, table) -> None:
        super().__init__(table)

    @property
    def __get_role(self):
        if 'member' in self._table.table_name:
            return 'member'
        elif 'advisor' in self._table.table_name:
            return 'advisor'

    def request(self, project_id, people_table):
        """_summary_

        This function is for sending requests to both member and advisors.
        As well as returning status of those requests.
        people_table : login.join(person, 'ID')
        """
        role = self.__get_role
        if role =='advisor':
            type = 'faculty'
        elif role == 'member':
            type = 'student'
        people = people_table.filter(lambda x: x['role'] == type).select(['ID', 'first', 'last'])
        print()
        print(f'Available {role} for recruitment')
        for i in people:
            print(i)
        recruit_list = []
        while True:
            try:
                recruit = input('Type the ID of the person you want to request, or press ENTER to exit: ')
                if recruit == '':
                    break
                if recruit not in [i['ID'] for i in people] :
                    raise AssertionError
            except AssertionError:
                print('The person you tried does not exist. Please try again')
                continue
            recruit_list.append(recruit)
        for i in recruit_list:
            temp_dict = {}
            temp_dict['ProjectID'] = project_id
            to_be = 'to_be_' + role
            temp_dict[to_be] = i
            temp_dict['response'] = None
            temp_dict['response_date'] = None
            self._table.insert(temp_dict)

    def status(self, project_id):
        """_summary_
        leader's and member's view
        """
        for i in self._table.filter(lambda x: x['ProjectID'] == project_id).table:
            print(i)

    def view(self, person_id):
        """_summary_
        students' and advisors' view
        """
        to_be = 'to_be_' + self.__get_role
        for i in self._table.filter(lambda x: x[to_be] == person_id and x['response'] == None).table:
            print(i)

    def decide(self, person_id, project_id, decision, login_table = None, project_obj = None):
        # Ask for project_id in the main class using self.view
        import datetime
        role = self.__get_role
        to_be = 'to_be_' + role
        for i in self._table.table:
            if i[to_be] == person_id and i['ProjectID'] == project_id:
                i['response'] = decision.lower().title()
                i['response_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
        if decision.lower() == 'accepted':
            login_table.update('ID', person_id, 'role', role)
            project_obj.update(project_id, role, person_id)
            # Automatically refused all other requests
            for i in self._table.table:
                if i[to_be] == person_id and i['ProjectID'] != project_id:
                    self.decide(person_id, i['ProjectID'], 'rejected')
            # Auto delete every request once the project ist full
            for i in project_obj.get_table.table:
                if (role == 'member' and i['member1'] != None and i['member2'] != None)\
                    or (role == 'advisor' and i['advisor'] != None):
                    for j in self._table.table:
                        if i['ProjectID'] == j['ProjectID'] and j['response'] == None:
                            self._table.table.remove(j)



class Project(Container):
    """_summary_
    This class does everything related to project manipulation
    """
    def __init__(self, table) -> None:
        super().__init__(table)
    
    def create(self, title, leader_id, login_table):
        #TODO write AssertionError if a leader already have a project
        temp_dict = {}
        temp_dict['ProjectID'] = str(len(self._table.table) + 1)
        temp_dict['title'] = title
        temp_dict['leader'] = leader_id
        temp_dict['member1'] = None
        temp_dict['member2'] = None
        temp_dict['advisor'] = None
        temp_dict['status'] = 'Pending'
        self._table.insert(temp_dict)
        login_table.update('ID', leader_id, 'role', 'leader')
    
    def find_dict(self, key, args):
        return self._table.filter(lambda x: x[key] == args).table[0]
        
    def get_id(self, key, args):
        return self.find_dict(key, args)['ProjectID']
    
    def update(self, project_id, key_update, val_update):
        project_dict = self.find_dict('ProjectID', project_id)
        if key_update == 'member' and project_dict['member1'] != None:
            key_update ='member2'
        elif key_update == 'member' and project_dict['member1'] == None:
            key_update = 'member1'
        self._table.update('ProjectID', project_id, key_update, val_update)


class Main:
    def __init__(self, id, role, database) -> None:
        self.__id = id
        self.__role = role
        self.__database = database
        print(f'Welcome! {self.__role} {self.__id}')
        print()
        #TODO do all the automatic notification process
        if self.__role == 'student':
            print("""S1: Accept/Reject Member Requests
S2: Become a Leader and Create a New Project""")
        elif self.__role == 'member':
            print("""M1: View Project Status
M2: View Request Status
M3: Modify the Project's title""")
        elif self.__role == 'leader':
            print("L1: Requests Member/Advisor")
            print("""M1: View Project Status
M2: View Request Status
M3: Modify the Project's title""")
        elif self.__role == 'faculty':
            print("F1: Accept/Reject Advisor Requests")
        elif self.__role == 'advisor':
            print("""A1: Approve the Project for Evaluation
A2: GIVE FINAL APPROVAL FOR THE PROJECT""")
        elif self.__role == 'admin':
            print('Gomenasai, coming soon desu!')
        choice = (input('Please choose one of the options above to proceed: '))
        choice2 = ''.join([choice[0].capitalize(), choice[1]])
        print('\n' + choice2)

# the code below is for testing purposes
if __name__ == '__main__':
    # __init__
    import database as dp
    import os
    project = dp.Table('project', [])
    login = dp.Table('login', dp.ReadCSV(os.path.join('database', 'login.csv')).fetch)
    person = dp.Table('login', dp.ReadCSV(os.path.join('database', 'persons.csv')).fetch)
    member_request = Request(dp.Table('member_request', []))
    advisor_request = Request(dp.Table('advisor_request', []))
    project_table = Project(dp.Table('Project', []))
    
    print(member_request)
    print(project_table)

    project_table.create('Magic Wand', '2567260', login)
    project_table.create('Magic Eraser', '9898118', login)
    print(project_table)
    print(login.filter(lambda x: x['role'] == 'leader'))
    member_request.request(project_table.get_id('leader', '2567260'), login.join(person, 'ID'))
    advisor_request.request(project_table.get_id('leader', '2567260'), login.join(person, 'ID'))
    member_request.request(project_table.get_id('leader', '9898118'), login.join(person, 'ID'))
    advisor_request.request(project_table.get_id('leader', '9898118'), login.join(person, 'ID'))
    print()


    print('decisions')
    member_request.status('1')
    advisor_request.status('1')
    member_request.status('2')
    advisor_request.status('2')
    
    member_request.decide('1863421', '1', 'accepted', login, project_table)
    member_request.decide('7998314', '1', 'rejected')
    member_request.decide('5086282', '1', 'accepted', login, project_table)
    
    member_request.decide('1228464', '2', 'accepted', login, project_table)
    member_request.decide('3938213', '2', 'rejected')
    member_request.decide('4788888', '2', 'accepted', login, project_table)
    
    advisor_request.decide('2472659', '1', 'accepted', login, project_table)
    advisor_request.decide('7525643', '2', 'accepted', login, project_table)
    for i in project_table.get_table.table:
        print(i)
    print()
    print('After recruitment')
    member_request.status('1')
    advisor_request.status('1')
    member_request.status('2')
    advisor_request.status('2')
    print(login)
