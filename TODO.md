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
- lead
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

## What each type of person can do
Initially, there're three types of people based on the csv files provided by T.Paruj; Admin, Faculty and Student. But the program will be able to assign new roles to these people. The person types outlined in the following section will be written as its own class in the [persons.py](persons.py) file.

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