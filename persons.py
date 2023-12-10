class Container:
    def __init__(self, table) -> None:
        self._table = table

    @property
    def get_table(self):
        return self._table
    
    def __str__(self) -> str:
        return str(self._table)


class Request(Container):
    """_summary_
    This class do everything which relates to doing requests and dealing with
    the request table.
    """
    def __init__(self, table) -> None:
        super().__init__(table)

    def request(self, project_id, people_table, role):
        """_summary_

        This function is for sending requests to both member and advisors.
        As well as returning status of those requests.
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
            # TODO find a way to also append to_be_advisor
            temp_dict['to_be_member'] = i
            temp_dict['response'] = None
            temp_dict['response_date'] = None
            self._table.insert(temp_dict)

    def status(self, project_id, role):
        print(f'status for {role} recruitment: ')
        for i in self._table.filter(lambda x: x['ProjectID'] == project_id).table:
            print(i)

    def view(self, person_id, to_be):
        for i in self._table.filter(lambda x: x[to_be] == person_id and x['response'] == None).table:
            print(i)

    def decide(self, person_id, role, project_id, decision, login_table=None, project_obj=None):
        #TODO MAYBE re-wrote it so that it somehow also update the project table.
        #TODO change True-False to Y-N. This is to reduce the lines needed for the Main class in the future.
        import datetime
        to_be = 'to_be_' + role
        if decision.lower() == 'yes':
            import datetime
            # TODO IMPORTANT also implement to_be_advisor
            self._table.update(to_be, person_id, 'response', 'Accepted')
            login_table.update('ID', person_id, 'role', role)
            project_obj.update(project_id, role, person_id)
        else:
            self._table.update('to_be_member', person_id, 'response', 'Rejected')
        self._table.update('to_be_member', person_id, 'response_date', datetime.datetime.now())


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
        temp_dict['status'] = 'Pending'
        self._table.insert(temp_dict)
        login_table.update('ID', leader_id, 'role', 'leader')
    
    def __find_dict(self, key, args):
        return self._table.filter(lambda x: x[key] == args).table[0]
        
    def get_id(self, key, args):
        return self.__find_dict(key, args)['ProjectID']
    
    def update(self, project_id, key_update, val_update):
        #TODO fix update procedure go boom
        project_dict = self.__find_dict('ProjectID', project_id)
        if key_update == 'member' and project_dict['member1'] != None:
            key_update =='member2'
        elif key_update == 'member' and project_dict['member1'] == None:
            key_update == 'member1'
        self._table.update('ProjectID', project_id, key_update, val_update)
        
        
# the code below is for testing purposes
if __name__ == '__main__':
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
    print(project_table)
    print(login.filter(lambda x: x['role'] == 'leader'))
    member_request.request(project_table.get_id('leader', '2567260'), login.join(person, 'ID'), 'student')
    # member_request.view('5086282', 'to_be_member')
    # member_request.view('7998314', 'to_be_member')
    # member_request.view('4850789', 'to_be_member')
    # member_request.status('1', 'member')
    # print(member_request)
    #TODO fix update procedure go boom
    # for i in member_request.get_table.table:
    #     print(i)
    print(project_table)
        


    