# To-Do Lists
lists of things to be implement 😭😭😭
## Databases
There shall be 5 tables with the following attributes

**Persons**
- ID
- first
- last
- type

**Login**
- ID
- username
- password
- role

**Project**
- ProjectID
- title
- leader
- member1
- member2
- advisor
- status

**Member_pending_request**
- ProjectID
- to_be_member
- response
- response_date

**Advisor_pending_request**
- ProjectID
- to_be_advisor
- response
- response_date

# What each type of person can do
Initially, there're three types of people based on the csv files provided by T.Paruj; Admin, Faculty and Student. But the program will be able to assign new roles to these people.

## Student
- See project member requests
- Accept and deny those requests.
  - If accepted, the **Project** and **Member_pending_request** tables shall be updated, _<u>denying all other requests</u>_. `login['role']`will also be updated to `'member'`
  - Otherwise, the **Member_pending_request** will be updated.
- Create a project and becomes a lead
  - update `persons['type']`and `login['role']` to leader
  - create project by appending a project dictionary with some attributes filled into the **Project** table.

  ```py
  projectID = len(project_table.table)
  ```
  - more features will be explained in the leader section.

## Leader
- See project and requests status by pulling the corresponding dictionaries from **Project**, **Member_pending_request** and **Advisor_pending_request** tables.
- find and send requests to potential members
  - filtering out the unrelated person type from **Persons** table
  - print the filtered list, then asks for the ID of member who the leader wanted to recruit
  - Append the IDs to **Member_pending_request**
- find and send requests to potential advisors
  - This is a similar process to the "find and send requests to potential members" part. Except changing `"member` to `"advisor"`

## Member
- See project and requests status by pulling the corresponding dictionaries from **Project**, **Member_pending_request** and **Advisor_pending_request** tables.
- Modify the project information
  - update the **Project** table.

## Faculty
- See requests to be an advisor
  - Pull the info form **Advisor_pending_request** table.
- Respond to those requests
  - If accepted, update the **Project** and **Advisor_pending_request** tables, _<u>denying all other requests</u>_. `login['role']`will also be updated to `'advisor'`.
  - Otherwise, update the **Advisor_pending_request** table.
- See details of all projects by printing projects out from the **Project** table.

### Advisor
In addition to performing Faculty tasks, Advisor can also
- Can Approve the project for the evaluation.
  - Modify the **Project** table.
- After the evaluation process, Gives the final approval to the project.

## Admin
- is an admin
- HAVE FULL ACCESS TO THE DATABASE. An admin can:
  - View, Edit and delete all tables in the database and its dictionaries.
  - delete the database if he somehow wishes to
- Is the person who will invite evaluators.


More info about the evaluating steps is provided in [proposal.md](proposal.md)

# How will I implement those using OOP
Initially, I planned to implement each role as its own class. But as I write more, I noticed that every roles share something in common. And that is the ability to view and/or manipulate both of the **Requests** tables (Member_pending_request and Advisor_pending_request). As well as the Project table. So to prevent repetitive identical codes, I'd write those as classes with its own methods instead. They would be called upon by the `Main` class, which I will further elaborate below.

## class Request:
It has one attribute: the request table. 
This class is for
- Sending requests to both member and advisors.
- Returning to a person all the requests placing upon him/her to become member/advisor using that person's id
- Receive the decision of `to_be_member` and `to_be_advisor` on whether or not will they join the project. then EDIT THE REQUEST TABLE.
- Returning status of requests. (accepted,rejected)
Since both **Member_pending_request** and **Project** tables are very similar, I think that one class is enough to handle both of them.

## class Project
It has one attribute: the Project table. 
This class is for
- Creating a new project
- update the project's attributes
- find and return a project dictionary using a key and a matching value

## class Login?
Manipulate the login table. Basically, its purpose is just for changing the role of a person. Which has only 2 use cases, when student/faculty become member/advisor. And when a student becomes a project manager. So I'm hesitating on whether to implement this as a class. Or find a way to do it by having methods in other classes taking in `login table` instead

## class Admin
having all admin-related tools. Maybe will merged with the login class above somehow.

## class "Main"
This will most likely be a class that prints out instructions regarding how to use the program for various user roles. As Food for Mankind exam will be held tomorrow, I need to go read it now and will update later.