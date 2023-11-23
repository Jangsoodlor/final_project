# Proposal for the evaluating step
__<u>All faculty members, regardless of being the advisor or not, must gather together and evaluate the project after the advisor approved</u>__

**Steps**
- The advisor approved the project
```py
project['status'] = 'waiting for evaluation'
```
- insert the project to a new table in the database called **Project_to_eval**

- send the "evaluation requests" to all the faculties member

- If all faculties members agreed, the project's status will be updated to `'finished'`

- If at least one of the faculty member denied
  - change project status back to whatever it was before `'waiting for evaluation'`

Regardless of the evaluation outcome, if all the faculties member responded, delete the project's dictionary form the **Project_to_eval** table.