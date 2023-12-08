class Request:
    """_summary_
    This class do everything which relates to doing requests
    """
    def __init__(self, request_table) -> None:
        self.__request_table = request_table

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
            self.__request_table.insert(temp_dict)

    def status(self, project_id, role):
        print(f'status for {role} recruitment: ')
        for i in self.__request_table.filter(lambda x: x['ProjectID'] == project_id).table:
            print(i)

    def view(self, person_id):
        for i in self.__request_table.filter(lambda x: x['to_be_member'] == person_id and x['response'] == None).table:
            print(i)

    def decide(self, person_id, login_table, role, decision):
        #TODO MAYBE re-wrote it so that it somehow also update the project table.
        #TODO change True-False to Y-N. This is to reduce the lines needed for the Main class in the future.
        if decision == True:
            import datetime
            # TODO IMPORTANT also implement to_be_advisor
            self.__request_table.update('to_be_member', person_id, 'response', 'Accepted')
            login_table.update('ID', person_id, 'role', role)
        else:
            self.__request_table.update('to_be_member', person_id, 'response', 'Rejected')
        self.__request_table.update('to_be_member', person_id, 'response_date', datetime.datetime.now())
    
    def __str__(self) -> str:
        return str(self.__request_table)


class Project:
    """_summary_
    This class does everything related to project manipulatoni
    """
    def __init__(self, project_table) -> None:
        self.__project_table = project_table
    
    def find_project_dict(self, key, args):
        return self.__project_table.filter(lambda x: x[key] == args).table[0]
    
    def create(self, title, leader_id):
        #TODO write AssertionError if a leader already have a project
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
    
class Main:
    def __init__(self) -> None:
        pass

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
        
    member_request.view('5086282')

    # leader = Leader('2567260', project)
    # print(leader)
    # leader.create_project('Magic wand', project)
    # print(leader)
    # print(project)
    # member_request.request('1', login.join(person, 'ID'), 'student')
    # print()
    # print(member_request.status('1', 'member'))
    # advisor_request.request('1', login.join(person, 'ID'), 'faculty')
    # print()
    # print(advisor_request.status('1', 'advisor'))

    # student = Student('5086282')



    