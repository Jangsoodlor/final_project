# Proposal for the evaluating step
__<u>All faculty members, regardless of being the advisor or not, must gather together and evaluate the project after the advisor approved</u>__

**Steps**
- The advisor approved the project for the evaluation
- Change project status in project table
  ```py
  {project['status'] : 'waiting for evaluation'}
  ```
- copy the project dictionary to a new table in the database called **Project_to_eval** (or something like that)
**Project_to_eval (TBC)**
 - These attributes are inherited from **Project** table.
    - ProjectID
    - Title
    - Lead
    - Member1
    - Member2
    - Advisor
    - Status
  - These attributes are new:
    - Evaluators (Default = `[]`). This will be a nested list. of the evaluator's name and the score he or she give. Something like
      ```py
      {Evaluators : [['0001', 10], ['0002', 9], ['0003', 20]]}
      ```


- The admin send the "evaluation requests" to all the faculty members by appending the project to **Advisor_pending_request** table.

- If <u>3 faculty members agreed</u>
  - the other requests will be deleted from **Advisor_pending_request** table automatically.
    ```py
    {project['status'] : 'evaluating'}
    ```
    ```py
    {Evaluators : [['0001', None], ['0002', None], ['0003', None]]}
    ```
- Each Evaluators can give score. This will be written as a method in 
- After each advisor gave scores, change the project status in both **Project_to_eval** and **Project** tables.
  ```py
  {project['status'] : 'Evaluated. waiting for final approval.'}
  ```

- After the Advisor gave the final approval
  - Change project status in both tables once again.
    ```py
    {project['status'] : 'Finished'}
    ```
