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
    
    def find_dict(self, key, args):
        try:
            return self._table.filter(lambda x: x[key] == args).table[0]
        except IndexError:
            return None


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
        elif 'evaluator' in self._table.table_name:
            return 'evaluator'

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
                if ((role == 'member' and i['member1'] != '' and i['member2'] != '')\
                    or (role == 'advisor' and i['advisor'] != ''))\
                    and self.__get_role != 'evaluator':
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

    def update(self, project_id, key_update, val_update):
        project_dict = self.find_dict('ProjectID', project_id)
        if key_update == 'member' and project_dict['member1'] != '':
            key_update ='member2'
        elif key_update == 'member' and project_dict['member1'] == '':
            key_update = 'member1'
        self._table.update('ProjectID', project_id, key_update, val_update)


class Evaluate(Container):
    def __init__(self,project_to_eval_table, evaluator_id, project_id = None) -> None:
        # Ask the evaluator what project he/she wants to evaluate from the main class
        # Assuming new attributes are appended from the main class already
        # And the request handling will be done in the main class
        super().__init__(project_to_eval_table)
        self.__project_id = project_id
        self.__eval_id = evaluator_id

    def eval_me(self):
        return_list = []
        if len(self._table.table) != 0:
            for i in self._table.table:
                for key in i:
                    if i[key] == self.__eval_id and key != 'advisor':
                        return_list.append(i)
        return return_list

    def print_no_eval_project(self):
        print('Projects that needs evaluator:')
        for i in self._table.table:
            if i['evaluator1'] == ''\
            and i['evaluator2'] == ''\
            and i['evaluator3'] == '':
                print(i)
    
    @property
    def project_id(self):
        return self.__project_id

    @project_id.setter
    def project_id(self, val):
        self.__project_id = val

    def give_score(self, score):
        project = self.find_dict('ProjectID', self.__project_id)
        for key in project:
            if key == self.__eval_id:
                project[f'{key}_score'] = score
                print('Successfully given score')

        count = 0
        for i in range(3):
            if project[f'evaluator{i+1}_score'] != '':
                count += 1
        if count == 3:
            project['status'] == 'evaluated'
                


