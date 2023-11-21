# Todo List

### Messages
Table in the database serves as message log.
- implement messages log which include sender ID, receiver ID, message, document(optional),message type
- The document key is optional that use to send the Senior Project Report.

Implement Sent Message Function:
  - Function Input(Message Type, Condition(optional))
  - Take message input until the all condition is met.
  - Insert Message into Messages Table.
### Project
- represent as Table
- including Project Name, Lead Student, Members, Advisor, Status
- Status of Project includes:
  - 'New' means their proposal didn't get approved by advisor yet.
  - 'Incomplete' means approved but incomplete Project
  - 'Completed' mean Advisor approves the project already

## Role
### Admin
- Read and Moderate all Data

### Student
- Add Menu and Function for Student with no assigned project
  - Create Project
  - Show Invites (Message with 'Request' type) + Accept/Deny
  - Read Incoming Messages
- Add Menu and Function for Lead Student
  - Show Project Detail
    - Print out Project Name, Lead Student, Member, Status
  - Modify Project Detail
    - Modify Project Name
  - Find Member
    - show the list of Name and ID of all student 
  - Request Advisors
    - insert new message element into messages table with type 'Request'
  - Send Invitation to Other Student
    - insert new message element into messages table with type 'Request' 
    - unavailable after have 2 member in the group
  - Add Members to Project
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
  - See Request to be a supervisor (Message with 'Request' type)
  - Send Deny response to be advisor
    - insert new message element into messages table with type 'Response'
    - change request message type to ('Closed')
  - See detail of all the project
  - Evaluate Project

### Advising Faculty
- Add Menu and Function for Advising faculty
  - See Request to be a supervisor
  - Sent Accept response to be advisor
  - Send Deny response to be advisor
  - See detail of all the project
  - Evaluate Projects
