# Proposal

## Evaluation Step
1. To Evaluate the project or Proposal
2. After Submission of Student
3. Advisor Can see the submission but can't approve it yet
4. Advisor need to assign another 2 Faculties to review the project
5. All the faculties that assign to review the project and Project's Advisor need to approve the project,
In order to completely approve projects
6. All Reviewer and Advisor review the project and response with Approve or Deny
7. Summarize the result

---
#### New csv file and Table Pending_Project_Approval with key
  - Project ID
  - Review_Result(Dict include reviewer and advisor name as key and review)
  - Response ('Approved' if all review be approved, otherwise 'Denied')
  - Date of Response

#### New csv file and Table Pending_Reviewer_Request with key
  - Project ID
  - Reviewer_ID
  - Project_Advisor
  - Response
  - Date_of_response
---
## Code Outline
this is the code is under evaluate menu of faculties
### Advisor
- Show Project Name
- Show Faculties member information
- assign 2 faculties to review the project
  - assigned faculties(by their name)
- option to read messages and attached document again
- give approve or deny response

### Normal Faculty
- Add menu to see review request
- Accept/Deny review request

### Reviewer
- read project report
- return approve or deny response
  - change their own response in dict of Pending_Project_Approval's review_result

After all approval/denial response
- Check If reviewers and advisor are all response
- If they're all response change response key of its table to 'Approve' or 'Deny' and change
response_date to current date