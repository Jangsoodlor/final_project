class Leader:
    def __init__(self, id) -> None:
        self.id = id
        self.project = []

    def create_project(self, title, advisor, project_table):
        self.project = {}
        self.project['ProjectID'] = len(project_table.table)
        self.project['Title'] = title
        self.project['Lead'] = self.id
        self.project['Member1'] = None
        self.project['Member2'] = None
        self.project['Advisor'] = None
        self.project['Status'] = 'pending'
        project_table.insert(self.project)
        
    def member_request(self, persons_table, member_pending_table):
        student = persons_table.filter(lambda x: x['type'] == student).select(['ID', 'fist', 'last'])
        print('Available Students')
        for i in student:
            print(i)
        while True:
            recruit = input('Type the ID of who do you want to request, or type EXIT to exit')