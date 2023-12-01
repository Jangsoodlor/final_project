class Leader:
    def __init__(self, id, project_table) -> None:
        self.id = id
        project = project_table.filter(lambda x: x['Lead'] == self.id).table
        if project == []:
            self.project = {}
            self.project_id = None
        else:
            for i in project_table.table:
                if i['Lead'] == self.id:
                    self.project = i
            self.project_id = self.project['ProjectID']

    def create_project(self, title, project_table):
        self.project_id = str(len(project_table.table) + 1)
        self.project['ProjectID'] = self.project_id
        self.project['Title'] = title
        self.project['Lead'] = self.id
        self.project['Member1'] = None
        self.project['Member2'] = None
        self.project['Status'] = 'Pending'
        project_table.insert(self.project)

    def request(self, people_table, request_table, role):
        """_summary_

        This function is for sending request to both member and advisor.
        people_table : login.join(person, 'ID')
        """
        people = people_table.filter(lambda x: x['role'] == role).select(['ID', 'fist', 'last'])
        print('Available '+ role)
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
            temp_dict['ProjectID'] = self.project_id
            temp_dict['to_be_member'] = i
            temp_dict['Response'] = None
            temp_dict['Response_date'] = None
            request_table.insert(temp_dict)

    def request_status(self, request_table, role):
        print(f'Status for {role} recruitment: ')
        for i in request_table.filter(lambda x: x['ProjectID'] == self.project_id).table:
            print(i)
            
    def __str__(self) -> str:
        return f'ID: {self.id}, Project:{self.project}'
    

class Student:
    def __init__(self, id, request_table) -> None:
        self.id = id
        # Show requests, rewritten soon.
        for i in request_table.filter(lambda x: x['to_be_member'] == self.id).table:
            print(i)
    
    def become_leader(self, login_table):
        login_table.update('ID', self.id, 'role', 'leader')
        

# the code below is for testing purposes
if __name__ == '__main__':
    import database as dp
    project = dp.Table('project', [])
    login = dp.Table('login', dp.ReadCSV('login').fetch)
    person = dp.Table('login', dp.ReadCSV('persons').fetch)
    request = dp.Table('request', [])
    
    leader = Leader('2567260', project)
    print(leader)
    leader.create_project('Magic wand', project)
    print(leader)
    print(project)
    leader.request(login.join(person, 'ID'), request, 'student')
    print(request)
    print(leader.request_status(request, 'student'))
    
    student = Student('9898118', request)
    # student.become_leader(login)
    # print(login.filter(lambda x: x['role'] == 'leader'))
    