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
    Or at least that was the case. I found out this (17/12/23) morning that **csvwriter reads everything as a string. So I can't do nested list anymore**. So here's my new approach:
    ```py
      {evaluator1 : evaluator No. 1's ID}
      {evaluator2 : evaluator No.2's ID}
      {evaluator3 : evaluator No.3's ID}
      {evaluator1_score : evaluator No.1's score}
      {evaluator2_score : evaluator No.2's score}
      {evaluator3_score : evaluator No.3's score}
      ```
    All of them defaulted to empty string because csvwriter also refused to recognize "NoneType" objects.

- The admin will select 3 evaluators. AND they can't refuse that offer.

- Each Evaluators can give score as an integer from 1 to 10.
- After each advisor gave scores, change the project status in both **Project_to_eval** and **Project** tables.
  ```py
  {project['status'] : 'Evaluated. waiting for final approval.'}
  ```

- The advisor decides whether to give the final approval.
  - If yes, Change project status in both tables once again.
    ```py
    {project['status'] : 'finished'}
    ```
  - If no, revert the project status to what it was before. And delete the project form the Project_to_eval table.
