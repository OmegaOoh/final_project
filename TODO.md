# Todo List

Modify Table Class to Have Calling which initiate as Table name(could be changed by admin)


Modify Database Class to have search by Calling Name Methods

## Project
- Status of Project includes:
  - 'New' means their proposal didn't get approved by advisor yet.
  - 'Incomplete' means approved but incomplete Project
  - 'Completed' mean Advisor approves the project already

#### New csv file and Table Pending_Project_Approval with key
  - Project ID
  - Type ('Proposal', 'Report')
  - Response
  - Date of Response
------------------------------------------------------------------------------------------------------------------------
create new object when login according to role

All class of the object take userID, roles and Database as attributes.

All class have menu methods to use as menu of the class functionality

In Class Methods: Input mean Take input from user inside methods of the class, Parameter mean Take as a function input.
## Role
### Admin
#### what admin can do:
- Read and Modify All Data in Database
- Remove Request from Database

#### Class Methods
- Read_Database
  - Show All Table in Database (its file name and its calling name)
- Modify_Calling_name(Input: File name, Calling name)
- Search_Database (Input Table's Calling Name)
  - Show All Element inside Table
- Remove_Table_Element(Input: Table, Key to search, Search Query)
  - Remove Element By Table's Search Methods


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

#### Class Methods
- Create_Project(Input: Project Title)
  - Checking Title Availability
  - Generate Project ID
  - Add Project To Project Table
- Show Invites
  - Search Through Member_Pending_Request Table for Their Name
  - Use Accept/Deny Methods
- Show_Project_Detail
  - from User ID print out All Project Detail
- Modify_Project_Detail
  - Change Project Title
  - Remove Member from the Project
- Show_Student
  - Print Person role with "Student" Name and user ID
- Send_Invites(input: Search Mode, ID/Name)
  - choose search mode (by ID or Name)
  - Search for Member
  - Add Person from search result to Member_pending_request
- Accept_Deny_request(input: Response, request)
  - Change Invites Response
  - Change Response Date
- Show_Faculty
  - Print Person role with "Faculty", "Advisor"
- Request_Advisor
  - choose search mode (by ID or Name)
  - Search for Advisor
  - Add Person from search result to Advisor_pending_request
- submit(Input: Document)
  - Search Project ID for current status
  - If Current Project Status be 'New'
    - Add new element to Pending_project_approval
      - with type 'Proposal'
  - If Current Project Status be 'Incomplete'
    - Add new element to Pending_project_approval
    - with type 'Proposal'


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
#### Class Methods
- Show_advisor_request()
  -Print out Request from lead student
- Accept_Deny_invitation(input: Response, invites)
  - Change Invites Response
  - Change Response Date
- Show_Project
  - Option to print only supervising project or all project
- Evaluate
  - If More than 1 Submission Print A menu to select it
  - If it is proposal advisor could read and approve themselves
---

 Adding Validation Methods everywhere the program take input from user.
