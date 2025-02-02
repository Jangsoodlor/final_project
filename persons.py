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
        print requests from all projects that recruited this person.
        """
        print('Requests')
        to_be = 'to_be_' + self.__get_role
        for i in self._table.filter(lambda x: x[to_be] == person_id).table:
            print(i)

    def view_return(self, person_id):
        """_summary_
        returns ProjectID of projects that recruited this person.
        """
        to_be = 'to_be_' + self.__get_role
        return [i['ProjectID'] for i in self._table.filter(lambda x: x[to_be] == person_id).table]

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
            role1 = role
            if len(login_table.filter(lambda x: x['ID'] == person_id)\
            .filter(lambda x: 'evaluator' in x['role']).table) == 1:
                role1 = ' advisor and evaluator'
            login_table.update('ID', person_id, 'role', role1)
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
            raise InterruptedError


class Project(Container):
    """_summary_
    This class does everything related to project manipulation
    """
    def __init__(self, table) -> None:
        super().__init__(table)

    def create(self, title, leader_id, login_table):
        temp_dict = {}
        temp_dict['ProjectID'] = str(len(self._table.table) + 1)
        temp_dict['title'] = title
        temp_dict['leader'] = leader_id
        temp_dict['member1'] = ''
        temp_dict['member2'] = ''
        temp_dict['advisor'] = ''
        temp_dict['status'] = 'pending'
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
                print(self._table.filter(lambda x: x['ProjectID'] == i['ProjectID'])\
                    .select(['ProjectID', 'title', 'leader', 'member1', 'member2', 'advisor']))

    @property
    def project_id(self):
        return self.__project_id

    @project_id.setter
    def project_id(self, val):
        self.__project_id = val

    def give_score(self, score):
        print('giving score...')
        project = self.find_dict('ProjectID', self.__project_id)
        if project['evaluator1_score'] == '' or project['evaluator2_score']== ''\
        or project['evaluator3_score'] == '':
            if project['evaluator1'] == self.__eval_id:
                project['evaluator1_score'] = score
            elif project['evaluator2'] == self.__eval_id:
                project['evaluator2_score'] = score
            elif project['evaluator3'] == self.__eval_id:
                project['evaluator3_score'] = score
            else:
                raise ValueError
        else:
            raise ValueError

        if project['evaluator1_score'] != ''\
        and project['evaluator2_score'] != ''\
        and project['evaluator3_score'] != ''\
        and project['status'] == 'waiting for evaluation':
            print('All evaluators have evaluated the project.')
            project['status'] = 'evaluated. waiting for final approval.'


class Main:
    def __init__(self, id, role, database) -> None:
        self.__id = id
        self.__role = role
        self.__database = database
        self.__member_request = Request(self.__database.search('member_pending_request'))
        self.__advisor_request = Request(self.__database.search('advisor_pending_request'))
        self.__project_to_eval = Evaluate(self.__database.search('project_to_eval'), self.__id)
        self.__projects = Project(self.__database.search('project'))
        print()
        if self.__role == 'student':
            self.__member_request.view(self.__id)
            print('\n' + 'Available Options')
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
            print('\n' + 'Available Options')
            print("M1: Modify the Project's title")

        elif self.__role == 'leader':
            self.__member__print()
            print('\n' + 'Available Options')
            print("L1: Requests Member/Advisor")
            print("M1: Modify the Project's title")

        elif 'faculty' in self.__role:
            self.__advisor_request.view(self.__id)
            print('\n' + 'Available Options')
            print("F1: Accept/Reject Advisor Requests")

        elif 'advisor' in self.__role:
            print('Project Status')
            print(self.__projects.find_dict('advisor', self.__id))
            print('\n' + 'Available Options')
            print("A1: Approve the Project for Evaluation")
            print("A2: View Evaluation Scores")
            print("A3: GIVE FINAL APPROVAL FOR THE PROJECT")

        if 'evaluator' in self.__role:
            print('E1: Give score to project')

        elif self.__role == 'admin':
            self.__print_database()
            print('D1: View projects that needs evaluators and Choose evaluators')
            print('D2: Insert new dict to table: ')
            print('D3: Edit an existing dict in table: ')
            print('D4: Delete an existing dict in table: ')
            print('D5: DELETE TABLE')
            print('D6: RESET PROGRAM STATE')

        print('Type :x or :wq to SAVE and exit ', end = '')
        print('OR type :q! to quit WITHOUT saving')
        self.__do = (input('Please choose one of the Available Options above to proceed: ')).capitalize()
        if self.__do == ':x' or self.__do == ':wq':
            raise InterruptedError
        elif self.__do == ':q!':
            raise KeyboardInterrupt
        elif len(self.__do) != 2:
            raise ValueError

        if ('S' in self.__do and self.__role != 'student')\
        or ('M' in self.__do and self.__role not in ['member', 'leader'])\
        or ('L' in self.__do and self.__role != 'leader')\
        or ('F' in self.__do and 'faculty' not in self.__role)\
        or ('A' in self.__do and 'advisor' not in self.__role)\
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
            self.__eval_status()

        elif self.__do == 'A3':
            self.__give_final_approval()

        elif self.__do == 'E1':
            self.__give_score()

        elif self.__do == 'D1':
            self.__choose_evaluator()

        elif self.__do == 'D2':
            self.__insert_dict_to_table()

        elif self.__do == 'D3':
            self.__edit_dict_in_table()

        elif self.__do == 'D4':
            self.__delete_dict_in_table()

        elif self.__do == 'D5':
            self.__clear_table()

        elif self.__do == 'D6':
            self.__reset()


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
        if x == None and y!=None:
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
                elif 'faculty' in self.__role:
                    self.__advisor_request.decide(self.__id, project_id, decision, self.__database.search('login'), self.__projects)
            except ValueError:
                print('Please enter valid project id or choice')
                continue
            break

    def __become_leader(self):
        title = input('Enter your project\'s title: ')
        self.__projects.create(title, self.__id, self.__database.search('login'))
        for i in self.__member_request.view_return(self.__id):
            self.__member_request.decide(self.__id, i, 'rejected')
        print('Project Created. Please restart the program.')
        raise InterruptedError

    def __recruit(self):
        project_id = self.__projects.find_dict('leader', self.__id)['ProjectID']
        people_table = self.__database.search('login').join(self.__database.search('persons'), 'ID')
        check = {'member': 'student', 'advisor' : 'faculty'}
        recruit_list = []
        project = self.__projects.get_table.filter(lambda x: x['leader'] == self.__id).table[0]
        while True:
            role = input('Please enter a role that you want to request (member/advisor): ').lower()
            if role not in ['advisor', 'member']:
                print('Please enter valid role before continuing.')
                continue
            if (project['member1'] != '' and project['member2'] != '' and role == 'member')\
            or (role == 'advisor' and project['advisor'] != ''):
                print('Why?')
                raise ValueError
            break
        people = people_table.filter(lambda x: check[role] in x['role']).select(['ID', 'first', 'last'])
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
            print(f'Requesting {i}')
            if role == 'member':
                self.__member_request.request(project_id, i)
            elif role == 'advisor':
                self.__advisor_request.request(project_id, i)

    def __update_project_title(self):
        project_id = self.__find_project_id()
        title = input('Enter your project\'s title: ')
        self.__projects.update(project_id, 'title', title)
        print(f'Project title successfully updated to {title}')

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
        print(f"+----------+---------------------+--------+--------+--------+--------+")
        print(f"|Project ID|    Project Title    | Leader | Member1| Member2| Advisor|")
        print(f"+----------+---------------------+--------+--------+--------+--------+")
        for i in self.__project_to_eval.eval_me():
            if i['status'] == 'waiting for evaluation':
                print(f"| {i['ProjectID']:<9}|{i['title']:^20} |{i['leader']:>8}|", end = '')
                print(f"{i['member1']:>8}|{i['member2']:>8}|{i['advisor']:>8}|")
                print(f"+----------+---------------------+--------+--------+--------+--------+")
        while True:
            try:
                project_id = input('Please enter Project ID, or type exit to exit: ')
                if project_id == 'exit':
                    break
                score = int(input('Please give score in integers between 0 to 10, or type exit to exit: '))
                if score == 'exit':
                    break
                if score < 0 or score > 10:
                    raise ValueError
                self.__project_to_eval.project_id = project_id
                self.__project_to_eval.give_score(score)
            except (ValueError, TypeError):
                print('Please enter a valid score or project')
                continue
            if self.__project_to_eval.find_dict('ProjectID', project_id)['status'] == 'evaluated. waiting for final approval.':
                self.__projects.update(project_id, 'status', 'evaluated. waiting for final approval.')
            break

    def __eval_status(self):
        project = self.__project_to_eval.find_dict('advisor', self.__id)
        if project != None:
            print('Evaluation Status', end=': ')
            print(project['status'])
            if project['status'] == 'evaluated. waiting for final approval.':
                print(f'Score1: {project["evaluator1_score"]}')
                print(f'Score2: {project["evaluator2_score"]}')
                print(f'Score3: {project["evaluator3_score"]}')
        else:
            print('Please send the project to evaluate first')

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
                and x['ID'] != advisor_id).select(['ID', 'first', 'last'])
        for i in people:
            print(i)
        recruit_list  = []
        count = 0
        while count < 3:
        # make the loop limited to 3 rounds and a way to cancel the procedure.
        # sorry for broken english here
            recruit = input(f'Type the ID of the {count+1}th evaluator, \
type exit to cancel: ')
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
            if project_dict['status'] != 'evaluated. waiting for final approval.':
                print('Please send the project for evaluation first')
                break
            confirm = input('Approve or not? (y/n): ').lower()
            project_id = project_dict['ProjectID']
            if 'y' in confirm:
                self.__projects.update(project_id, 'status', 'finished')
                self.__project_to_eval.get_table.update('ProjectID', project_id, 'status', 'finished')
                print('PROJECT APPROVED')
            elif 'n' in confirm:
                self.__projects.update(project_id, 'status', 'pending')
                if len(self.__project_to_eval.get_table.table) == 1:
                    self.__project_to_eval.get_table.table.clear()
                else:
                    self.__project_to_eval.get_table.table.remove(self.__project_to_eval.find_dict('advisor', self.__id))
                print('PROJECT NOT APPROVED')
            break

    def __print_database(self):
        print('Databases: ')
        self.__database.print_tables()
        print()

    def __insert_dict_to_table(self):
        table = self.__database.search(input('Please enter table: '))
        temp_dict = {}
        print('press ENTER without inputting for empty string')
        for key in table.table[0]:
            val = input(f'Please input value for {key}: ') or ''
            temp_dict[key] = val
        table.insert(temp_dict)
        print('done')

    def __edit_dict_in_table(self):
        table = self.__database.search(input('Please enter table: '))
        for i in table.table:
            print(i)
        key_main = input('Please enter main key: ')
        val_main = input('Please enter main value: ')
        key_update = input('Please enter key that you want to update: ')
        val_update = input('Please enter val that you want to update: ')
        table.update(key_main, val_main, key_update, val_update)
        print('done')

    def __delete_dict_in_table(self):
        table = self.__database.search(input('Please enter table: '))
        for i in table.table:
            print(i)
        key_main = input('Please enter main key: ')
        val_main = input('Please enter main value: ')
        for i in table.table:
            if i[key_main] == val_main:
                table.table.remove(i)
        print('done')

    def __clear_table(self):
        self.__database.search(input('Please enter table: ')).table.clear()
        print('done')

    def __reset(self):
        self.__database.search('member_pending_request').table.clear()
        self.__database.search('advisor_pending_request').table.clear()
        self.__database.search('project').table.clear()
        self.__database.search('project_to_eval').table.clear()
        for i in self.__database.search('login').table:
            if 'advisor' in i['role'] or 'evaluator' in i['role']:
                i['role'] = 'faculty'
            elif i['role'] in ['member', 'leader']:
                i['role'] = 'student'
        print('done')


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
