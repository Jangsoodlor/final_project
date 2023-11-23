# To-Do Lists
lists of things to be implement 😭😭😭
## Databases
There shall be 5 tables with the following attributes

**Persons**
- ID
- First
- Last
- Type

**Login**
- ID
- Username
- Password
- Role

**Project**
- ProjectID
- Title
- Lead
- Member1
- Member2
- Advisor
- Status

**Member_pending_request**
- ProjectID
- to_be_member
- Response
- Response_date

**Advisor_pending_request**
- ProjectID
- to_be_advisor
- Response
- Response_date

## What each type of person can do
Initially, there're three types of people based on the csv files provided by T.Paruj; Admin, Faculty and Student. But the program will be able to assign new roles to these people. Each type of person will be written as its own class in the [persons.py](persons.py) file.

### Student
- See project member requests
- Accept and deny those requests.
  - If accepted, the **Project** and **Member_pending_request** tables shall be updated, _denying all other requests_. `persons['type']`and `login['role']`will also be updated to `'member'`
  - Otherwise, the **Member_pending_request** will be updated.
- Create a project and becomes a lead
  - update `persons['type']`and `login['role']` to leader
  - create project by appending a project dictionary with some attributes filled into the **Project** table.

  ```py
  projectID = len(project_table.table)
  ```
  - more features will be explained in the Leader section.

### Leader
- See project and requests status by pulling the corresponding dictionaries from **Project**, **Member_pending_request** and **Advisor_pending_request** tables.
- find and send requests to potential members
  - filtering out the unrelated person type from **Persons** table
  - print the filtered list, then asks for the ID of member/advisor who the leader wanted to recruit
  - Append the IDs to **Member/Advisor_pending_request**

### Member
- See project and requests status by pulling the corresponding dictionaries from **Project**, **Member_pending_request** and **Advisor_pending_request** tables.
- Modify the project information
  - update the **Project** table.

### Faculty
- See requests to be an advisor
  - Pull the info form **Advisor_pending_request** table.
- Respond to those requests
  - If accepted, update the **Project** and **Advisor_pending_request** tables, _denying all other requests_. `persons['type']`and `login['role']`will also be updated to `'advisor'`.
  - Otherwise, update the **Advisor_pending_request** table.
- See details of all projects by printing projects out from the **Project** table.

### Advisor
- Can Approve the project for the evaluation.
  - Modify the **Project** table.

### __<u>All faculty members, regardless of being the advisor or not, must gather together and evaluate the project after the advisor approved</u>__.
More info will be provided in [proposal.md](proposal.md)

### Admin
- is an admin
- HAVE FULL ACCESS TO THE DATABASE.