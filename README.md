# Final project for 2023's 219114/115 Programming I
* Starting files for part 1
  - database.py
  - project_manage.py
  - persons.csv

# Table of Contents
- [Files NECESSARY to run the program](#files-necessary-to-run-the-program)
- [HOW TO RUN?](#how-to-run)
- [Classes and Functions](#classes-and-functions)
  - [Container](#class-container)
  - [Request](#class-request)
  - [Project](#class-project)
  - [Evaluate](#class-evaluate)
  - [Main](#class-main)
- [A table detailing each role and its actions](#a-table-detailing-each-role-and-its-actions)
- [Known Bugs](#known-bugs)

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
  - **run the [project_manage.py](project_manage.py) file.**

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

# A table detailing each role and its actions
Because of the way I design this program, all actions done by the user must goes through at least one method in the main class first the Main class first before going to other class
|Role|Action|Method in the Main class|Which Involves these methods in these classes|Completion Percentage|
|-|-|-|-|-|
|Advisor|View Project Status|None|find_dict in Project|100 %|
|Member, Leader|View Project Status and Requests status|__member_print|find_dict in Project, status in Request|100 %|
|Student|become leader|__become_leader|create in Project, decide in Request|100 %|
|Student, Faculty|accept/reject requests|__decide_request|decide in Request|95 %|
|Leader|Send Requests to Member and Advisors|__recruit|request in Request|100 %|
|Leader, Member|Update project title|__update_project_title|update in Project|100 %|
|Advisor|Send the project to evaluation|__send_project_for_eval|update in Projects|100 %|
|Admin|choose evaluator|__choose_evaluator|a lot of functions in Evaluate and Project classes|100 %|
|Evaluator|Give score|__give_score|a lot of functions in Evaluate and Project classes|100 %|
|Advisor|View Evaluator's score|__eval_status|find_dict in Evaluator, which inherits from Container class|100 %|
|Advisor|Give Final Approval|__give_final_approval| lot of functions in Evaluate and Project classes|100 %|
|Admin|Insert a new dict to an existing table|__insert_new_dict_to_table|None|100 %|
|Admin|Edit a dict in an existing table|__edit_dict_in_table|None|100 %|
|Admin|delete a dictionary in table|__delete_dict_in_table|None|100 %|
|Admin|Delete an entire table|__clear_table|None|100 %|
|Admin|Reset program's state|__reset|None|100 %|

# Known bugs
These are some last-minutes bugs I found:
- Cannot exit from __decide_request function unless accept or reject a valid requests
- Advisor can submit project for evaluation multiple times.
- Members and leaders can change title everytime. Even if the project is finished
- Evaluator does not lose his role when there's no more projects to evaluate. Albeit he cannot evaluate the projects that has been marked finished by the advisor anyways.
- Leader can invite members after all members have been invited. Those invites should be automatically deleted after someone accepts an offer from other groups.

These are not necessarily bugs, but are kinda intended behaviors that got implemented in a weird way:
- inputting :q! and get KeyboardInterrupted is an intended behavior. Because it's a way to skip the exit() function in [project_manage.py](project_manage.py)
- Project Title could be set as empty string.