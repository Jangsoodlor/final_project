class Request:
    def __init__(self, request_table) -> None:
        self.request_table = table

    def request(self, project_id, people_table, role):
        """_summary_

        This function is for sending request to both member and advisor.
        people_table : login.join(person, 'ID')
        """
        people = people_table.filter(lambda x: x['role'] == role).select(['ID', 'first', 'last'])
        print(f'Available {role} for recruitment')
        for i in people:
            print(i)
        recruit_list = []
        while True:
            recruit = input('Type the ID of the person you want to request, or press ENTER to exit: ')
            if recruit == '':
                break
            recruit_list.append(recruit)
        for i in recruit_list:
            temp_dict = {}
            temp_dict['ProjectID'] = project_id
            temp_dict['to_be_member'] = i
            temp_dict['response'] = None
            temp_dict['response_date'] = None
            self.request_table.insert(temp_dict)

    def status(self, project_id, role):
        print(f'status for {role} recruitment: ')
        for i in self.request_table.filter(lambda x: x['ProjectID'] == project_id).table:
            print(i)

    def view(self, person_id):
        for i in self.request_table.filter(lambda x: x['to_be_member'] == person_id and x['response'] == None).table:
            print(i)

    def decide(self, person_id, login_table, role, decision):
        #TODO re-wrote it so that it somehow also update the project table.
        #TODO change True-False to Y-N. This is to reduce the lines needed for the Main class in the future.
        if decision == True:
            import datetime
            self.request_table.update('to_be_member', person_id, 'response', 'Accepted')
            login_table.update('ID', person_id, 'role', role)
        else:
            self.request_table.update('to_be_member', person_id, 'response', 'Rejected')
        self.request_table.update('to_be_member', person_id, 'response_date', datetime.datetime.now())
    
    def __str__(self) -> str:
        return str(self.request_table)


class Project:
    def __init__(self, project_table) -> None:
        self.__project_table = project_table
    
    def find_project_dict(self, person_id, role):
        return self.__project_table.filter(lambda x: x[role] == person_id).table[0]
    
    def create(self, title, leader_id):
        #TODO write AssertionError
        temp_dict = {}
        temp_dict['ProjectID'] = str(len(self.__project_table.table) + 1)
        temp_dict['title'] = title
        temp_dict['leader'] = leader_id
        temp_dict['member1'] = None
        temp_dict['member2'] = None
        temp_dict['status'] = 'Pending'
        self.__project_table.insert(temp_dict)
        
    def update(self, project_id, key, args):
        project_dict = self.__project_table.filter(lambda x: x['ProjectID'] == project_id).table[0]
        if key == 'member1' and project_dict['member1'] != None:
            self.update(self, project_id, args, 'member2')
        project_dict[key] = args
    

# class Leader:
#     def __init__(self, id, project_table) -> None:
#         self.__id = id
        # project = project_table.filter(lambda x: x['lead'] == self.id).table
        # if project == []:
        #     self.project = {}
        #     self.project_id = None
        # else:
        #     for i in project_table.table:
        #         if i['lead'] == self.__id:
        #             self.project = i
        #     self.project_id = self.project['ProjectID']

    @property
    def id(self):
        return self.__id
    
    # def create_project(self, title, project_table):
    #     self.project_id = str(len(project_table.table) + 1)
    #     self.project['ProjectID'] = self.project_id
    #     self.project['title'] = title
    #     self.project['leader'] = self.__id
    #     self.project['member1'] = None
    #     self.project['member2'] = None
    #     self.project['status'] = 'Pending'
    #     project_table.insert(self.project)

    # def __str__(self) -> str:
    #     return f'ID: {self.__id}, Project:{self.project}'


class Student:
    def __init__(self, id) -> None:
        self.__id = id
        
    @property
    def id(self):
        return self.__id

    def become_leader(self, login_table, member_request):
        login_table.update('ID', self.__id, 'role', 'leader')
        member_request.decide(self.__id, login_table, 'member', False)


# the code below is for testing purposes
if __name__ == '__main__':
    import database as dp
    project = dp.Table('project', [])
    login = dp.Table('login', dp.ReadCSV('login').fetch)
    person = dp.Table('login', dp.ReadCSV('persons').fetch)
    member_request = Request(dp.Table('member_request', []))
    advisor_request = Request(dp.Table('advisor_request', []))
    project_table = Project(dp.Table('Project', []))
    
    leader = Leader('2567260', project)
    print(leader)
    # leader.create_project('Magic wand', project)
    print(leader)
    print(project)
    member_request.request('1', login.join(person, 'ID'), 'student')
    print()
    print(member_request.status('1', 'member'))
    # advisor_request.request('1', login.join(person, 'ID'), 'faculty')
    # print()
    # print(advisor_request.status('1', 'advisor'))

    student = Student('5086282')
    member_request.view('5086282')




    