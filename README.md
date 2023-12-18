# Final project for 2023's 219114/115 Programming I
* Starting files for part 1
  - database.py
  - project_manage.py
  - persons.csv

# Files NECESSARY to run the program:
  - database.py
  - project_manage.py
  - persons.csv
  - a database subdirectory in the program's directory. Which contains:
    - login.csv
    - persons.csv

  additionally, the program utilizes these following libraries
  - os
  - csv
  - datetime
  - copy
  all of which are standard python libraries.
  
# How to run?
  - clone or download the project
  - run the **project_manage.py** file.

# Classes and Functions
All additional classes (aside from ReadCSV, Table and Database) is in the [persons.py](persons.py) file.

## Class Container
This class is, like the name suggests, a container class. Which all the other classes except the main class inherited its attributes from.

|method|description|additional arguments taken|
|------|-----------|----------------|
|__init__|take in table object as a starting attribute|table|
|get_table|returns the table object|None|
|find_dict|returns the first dictionary which matches the key and value the user inputted|None|
|__str__|print table|None|

## Class Request
This class handled requests. Inherited attributes from container.
|method|description|additional arguments taken|
|------|-----------|---------------|
|__init__|inherits from container|either "member_request_table" or "advisor_request_table" table|
|__get_role|get the role of the user from the table's name|None|
|request|append the request into the respective tables.|project_id, recruit_id|
|status|prints all member/advisor requests of a project|project_id|
|view|prints all requests sent to a particular person|person_id|
|view_return|return a list of  ProjectID of projects that requested this person.|person_id|
|decide|handle the decision of a person on whether to join a particular project or not. And modify the login and project tables.|person_id, project_id, decision, login_table=None, project_obj=None (project_obj is an object in Project class, which is explained below)|

## Class Project
This class handles the modification of the project table. Inherits from the Container class
|method|description|additional arguments taken|
|------|-----------|---------------|
|__init__|inherits from the Container class|"project" table|
|create|creates a new project and change the role of member who started the project to leader|title, leader_id, login_table|
|update|update the project table with ProjectID as the main key|project_id, key_update, val_update|

## Class Evaluate
Inherits from the Container class. This class handles the modification of the project_to_eval table.
|method/property|description|additional arguments taken|
|------|-----------|---------------|
|__init__|inherits from the Container class with some additional arguments|"project_to_eval" table, project_id=None, evaluator_id|
|eval_me|returns a list project which the user is an evaluator|None|
|print_no_eval_project|prints projects with no evaluators|None|
|project_id|a getter and setter method. use to set project_id|project_id|
|give_score|give score to projects|score|

## Class Main
THE Main class. it's the class that receives inputs and send it to other classes. And sometimes modified the database directly. Further explanation is in the next section.

Take role, id and database. and
- Make  

# A table detailing each role and its actions
For completion percentage, please refers to [Bugs and completion percentage](#Bugs-and-completion-percentage) section.
|Role|Action|Method in the main class|Which Involves these methods in these classes|
|-|-|-|-|
|Advisor|View Project Status|None|find_dict in Project|
|Member, Leader|View Project Status and Requests status|__member_print|find_dict in Project, status in Request|
|Student|become leader|__become_leader|create in Project, decide in Request|
|Student, Faculty|accept/reject requests|__decide_request|decide in Request|
|Leader|Send Requests to Member and Advisors|__recruit|request in Request|
|Leader, Member|Update project title|__update_project_title|update in Project
|Advisor|Send the project to evaluation|__send_project_for_eval|update in Projects|
|Admin|choose evaluator|__choose_evaluator|a lot of functions in Evaluate and Project classes|
|Evaluator|Give score|__give_score|a lot of functions in Evaluate and Project classes|
|Advisor|View Evaluator's score|__eval_status|find_dict in Evaluator, which inherits from Container class|
|Advisor|Give Final Approval|__give_final_approval| lot of functions in Evaluate and Project classes|
|Admin|Insert a new dict to an existing table|__insert_new_dict_to_table|None|
|Admin|Edit a dict in an existing table|__edit_dict_in_table|None|
|Admin|delete a dictionary in table|__delete_dict_in_table|None|
|Admin|Delete an entire table|__clear_table|None|
|Admin|Reset program's state|__reset|None|

# Bugs and Completion Percentage
**Completion: 99%** (No docstring lol)
I've spent three hours finding and fixing bugs. The only bugs I can think of is IndentationError. Since I run pylint after all the debuggings. But that should be almost impossible because I rigorously checked for indentation mistakes before pushing the final commit. The other thing is the way os library handles folder and may not detect a database.

UPDATE: I actually found last-minute bugs lol
- Cannot exit from F1 and S1 functions unless accept or reject requests
- inputting :q! and get KeyboardInterrupted is an intended behavior. Because it's a way to skip the exit() function in [project_manage.py](project_manage.py)
- Advisor can submit project for evaluation multiple times.
- Members and leaders can change title everytime. Even if the project is finished
- Project Title can be empty string. **Which is a FEATURE unique to my program, not a bug.**
- Evaluator does not lose his role when there's no more projects to evaluate. Albeit he cannot evaluate the projects that has been marked finished by the advisor anyways.
- Leader can invite members after all members have been invited. Those invites should be automatically deleted after someone accepts an offer from other groups.

# Copyright Notice
Graduation Project Management System.
Copyright (C) 2023 Jangsoodlor. All Rights Reserved.

This program is part of 01219114/15 Computer Programming I Course
Semester 1 Academic Year 2566 B.E. (2023 A.D.)
Kasetsart University

DO NOT copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this Software.
UNLESS you're a Kasetsart University Computer Engineering Department's Professor or Teacher Assistant.

THERE IS NO WARRANTY FOR THE PROGRAM. IN NO EVENT WILL THE COPYRIGHT HOLDER BE LIABLE TO YOU FOR DAMAGES, 
INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE 
OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA 
OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES 
OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), 
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.