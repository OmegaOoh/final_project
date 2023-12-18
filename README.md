# Final project for 2023's 219114/115 Programming 1

---
# List of File
## Python
### 1. database.py
   - Read csv (as function)
   - Database Class
     - Collection of table
     - Table can be select out for further operation
     - Used to Store Table that needed to use in the application
   - Table Class
     - List of Dictionary
     - Used to Store the data of each type of file
     - Can be used to write its data to csv file.
   
### 2. operation.py
   - Session Class
     - all operation method
     - all validation method
     
### 3. project_manage.py
   - Read csv file and transform it into table object
   - Generate necessary table
   - Login Operation
   - Create Session Object
   - Display and functional of the main menu
     - assign the function list according to the role
---
## Comma Seperated Value(CSV)
### 1. login.csv
   - Store ID Username Password and Person's Role
### 2. persons.csv
   - Store ID FirstName LastName and Type of the Person

### More CSV file will be created after the first execute of the program include
### 1. Project.csv
   - Store ProjectID Project Title Lead Members Advisor and Status
### 2. Advisor_pending_request,  Member_pending_request, Pending_Reviewer_Request
   - Store ProjectID ReceiverID Response and Response Date
   - Those 3 file have same attribute but serve different purpose
### 3. Pending_project_approval
   - Store ProjectID Document(as Text, Represent FileName) Advisor Response and Response Date
### 4. Project_Evaluate_Committee
   - Store ProjectID, Committee member ID and Status
### 5. Project_Score_Result
   - Store Project Score by Each Committee
---
# List of Feature of Role with its Action and Method name
| Role                     |                                   Action                                    |        Method         |  Class  | Completion Percentage (%) |
|:-------------------------|:---------------------------------------------------------------------------:|:---------------------:|:-------:|:-------------------------:|
| All Role                 |       Read Table Data in the Organized Way (Look like Markdown Table)       |     read_as_table     | Session |            100            |
| All Role                 |                   Show table of Person(by key and Value)                    | read_filtered_person  | Session |            100            |
| All Role (Except Admin)  | Read and Response to Request (Need to Modify if New Table has been  append) | response_request_menu | Session |            100            |
| Admin                    |                      Read all of the data in database                       |      read_all_db      | Session |            90             |
| Admin                    |                  Modify Data in the table inside database                   |        modify         | Session |            100            |
| Admin                    |                          Remove Data From Database                          |      remove_data      | Session |            100            |
| Student                  |         Create New Project (Take Project Title, Generate ProjectID)         |    create_project     | Session |            100            |
| Member/ Lead             |                 Show Detail of the Project They working on                  |   show_user_project   | Session |            100            |
| Lead                     |         Modify Project Detail (Change Project Title/ Remove Member)         | modify_Project Detail | Session |            100            |
| Lead                     |                 Send Project Invitation to another Student                  |     send_invites      | Session |            100            |
| Lead                     |                 Send Advising Request to Potential Advisor                  |    request_advisor    | Session |            100            |
| Lead                     |                     Submit The Document for Evaluation                      |        submit         | Session |            100            |
| Faculty/ Advisor         |                         Read All of Projects Detail                         |     read_as_table     | Session |            100            |
| Faculty/ Advisor         |                        Response to Advising Request                         | response_request_menu | Session |            100            |
| Faculty/ Advisor         |                         Response to Review Request                          | response_request_menu | Session |            100            |
| Advisor                  |   Evaluate Project(Process will be different depends on project's status    |   advisor_evaluate    | Session |            100            |
| Advisor(review)          |                              Request Reviewer                               |   request_reviewer    | Session |            100            |
| Reviewer(extension role) |                       Add Paper Score(Maximum of 10)                        |    add_paper_score    | Session |            100            |
| Reviewer(extension role) |                    Add Presentation Score(Maximum of 5)                     |   add_present_score   | Session |            100            |

Note: Class Private Methods Does not List Here

Note: read_filtered_person, response_request_menu, read_as_table can be used in multiple occasion for example:
read_as_table can be use for Find Member, Find Advisor, Find Reviewer which depends on input parameter.

Note: response_request_menu need to modify as if new role or new table has been introduced (needed to have same key)

---
## Missing Feature and Bugs
##### No Major Bugs was found, All feature have been implemented 
