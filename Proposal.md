# Proposal 

- Add 1 key named 'Reviewer' into Table of Projects

## Evaluation Step
1. To Evaluate the project or Proposal
2. - After Submission of Student
3. - Advisor Can see the submission but can't approve it yet
4. - Advisor need to assign another 2 Faculties to review the project
5. - All the faculties that assign to review the project and Project's Advisor need to approve the project,
In order to completely approve projects
6.  The Denial of the project need to have reply messages along with it
7.  Submission will be treated as message Type of 'Submission'
8.  and Changed to Closed when gets approve or deny

## Code Outline
this is the code is under evaluate menu of faculties
### Advisor
- Show Project Name
- Show Faculties member information
- assign 2 faculties to review the project
  - assigned faculties(their ID) get added into reviewer key of the project
- option to read messages and attached document again
- give approve or deny response

### Assigned Faculties
- read project report
- return approve or deny response
  - denial need to be with message (Type 'Denial')
    - loop till the message not being empty string.
  - approval - message is optional (Type 'Approval')
  - insert response message to Advisor.

After Evaluation of both Advisor and/or Faculties
- Check if All evaluation process is done (all faculties are response)
  -  if Yes
    - sent summary of the evaluation to student and Advisor along with message
      - include results, project name, advisor name, reviewer name