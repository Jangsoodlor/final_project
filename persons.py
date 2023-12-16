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
import database as dp
import os

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

    def request(self, project_id, recruit_id):
        """_summary_

        This function is for sending requests to both member and advisors.
        """
        role = self.__get_role
        temp_dict = {}
        temp_dict['ProjectID'] = project_id
        to_be = 'to_be_' + role
        temp_dict[to_be] = recruit_id
        temp_dict['response'] = ''
        temp_dict['response_date'] = ''
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
        print('Requests')
        to_be = 'to_be_' + self.__get_role
        for i in self._table.filter(lambda x: x[to_be] == person_id).table:
            print(i)

    def decide(self, person_id, project_id, decision, login_table = None, project_obj = None):
        # Ask for project_id in the main class using self.view
        role = self.__get_role
        to_be = 'to_be_' + role
        if (len(self._table.filter(lambda x: x['ProjectID'] == project_id and x[to_be] == person_id).table) == 0)\
            or (decision.lower() not in ['accepted', 'rejected']):
            raise ValueError
        import datetime
        for i in self._table.table:
            if i[to_be] == person_id and i['ProjectID'] == project_id:
                i['response'] = decision.lower()
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
                if (role == 'member' and i['member1'] != '' and i['member2'] != '')\
                    or (role == 'advisor' and i['advisor'] != ''):
                    for j in self._table.table:
                        if i['ProjectID'] == j['ProjectID'] and j['response'] == '':
                            self._table.table.remove(j)
            print('Please Restart the program')
            raise KeyboardInterrupt


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
        temp_dict['member1'] = ''
        temp_dict['member2'] = ''
        temp_dict['advisor'] = ''
        temp_dict['status'] = 'Pending'
        self._table.insert(temp_dict)
        login_table.update('ID', leader_id, 'role', 'leader')
    
    def find_dict(self, key, args):
        try:
            return self._table.filter(lambda x: x[key] == args).table[0]
        except IndexError:
            return None
        
    def get_id(self, key, args):
        return self.find_dict(key, args)['ProjectID']
    
    def update(self, project_id, key_update, val_update):
        project_dict = self.find_dict('ProjectID', project_id)
        if key_update == 'member' and project_dict['member1'] != '':
            key_update ='member2'
        elif key_update == 'member' and project_dict['member1'] == '':
            key_update = 'member1'
        self._table.update('ProjectID', project_id, key_update, val_update)


