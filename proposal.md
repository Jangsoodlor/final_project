# Proposal for the evaluating step
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
    - Evaluators (Default = `[]`). This will be a nested list. of the evaluator's id and the score he or she give. Something like
      ```py
      {evaluators : [['0001', 10], ['0002', 9], ['0003', 20]]}
      ```
    - Initially, the evaluator's id and their score (aka. first and second index of each list) will be set to a NoneType.
      ```py
      {Evaluators : [['0001', None], ['0002', None], ['0003', None]]}
      ```

- The admin will select 3 evaluators. AND they can't refuse that offer

- Each Evaluators can give score as an integer from 1 to 10. This will be written as a method in 
- After each advisor gave scores, change the project status in both **Project_to_eval** and **Project** tables.
  ```py
  {project['status'] : 'Evaluated. waiting for final approval.'}
  ```

- The advisor decides whether to give the final approval.
  - If yes, Change project status in both tables once again.
    ```py
    {project['status'] : 'Finished'}
    ```
  - If no, revert the project status to what it was before.