class Main:
    def __init__(self, id, role, database) -> None:
        self.__id = id
        self.__role = role
        self.__database = database
        self.__member_request = Request(self.__database.search('member_pending_request'))
        self.__advisor_request = Request(self.__database.search('advisor_pending_request'))
        self.__project_to_eval = Evaluate(self.__database.search('project_to_eval'), self.__id)
        self.__projects = Project(self.__database.search('project'))
        
        if self.__role == 'student':
            self.__member_request.view(self.__id)
            print('\n' + 'Avialable Methods')
            print("S1: Accept/Reject Member Requests")
            print("S2: Become a Leader and Create a New Project")

        elif self.__role == 'member':
            self.__member__print()
            print('Project Status')
            print(self.__projects.find_dict('ProjectID', self.__find_project_id()))
            print()
            print('Member Request Status')
            self.__member_request.status(self.__find_project_id())
            print()
            print('Advisor Request Status')
            self.__advisor_request.status(self.__find_project_id())
            print('\n' + 'Avialable Methods')
            print("M1: Modify the Project's title")

        elif self.__role == 'leader':
            self.__member__print()
            print('\n' + 'Avialable Methods')
            print("L1: Requests Member/Advisor")
            print("M1: Modify the Project's title")

        elif 'faculty' in self.__role:
            self.__advisor_request.view(self.__id)
            print('\n' + 'Avialable Methods')
            print("F1: Accept/Reject Advisor Requests")

        elif 'advisor' in self.__role:
            print('\n' + 'Avialable Methods')
            print("A1: Approve the Project for Evaluation")
            print("A2: GIVE FINAL APPROVAL FOR THE PROJECT")

        if 'evaluator' in self.__role:
            print('E1: Give score to project')
        
        elif self.__role == 'admin':
            print('D1: choose evaluator')

        print()
        self.__do = (input('Please choose one of the Avialable Methods above to proceed. Or type exit to exit: ')).capitalize()
        print('Pressing ENTER without inputting anything will abort the operation unless stated otherwise.')
        if self.__do == 'Exit':
            raise KeyboardInterrupt
        elif len(self.__do) != 2:
            raise ValueError
        
        if ('S' in self.__do and self.__role != 'student')\
            or ('M' in self.__do and self.__role not in ['member', 'leader'])\
            or ('L' in self.__do and self.__role != 'leader')\
            or ('F' in self.__do and self.__role not in ['advisor', 'faculty', 'advisor and evaluator', 'faculty and evaluator'])\
            or ('A' in self.__do and self.__role not in ['advisor', 'advisor and evaluator'])\
            or ('E' in self.__do and 'evaluator' not in self.__role)\
            or ('D' in self.__do and self.__role != 'admin'):
            raise PermissionError
        
        if self.__do == 'S1' or self.__do == 'F1':
            self.__decide_request()
        
        elif self.__do =='S2':
            self.__become_leader()
        
        elif self.__do == 'L1':
            self.__recruit()
        
        elif self.__do == 'M1':
            self.__update_project_title()
        
        elif self.__do == 'A1':
            self.__send_project_for_eval()
    
        elif self.__do == 'A2':
            self.__give_final_approval()
            
        elif self.__do == 'E1':
            self.__give_score()
        
        elif self.__do == 'D1':
            self.__choose_evaluator()


    def __member__print(self):
            print('Project Status')
            print(self.__projects.find_dict('ProjectID', self.__find_project_id()))
            print()
            print('Member Request Status')
            self.__member_request.status(self.__find_project_id())
            print()
            print('Advisor Request Status')
            self.__advisor_request.status(self.__find_project_id())
    
    def __find_project_id(self):
        x = self.__projects.find_dict('leader', self.__id)
        y = self.__projects.find_dict('member1', self.__id)
        z = self.__projects.find_dict('member2', self.__id)
        if x == None:
            return y['ProjectID']
        elif y == None and x == None:
            return z['ProjectID']
        return x['ProjectID']
    
    def __decide_request(self):
        while True:
            print('pressing ENTER without inputting anything project_id and/or decision will abort the process')
            project_id = input('Please input your Project ID: ')
            if project_id == '':
                break
            decision = input('Please input your decision (Accepted/Rejected). DONT FORGET THE "ED" AT THE END: ').lower()
            if decision == '':
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
            recruit = input('Type the ID of the person you want to request, \
                        Press ENTER without inputting anything to stop: ')
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

    def __send_project_for_eval(self):
        self.__projects.get_table.update('advisor', self.__id, 'status', 'waiting for evaluation')
        import copy
        temp_dict = copy.deepcopy(self.__projects.find_dict('advisor', self.__id))
        temp_dict['evaluator1'] = ''
        temp_dict['evaluator2'] = ''
        temp_dict['evaluator3'] = ''
        temp_dict['evaluator1_score'] = ''
        temp_dict['evaluator2_score'] = ''
        temp_dict['evaluator3_score'] = ''
        self.__project_to_eval.get_table.table.append(temp_dict)
        print('Successfully send the project for evaluation.')

    def __give_score(self):
        for i in self.__project_to_eval.eval_me():
            print(i)
        while True:
            print('If enter invalid project ID, your score will not be given.')
            project_id = input('Please enter Project ID: ')
            try:
                score = int(input('Please give score in integers: '))
                self.__project_to_eval.project_id = project_id
                self.__project_to_eval.give_score(score)
            except ValueError:
                print('Please enter a valid score')
                continue
            break

    def __choose_evaluator(self):
        self.__project_to_eval.print_no_eval_project()
        while True:
            project_id = input('Please enter project ID: ')
            if project_id == '':
                raise ValueError
            break
        print()
        advisor_id = self.__projects.find_dict('ProjectID', project_id)['advisor']
        print('Availale Evaluators')
        people = self.__database.search('persons').filter(lambda x : x['type'] == 'faculty' 
                                                          and x['ID'] != advisor_id).table
        for i in people:
                print(i)
        recruit_list  = []
        count = 0
        while count < 3:
        # make the loop limited to 3 rounds and a way to cancel the procedure.
            recruit = input('Type the ID of the person you want to choose as evaluator, \
type exit to abort: ')
            if recruit == 'exit':
                break
            elif recruit not in [i['ID'] for i in people] :
                print('The person you tried to recruit does not exist. Please try again')
                continue
            elif recruit in recruit_list:
                continue
            recruit_list.append(recruit)
            count += 1
        
        if len(recruit_list) == 3:
            for i in range(3):
                self.__project_to_eval.get_table.filter(lambda x: x['ProjectID'] == project_id)\
                .table[0][f'evaluator{i+1}'] = recruit_list[i]
            for i in self.__database.search('login').table:
                if i['ID'] in recruit_list and 'evaluator' not in i['role']:
                    i['role'] += ' and evaluator'
            print('Successfully added evaluator')
        

    def __give_final_approval(self):
        while True:
            project_dict = self.__projects.find_dict('advisor', self.__id)
            if project_dict['status'] != 'evaluated':
                print('Please send the project for evaluation first')
                break
            confirm = input('Are you sure (y/n): ')
            if 'y' not in confirm.lower():
                break
            project_id = project_dict['Project_ID']
            self.__projects.update(project_id, 'status', 'finished')


if __name__ == '__main__':
    pass
    # the code below is for testing purposes
    # project = dp.Table('project', [])
    # login = dp.Table('login', dp.ReadCSV(os.path.join('database', 'login.csv')).fetch)
    # person = dp.Table('login', dp.ReadCSV(os.path.join('database', 'persons.csv')).fetch)
    # member_request = Request(dp.Table('member_request', []))
    # advisor_request = Request(dp.Table('advisor_request', []))
    # project_table = Project(dp.Table('Project', []))
    
    # print(member_request)
    # print(project_table)

    # project_table.create('Magic Wand', '2567260', login)
    # project_table.create('Magic Eraser', '9898118', login)
    # print(project_table)
    # print(login.filter(lambda x: x['role'] == 'leader'))