class Main:
    def __init__(self, id, role, database) -> None:
        self.__id = id
        self.__role = role
        self.__database = database
        self.__member_request = Request(self.__database.search('member_pending_request'))
        self.__advisor_request = Request(self.__database.search('advisor_pending_request'))
        self.__projects = Project(self.__database.search('project'))
        
        if self.__role == 'student':
            self.__member_request.view(self.__id)
            print('\n' + 'Options')
            print("S1: Accept/Reject Member Requests")
            print("S2: Become a Leader and Create a New Project")

        elif self.__role == 'member':
            print('Project Status')
            print(self.__projects.find_dict('ProjectID', self.__find_project_id()))
            print()
            print('Member Request Status')
            self.__member_request.status(self.__find_project_id())
            print()
            print('Advisor Request Status')
            self.__advisor_request.status(self.__find_project_id())
            print('\n' + 'Options')
            print("M1: Modify the Project's title")

        elif self.__role == 'leader':
            print('Project Status')
            print(self.__projects.find_dict('ProjectID', self.__find_project_id()))
            print()
            print('Member Request Status')
            self.__member_request.status(self.__find_project_id())
            print()
            print('Advisor Request Status')
            self.__advisor_request.status(self.__find_project_id())
            print('\n' + 'Options')
            print("L1: Requests Member/Advisor")
            print("M1: Modify the Project's title")

        elif self.__role == 'faculty':
            self.__advisor_request.view(self.__id)
            print('\n' + 'Options')
            print("F1: Accept/Reject Advisor Requests")

        elif self.__role == 'advisor':
            print('\n' + 'Options')
            print("A1: Approve the Project for Evaluation")
            print("A2: GIVE FINAL APPROVAL FOR THE PROJECT")

        elif self.__role == 'admin':
            print('Gomenasai, coming soon desu!')

        self.__do = (input('Please choose one of the options above to proceed. Or press ENTER to exit: ')).capitalize()
        if self.__do == '':
            raise KeyboardInterrupt
        elif len(self.__do) != 2:
            raise ValueError
        
        if ('S' in self.__do and self.__role != 'student')\
            or ('M' in self.__do and self.__role not in ['member', 'leader'])\
            or ('L' in self.__do and self.__role != 'leader')\
            or ('F' in self.__do and self.__role not in['advisor', 'faculty'])\
            or ('A' in self.__do and self.__role != 'advisor'):
            raise PermissionError
        
        if self.__do == 'S1' or self.__do == 'F1':
            self.__decide_request()
        
        elif self.__do =='S2':
            self.__become_leader()
        
        elif self.__do == 'L1':
            self.__recruit()
        
        elif self.__do == 'M1':
            self.__update_project_title()

    def __decide_request(self):
        while True:
            project_id = input('Please input your Project ID. Or press ENTER twice to exit: ')
            decision = input('Please input your decision (Accepted/Reject). Or press ENTER to exit: ').lower()
            if project_id == '' or decision == '':
                break
            try:
                if self.__role == 'student':
                    self.__member_request.decide(self.__id, project_id, decision, self.__database.search('login'), self.__projects)
                elif self.__role == 'faculty':
                    self.__advisor_request.decide(self.__id, project_id, decision, self.__database.search('login'), self.__projects)
            except ValueError:
                print('Please enter valid project id or choice')
                continue
            break


    def __become_leader(self):
        title = input('Enter your project\'s title: ')
        self.__projects.create(title, self.__id, self.__database.search('login'))
        print('Project Created. Please restart the program.')
        raise KeyboardInterrupt

    def __recruit(self):
        project_id = self.__projects.find_dict('leader', self.__id)['ProjectID']
        people_table = self.__database.search('login').join(self.__database.search('persons'), 'ID')
        check = {'member': 'student', 'advisor' : 'faculty'}
        recruit_list = []
        while True:
            role = input('Please enter a role that you want to recruit: ').lower()
            if role not in ['advisor', 'member']:
                print('Please enter valid role')
                continue
            break

        people = people_table.filter(lambda x: x['role'] == check[role]).select(['ID', 'first', 'last'])

        for i in people:
            print(i)

        while True:
            recruit = input('Type the ID of the person you want to request: ')
            if recruit == '':
                break
            elif recruit not in [i['ID'] for i in people] :
                print('The person you tried to recruit does not exist. Please try again')
                continue
            elif recruit in recruit_list:
                continue
            recruit_list.append(recruit)
        for i in recruit_list:
            if role == 'member':
                self.__member_request.request(project_id, i)
            elif role == 'advisor':
                self.__advisor_request.request(project_id, i)


    def __update_project_title(self):
        project_id = self.__find_project_id()
        title = input('Enter your project\'s title: ')
        self.__projects.update(project_id, 'title', title)


    def __find_project_id(self):
        x = self.__projects.find_dict('leader', self.__id)
        y = self.__projects.find_dict('member1', self.__id)
        z = self.__projects.find_dict('member2', self.__id)
        if x == None:
            return y['ProjectID']
        elif y == None and x == None:
            return z['ProjectID']
        return x['ProjectID']
    
    def __give_final_approval(self):
        project_id = self.project.find_dict('advisor', self.__id)['Project_ID']
        self.__projects.update(project, 'status', 'finished')

# the code below is for testing purposes
if __name__ == '__main__':
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
