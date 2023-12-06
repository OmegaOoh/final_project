# Proposal

## Evaluation Step
1. To Evaluate the project or Proposal
2. After Submission of Student
3. Advisor Can see the submission but can't approve it yet
4. Advisor need to assign another 2 Faculties and another 5 Students to review the project and 
5. All the Reviewer that assign to review the project and Project's Advisor need to approve the project,
In order to completely approve projects
6. All Reviewer review the project and response with score maximum of 10
7. Add in Presentation Appointment for Advisor
8. Presentation have maximum score of 10
9. Summarize the result

### To summarize the result
Faculty score weight 90% (30% Each)

Student score weight 10% (2% Each)

score >= 50 to pass

------------------------------------------------------------------------------------------------------------------------

#### Modify Pending_Project_Approval key to
  - Project ID
  - Type
  - Review_Result(Dict include reviewer and advisor name as key and review)
  - Response ('Approved' if all review be approved, otherwise 'Denied')
  - Date of Response

#### New csv file Presentation_appointment with key
  - Project ID
  - Date
  - Result
  - Date of Result

#### New csv file and Table Pending_Reviewer_Request with key
  - Project ID
  - Reviewer_ID
  - Project_Advisor
  - Response
  - Date_of_response

### New csv file  Score_sheet
  - Project ID
  - Reviewer 1 
  - Reviewer 2 
  - Advisor 
  - Student 1-5 
  - Score initialize at 0

------------------------------------------------------------------------------------------------------------------------
## Code Outline
this code outline is under evaluate menu of faculties
### Advisor
- Print Project Title and ID
- Menu
  - Show Faculties member information
  - assign 2 faculties to review the project
    - assigned faculties(by their name)
  - Open Document
  - give approve or deny response
  - Make an Appointment for Presentation
    - Take an Input (dd/mm/yyyy)
  - Presentation Results
    - Change Presentation's Result key

### Normal Faculty
- Add menu to see review request
- Accept/Deny review request

### Reviewer (New role)
- Make Project Evaluate Option in menu available for them
- read project report
- return approve or deny response
  - change their own response in dict of Pending_Project_Approval's review_result

#### After all approval/denial response
- Check If reviewers and advisor are all response
- Check If Presentation Take Place
- Check If They Pass Presentation
- If all passes Change result key to Approved ,otherwise change to 'Denied'