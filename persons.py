class Leader:
    def __init__(self, id, project_table) -> None:
        self.leader_id = id
        project = project_table.filter(lambda x: x['Lead'] == self.leader_id).table
        if project == []:
            self.project = {}
            self.project_id = None
        else:
            self.project = project[0]
            self.project_id = self.project['ProjectID']

    def create_project(self, title, project_table):
        self.project_id = str(len(project_table.table) + 1)
        self.project['ProjectID'] = self.project_id
        self.project['Title'] = title
        self.project['Lead'] = self.leader_id
        self.project['Member1'] = None
        self.project['Member2'] = None
        self.project['Status'] = 'Pending'
        project_table.insert(self.project)

    def request(self, login_table, table_to_append, role):
        people = login_table.filter(lambda x: x['role'] == role).select(['ID', 'fist', 'last'])
        print('Available '+ role)
        for i in people:
            print(i)
        recruit_list = []
        while True:
            recruit = input('Type the ID of who do you want to request, or type exit to exit')
            if recruit == 'exit'.lower():
                break
            recruit_list.append(recruit)
        for i in recruit_list:
            temp_dict = {}
            temp_dict['ProjectID'] = self.project_id
            temp_dict['to_be_member'] = i
            temp_dict['Response'] = None
            temp_dict['Response_date'] = None
            table_to_append.insert(temp_dict)

    def request_status(self, request_table, role):
        print(f'Status for {role} recruitment: ')
        for i in request_table.filter(lambda x: x['ProjectID'] == self.project_id):
            print(i)
