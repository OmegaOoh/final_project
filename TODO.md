# Todo List
## Project
- Status of Project includes:
  - 'New' means their proposal didn't get approved by advisor yet.
  - 'Ongoing' means approved but incomplete Project
  - 'Completed' mean Advisor approves the project already

#### New csv file and Table Pending_Project_Approval with key
  - Project ID
  - Type ('Proposal', 'Report')
  - Response
  - Date of Response
------------------------------------------------------------------------------------------------------------------------
## Role
### Admin
#### what admin can do:
- Read and Modify All Data in Database
- Remove Request from Database

### Student
#### what Student can do:
- Add Menu and Function for Student with no assigned project
  - Create Project
  - Show Invites (From Member_pending_request table with their Name on it) + Accept/Deny
- Add Menu and Function for Lead Student
  - Show Project Detail
    - Print all Project Detail
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
    - Unavailable if No Request

#### Class Methods
- Show_advisor_request()
  -Print out Request from lead student
- Accept_Deny_invitation(input: Response, invites)
  - Change Invites Response
  - Change Response Date
- Show_Project
  - Print All Project Detail
- Evaluate
  -Start Evaluation Process

### Advising Faculty
- Add Menu and Function for Advising faculty
  - See Request to be a supervisor
  - Send Accept/Deny response to be advisor
    - insert new message element into messages table with type 'Response'
    - change its response key to 'Accepted' or 'Denied'
  - See detail of all the project
  - Evaluate
    - Unavailable if No Request

------------------------------------------------------------------------------------------------------------------------
### Add Operation Class
construct with UserID, Role, Database.
- Remove Element(UserID,Table Name, Index of Element)
- Create_Project(Project Title, UserID(Creator))
  - Checking Title Availability
  - Generate Project ID
  - Add Project To Project Table
- Modify_Project_Detail
  - Change Project Title
  - Remove Member from the Project
- Send_Invites(Search Mode, ID/Name)
  - choose search mode (by ID or Name)
  - Search for Member
  - Add Person from search result to Member_pending_request
- Accept_Deny_request(table, Bool of Response Type)
  - Change Invites Response
  - Change Response Date
- Request_Advisor(Search Mode, ID/Name)
  - choose search mode (by ID or Name)
  - Search for Advisor ID
  - Add Person from search result to Advisor_pending_request
- submit(UserID, ProjectID ,Document)
  - Search Project ID for current status
  - If Current Project Status be 'New'
    - Add new element to Pending_project_approval
      - with type 'Proposal'
  - If Current Project Status be 'Incomplete'
    - Add new element to Pending_project_approval
    - with type 'Proposal'
------------------------------------------------------------------------------------------------------------------------
### Add Function in project_manage.py
- print_all(UserID)
  - Print Everything in database
  - Organized way of printing
- print_as_choice(UserID, List)
  - print every thing in list with choice number
  - return maximum range of number for further operation
  - ###### example use case: print for admin to remove element, response to anything.
- print_spec_for_ops(UserID, Table, Key)
  - print information for specific user from id
  - return length of list for further operation if needed
  - ###### example use case: Search for Invitation
------------------------------------------------------------------------------------------------------------------------

Add Validation Methods everywhere the program take input from user.
