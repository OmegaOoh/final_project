# Todo List

## Project
- Status of Project includes:
  - 'New' means their proposal didn't get approved by advisor yet.
  - 'Incomplete' means approved but incomplete Project
  - 'Completed' mean Advisor approves the project already
---
## Role
### Admin
- Read All Data in Database
- Remove Request from Database

### Student
- Add Menu and Function for Student with no assigned project
  - Create Project
  - Show Invites (From Member_pending_request table with their Name on it) + Accept/Deny
- Add Menu and Function for Lead Student
  - Show Project Detail
    - Print all Project Detail
  - Modify Project Detail
    - Modify Project Detail
  - Find Member
    - show the list of Name and ID of all student 
  - Request Advisors
    - Add new Request to Advisor_pending_request table
  - Send Project Invitation to Other Student
    - Add new Request to Member_pending_request table
    - unavailable after have 2 member in the group
  - Submit
    - Will be changed according to status of the project
      - Submit Proposal If Project Status be ('New')
      - Submit Report If Project Status be ('Incomplete')
      - None If Project is completed
- Add Menu and Function for Member Student
  - Show Project Detail
  - Modify Project Detail

### Normal Faculty
- Add Menu and Function for faculty
  - See Request to be a supervisor (From Advisor_pending_request table with their Name on it)
  - Send Accept/Deny response to be advisor
    - insert new message element into messages table with type 'Response'
    - change its response key to 'Accepted' or 'Denied'
  - See detail of all the project
  - Evaluate Project

### Advising Faculty
- Add Menu and Function for Advising faculty
  - See Request to be a supervisor
  - Send Accept/Deny response to be advisor
    - insert new message element into messages table with type 'Response'
    - change its response key to 'Accepted' or 'Denied'
  - See detail of all the project
  - Evaluate Projects
---

Adding Validation Methods everywhere the program take input from user.
