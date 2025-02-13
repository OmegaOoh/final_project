import time
import database
from database import Table


# Handle Common Methods
class Session:
    __valid_role = ['student', 'member', 'lead',
                    'student/reviewer', 'member/reviewer', 'lead/reviewer',
                    'faculty', 'advisor', 'admin',
                    'faculty/reviewer', 'advisor/reviewer']
    __faculty_role = ['faculty', 'advisor',
                      'faculty/reviewer', 'advisor/reviewer']

    __student_role = ['student', 'member', 'lead',
                      'student/reviewer', 'member/reviewer', 'lead/reviewer']

    @staticmethod
    def time_format():
        '''
        This function Format date from time module into readable form
        :return: string of formatted date
        '''
        curr_time = time.localtime()
        formatted_time = (str(curr_time.tm_mon)
                          + '/' + str(curr_time.tm_mday)
                          + '/' + str(curr_time.tm_year))
        return formatted_time
    
    @staticmethod
    def __is_int(x):
        '''
        This function check if x is an integer
        :param x: data to be checked for
        :return: result of check if x is an integer
        '''
        try:
            int(x)
            return True
        except ValueError:
            return False

    @staticmethod
    def __check_review_status(result):
        '''
        This function Check if score is acquired
        :param result: score to check
        :return: True if score is acquired.Otherwise, False
        '''
        ls = result.split(' + ')
        return 'r' not in ls and 'p' not in ls
            
    def __init__(self, uid, db: database.Database):
        self.db = db
        self.__uid = uid
        self.role = self.__check_role(uid)

    def __check_role(self, uid):
        '''
        This function check role of person in login table
        :param uid: uid of person to check
        :return: person's role
        '''
        login_table = self.db.search('login')
        if not login_table:
            raise LookupError("Table Not Found; Can't Validate Roles.")
        login_data = login_table.search("ID", uid)
        if not login_data:
            print('UID: ', uid)
            raise LookupError('No User ID Found')
        return login_data['role']

    def __update_role(self, uid, new_role):
        '''
        This function Update role of person in login table and in Session
        :param uid: uid of person to update
        :param new_role: role to change to
        :return: None
        '''
        if new_role in self.__valid_role:
            table = self.db.search('login')
            if table:
                user_dict = table.search('ID', uid)
                if not user_dict:
                    raise LookupError("User ID not found")
                user_dict['role'] = new_role
                self.role = new_role

    def __update_project(self):
        '''
        This function Update Project in all Related Table
        :return: None
        '''
        pr_table = self.db.search('Project')
        if not pr_table:
            raise LookupError("Project Table not Found")
        adv_req = self.db.search('Advisor_pending_request')
        if not adv_req:
            raise LookupError("Advisor Request Table not Found")
        mem_req = self.db.search('Member_pending_request')
        if not mem_req:
            raise LookupError("Member Invites Table not Found")
        rev_req = self.db.search('Pending_Reviewer_Request')
        if not rev_req:
            raise LookupError("Reviewer Invites Table not found")
        committee_tab = self.db.search("Project_Evaluate_Committee")
        if not committee_tab:
            raise LookupError("Committee Table Not Found")
        committee_tab = committee_tab.filter(lambda x: x['Status'] != 'Completed')
        score_tab = self.db.search("Project_Score_Result")
        if not score_tab:
            raise LookupError("Score Sheet Not Found")

        # Update Project Advisor
        adv_acc_req = adv_req.filter(lambda x: x['Response'] == 'Accepted')
        if adv_acc_req and not all(i == '' for i in adv_acc_req.data[0]):
            for i in adv_acc_req.data:
                pr_id = i['ProjectID']
                project = pr_table.search('ProjectID', pr_id)
                # Skip if Duplicates
                uid = i['ReceiverID']
                if all(project[j] != uid for j in project):
                    continue
                # Check if Any slot is empty and assign newly accept in
                if project and project['Advisor'] == '':
                    pr_table.search('ProjectID', pr_id)['Advisor'] = i['ReceiverID']
                adv_pending_req = adv_req.filter(lambda x: x['ProjectID'] == pr_id)
                # if all slot is occupied then change status to Expired
                if adv_pending_req and not all(i == '' for i in adv_pending_req.data[0]):
                    for j in adv_pending_req.data:
                        if j['Response'] == 'Pending':
                            j['Response'] = 'Expired'
                            j['Response_date'] = self.time_format()

        # Update Project Member
        mem_acc_req = mem_req.filter(lambda x: x['Response'] == 'Accepted')
        if mem_acc_req and not all(i == '' for i in mem_acc_req.data[0]):
            for i in mem_acc_req.data:
                pr_id = i['ProjectID']
                project = pr_table.search('ProjectID', pr_id)
                # Skip if duplicates
                uid = i['ReceiverID']
                if uid in list(project.values()):
                    continue
                if project:
                    # Check if Any slot is empty and assign newly accept in
                    if project['Member1'] == '':
                        pr_table.search('ProjectID', pr_id)['Member1'] = i['ReceiverID']
                    elif project['Member2'] == '':
                        pr_table.search('ProjectID', pr_id)['Member2'] = i['ReceiverID']
                    mem_pending_req = mem_req.filter(lambda x: x['ProjectID'] == pr_id
                                                     and x['Response'] == 'Pending')
                    # if all slot is occupied then change status to Expired
                    if mem_pending_req and not all(i == '' for i in mem_pending_req.data[0]):
                        if project['Member1'] != '' and project['Member2'] != '':
                            for j in mem_pending_req.data:
                                if j['Response'] == 'Pending':
                                    j['Response'] = 'Expired'
                                    j['Response_date'] = self.time_format()

        # Update Project Reviewer
        rev_acc_req = rev_req.filter(lambda x: x['Response'] == 'Accepted')
        if rev_acc_req and not all(i == '' for i in rev_acc_req.data[0]):
            for i in rev_acc_req.data:
                if i['ReceiverID'] == '':
                    break
                pr_id = i['ProjectID']
                uid = i['ReceiverID']
                committee_dc = committee_tab.search('ProjectID', pr_id)
                # Assign To Committee Table
                if committee_dc:
                    # Check if Assigned,if it duplicates skip
                    if uid in (committee_dc.values()):
                        continue
                    # Check if Any slot is empty and assign newly accept in
                    if self.__check_role(uid) in self.__faculty_role:
                        if committee_dc['Reviewer1'] == '':
                            committee_tab.search('ProjectID', pr_id)['Reviewer1'] = i['ReceiverID']
                        elif committee_dc['Reviewer2'] == '':
                            committee_tab.search('ProjectID', pr_id)['Reviewer2'] = i['ReceiverID']

                        fac_pending = (rev_req.filter(lambda x: x['ProjectID'] == pr_id
                                                      and x['Response'] == 'Pending'
                                                      and self.__check_role(x['ReceiverID'])
                                                      in self.__faculty_role))
                        if fac_pending and not all(i == '' for i in fac_pending.data[0]):
                            if committee_dc['Reviewer1'] != '' and committee_dc['Reviewer2'] != '':
                                for j in fac_pending.data:
                                    if j['Response'] == 'Pending':
                                        j['Response'] = 'Expired'
                                        j['Response_date'] = self.time_format()
                    # Check if Any slot is empty and assign newly accept in
                    elif self.__check_role(i['ReceiverID']) in self.__student_role:
                        if committee_dc['Student1'] == '':
                            committee_tab.search('ProjectID', pr_id)['Student1'] = i['ReceiverID']
                        elif committee_dc['Student2'] == '':
                            committee_tab.search('ProjectID', pr_id)['Student2'] = i['ReceiverID']
                        elif committee_dc['Student3'] == '':
                            committee_tab.search('ProjectID', pr_id)['Student3'] = i['ReceiverID']
                        elif committee_dc['Student4'] == '':
                            committee_tab.search('ProjectID', pr_id)['Student4'] = i['ReceiverID']
                        elif committee_dc['Student5'] == '':
                            committee_tab.search('ProjectID', pr_id)['Student5'] = i['ReceiverID']

                        std_pending = (rev_req.filter(lambda x: x['ProjectID'] == pr_id
                                                     and x['Response'] == 'Pending'
                                                     and self.__check_role(x['ReceiverID'])
                                                     in self.__student_role))
                        check_ls = ['Student1', 'Student2', 'Student3', 'Student4', 'Student5']
                        # if all slot is occupied then change status to Expired
                        if std_pending and not all(i == '' for i in std_pending.data[0]):
                            if all(committee_dc[k] == '' for k in check_ls):
                                for j in std_pending.data:
                                    if j['Response'] == 'Pending':
                                        j['Response'] = 'Expired'
                                        j['Response_date'] = self.time_format()

    def __check_score(self):
        '''
        This method is used to Summarize score and update its status accordingly
        Each Faculty Reviewer will give 30% of Score (3 Person)
        Each Student will give only 2% of Score (5 Person)
        The Project Need 50% To be Pass
        :return: None
        '''
        score_tab = self.db.search('Project_Score_Result')
        if not score_tab:
            raise LookupError('Table Not Found')
        cmm_tab = self.db.search('Project_Evaluate_Committee')
        if not cmm_tab:
            raise LookupError('Table Not Found')
        for i in score_tab.data:
            check_ls = ['Advisor', 'Reviewer1', 'Reviewer2',
                        'Student1', 'Student2', 'Student3', 'Student4', 'Student5']
            if all(self.__check_review_status(i[j]) for j in check_ls):
                i['Status'] = 'Completed'
                # Remove Reviewer from Role
                proj_cmm = cmm_tab.search('ProjectID', i['ProjectID'])
                proj_cmm['Status'] = 'Completed'
                for j in check_ls:
                    self.__update_role(proj_cmm[j],
                                       self.__check_role(proj_cmm[j]).removesuffix('/reviewer'))

                # Summarize Score
                sum_score = 0
                # Faculty
                for j in check_ls[0:3]:
                    ls = i[j].split(' + ')
                    for k in ls:
                        sum_score += int(k) * 2

                # Student
                for j in check_ls[0:3]:
                    ls = i[j].split(' + ')
                    for k in ls:
                        sd_score = int(k) / 8
                        if sd_score > 2:
                            sum_score = 2
                        sum_score += sd_score

                if sum_score > 100:
                    sum_score = 100

                project_app = self.db.search("Pending_project_approval")
                if not project_app:
                    raise LookupError("Table Not Found")
                project_app = project_app.filter(lambda x: x['Response'] == 'Pending')
                j = project_app.search('ProjectID', i['ProjectID'])
                if sum_score >= 50:
                    j['Response'] = 'Approved'
                    project = self.db.search('Project')
                    if project:
                        p = project.search("ProjectID", i['ProjectID'])
                        p['Status'] = 'Completed'
                        self.__complete_project(p['ProjectID'])
                else:
                    j['Response'] = 'Denied'
                j['Response_date'] = self.time_format()

    def __complete_project(self, project_id):
        '''
        Set User in The project back to normal
        For Lead and Member Change back to Student
        For Advisor Change back to Faculty unless They still have project to supervising
        :param project_id: Project ID
        :return: None
        '''
        p_table = self.db.search("Project")
        if not p_table:
            raise LookupError("Table Not Found")
        project = p_table.search("ProjectID", project_id)
        if not project:
            raise LookupError("No Project Found")
        # Set Student role to student
        check_ls = ['Lead', 'Member1', 'Member2']
        for i in check_ls:
            if project[i] and not project[i].isspace():
                self.__update_role(project[i], 'student')

        # Handle Advisor Role(Return to Faculty if no more advising project)
        uid = project['Advisor']
        advise_tab = p_table.filter(lambda x: x['Advisor'] == uid)
        if all(i == '' for i in advise_tab.data[0]):
            raise LookupError("Something went wrong")
        if len(advise_tab.data) > 1:
            # Nothing will be done to Advisor Role
            # Advisor still advising another project
            return
        else:
            self.__update_role(uid,'faculty')

###############################################################################################
    # Admin Related Staff
    def read_all_db(self, uid):
        '''
        Read Every thing in the Database
        :param uid: UserID
        :return: None
        '''
        if uid != self.__uid or self.__role != 'admin':
            raise PermissionError()
        for i in range(len(self.db.table_name())):
            print(self.db.search(self.db.table_name()[i]).to_table())
            print()

    def __remove_by_data(self,uid, table_name, key, value):
        '''
        Remove the Data from the Table in Database by Value
        :param uid: UserID
        :param table_name: Table name
        :param key: Key to remove
        :param value: Value to remove
        :return: None
        '''
        if uid != self.__uid or self.__role != 'admin':
            raise PermissionError()
        target_table = self.db.search(table_name)
        if not target_table:
            print('Table Not Found; Nothing was changed')
            return
        ls = target_table.select(key)
        index = ls.index(value)
        self.__remove_element(uid, target_table, index)

    def __remove_by_order(self, uid, table_name, order):
        '''
        Remove the Data from the Table in Database by Order
        :param uid: UserID
        :param table_name: Table Name
        :param order: Order of The Data to be Remove
        :return: None
        '''
        if uid != self.__uid or self.__role != 'admin':
            raise PermissionError()
        target_table = self.db.search(table_name)
        if not target_table:
            print('Table Not Found; Nothing was changed')
            return
        self.__remove_element(uid, target_table, order - 1)

    def __modify_data(self, uid, table_name, key_search, val_search, key_mod, val_mod):
        '''
        Modify the Data in The Table in Database
        :param uid: UserID
        :param table_name: Table Name
        :param key_search: Key To Search for data to modify
        :param val_search: Value to Modify
        :param key_mod: Key to Modify
        :param val_mod: New Value
        :return: None
        '''
        if uid != self.__uid or self.__role != 'admin' or key_mod == 'ID':
            raise PermissionError()
        target_table = self.db.search(table_name)
        if not target_table:
            print('Table Not Found; Nothing was changed')
            return
        dc = target_table.search(key_search, val_search)
        if not dc:
            print('Data Not Found')
            return
        if key_mod in dc.keys():
            dc[key_mod] = val_mod

    def __remove_element(self, uid, table, index):
        '''
        Remove the Element from Table
        :param uid: UserID
        :param table: Target Table
        :param index: Index to be remove
        :return: None
        '''
        if uid != self.__uid or self.__role != 'admin':
            raise PermissionError()
        table.remove_data(index)

    def remove_data(self, uid):
        '''
        This Method let Admin remove The Data from Table
        All Necessary Information to remove take in the method
        :param uid: UserID
        :return: None
        '''
        table_name = input('Target Table: ')
        mode = input('Remove mode (Data or Order) \nChoice: ')
        if mode == 'Data':
            key = input('Key to Remove: ')
            value = input('Value to Remove: ')
            self.__remove_by_data(uid, table_name, key, value)
        elif mode == "Order":
            order = input('Order to Remove: ')
            if self.__is_int(order):
                self.__remove_by_order(uid, table_name, int(order))
            else:
                return print('Invalid input...')

    def modify(self, uid):
        '''
        This Method Take Input for Modify
        No Validation is needed because The Method will be Stop if Something was off.
        :param uid: UserID
        :return: None
        '''
        tab_name = input('Table Name: ')
        key_s = input('Key to Search: ')
        val_s = input('Searching Value: ')
        key_m = input('Key to Modify: ')
        val_m = input('Value to Modify: ')
        self.__modify_data(uid, tab_name, key_s, val_s, key_m, val_m)

    ###############################################################################################
    def read_as_table(self, uid, table):
        '''
        This Method Print Table Data in the Table Form
        :param uid: UserID
        :param table: Table to Print
        :return:
        '''
        if uid != self.__uid:
            raise PermissionError()
        print(table.to_table())

    def read_filtered_person(self, uid, key, val):
        '''
        Read Filtered Person Data by Key and Value
        :param uid: UserID
        :param key: Key to Filter
        :param val: Value to Filter
        :return: None
        '''
        if uid != self.__uid:
            raise PermissionError()
        project = self.db.search('persons')
        if project:
            filtered = project.filter(lambda x: x[key] == val)
            print(filtered.to_table())
        else:
            raise LookupError('Table not found')

    def __search_for_id(self, mode, query, p_type: str):
        '''
        This Method Search For Person ID
        :param mode: Name or ID
        :param query: Searching Query corresponding to Mode
        :param p_type: Person Type
        :return: User ID if it is found, else None
        '''
        p_table = self.db.search('persons')
        p_table = p_table.filter(lambda x: x['type'] == p_type)
        if not p_table:
            raise LookupError("Table not found")
        # Search mode 'Name' / 'ID'
        if mode == 'Name':
            dict_p = p_table.search('first', query)
            if dict_p:
                return dict_p['ID']
            return None
        if mode == 'ID':
            dict_p = p_table.search('ID', query)
            if dict_p:
                return query
        return None

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, r):
        if r in self.__valid_role:
            self.__role = r
        else:
            ValueError('INVALID ROLE')

    def create_project(self, uid):
        '''
        This Method Create Project by
        Taking Project Title and Generate Project ID and
        Assign User to Lead
        :param uid: UserID
        :return: None
        '''
        if self.__uid != uid:
            raise PermissionError("User ID Not Match")
        table = self.db.search('Project')
        if table:
            name_valid = False
            project_title = ''
            while not name_valid:
                project_title = input("Insert Your Project Title: ")
                if not table.search('Title', project_title):
                    name_valid = True
                else:
                    print('Name not Valid Please Try Again')
            if project_title == '' or project_title.isspace():
                print('Invalid Project Title')
                return
            project_id = self.__gen_project_id(project_title)
            if project_id:
                if table.insert({"ProjectID": str(project_id),
                                 'Title': project_title,
                                 'Lead': uid,
                                 'Member1': '',
                                 'Member2': '',
                                 'Advisor': '',
                                 'Status': 'New'}):
                    self.__update_role(uid, 'lead')

    # ProjectID generation is Subject to be change
    @staticmethod
    def __gen_project_id(project_title):
        '''
        Generate project ID
        first 2 digit is Year
        3-7 digit is time in nanosecond
        8th digit is len of project_title mod 10
        9th and 10th digit is usm of all number in the ID before mod 100
        :param project_title:
        :return:
        '''
        uniqueid = str(time.gmtime().tm_year)[-2:]
        uniqueid += str(time.time_ns())[-8:-3]
        uniqueid += str(len(project_title) % 10)
        uniqueid += str(sum([int(i) for i in uniqueid]) % 100)
        return uniqueid

    def modify_project_detail(self, uid):
        '''
        Modify Project Detail
        :param uid:
        :return:
        '''
        if self.__uid != uid:
            raise PermissionError("User ID Not Match")
        table = self.db.search('Project')
        if table:
            project = table.search('Lead', uid)
            self.__project_modify_menu(project)
        else:
            raise LookupError("Table not found")

    def __project_modify_menu(self, project):
        '''
        Printout and Use as Menu to Modify the project detail
        :param project: Project Dict
        :return: None
        '''
        while True:
            print('Project Modification Menu:')
            print('1. Change Project Title')
            if project['Member1'] != '' or project['Member2'] != '':
                print('2. Remove Member')
            c = input('Choice: ')
            if not self.__is_int(c):
                continue
            c = int(c)
            if c == 1:
                print('Current Title', project['Title'])
                project['Title'] = input('New Title: ')
                break
            if c == 2 and project['Member1'] != '' or project['Member2'] != '':
                while True:
                    print('Member to Remove:')
                    member_ls = [project['Member1'], project['Member2']]
                    for i in range(len(member_ls)):
                        print(f'{i}. Member{i}: {member_ls[i]}')
                    c = input('Choice: ')
                    if not self.__is_int(c):
                        if c == 1:
                            if member_ls[0] != '':
                                project['Member1'] = ''
                            else:
                                project['Member2'] = ''
                            break
                        if c == 2 and '' not in member_ls:
                            project['Member2'] = ''
                            break
                break

    def show_user_project(self, uid):
        '''
        Function to Show User Project Details
        :param uid: UserID
        :return: None
        '''
        if uid != self.__uid:
            raise PermissionError()
        project = self.db.search('Project')
        if project:
            filtered = project.filter(lambda x: uid in [x['Lead'], x['Member1'], x['Member2']])
            filtered.table_name = uid
            print(filtered.to_table())
        else:
            raise LookupError('Table not found')

    def send_invites(self, l_uid):
        '''
        Function to Send invites
        :param l_uid: UserID of Lead
        :return: None
        '''
        if l_uid != self.__uid:
            raise PermissionError("User ID Not Match")
        s_m = input('Search by Name or by ID \nSearch Mode: ')
        while s_m not in ['ID', 'Name']:
            print('Invalid Search Mode')
            s_m = input('Search by Name or by ID \nSearch Mode: ')

        s_q = input('Search Query: ')
        uid = self.__search_for_id(s_m, s_q, 'student')
        # Return if it is your self
        if uid == l_uid:
            print("You Can't Invite Your Self")
            return
        if uid:
            i_table = self.db.search('Member_pending_request')
            pr_table = self.db.search('Project')
            if i_table and pr_table:
                # Find Project ID and Project Lead by UID
                project_dict = pr_table.search('Lead', l_uid)
                project_id = project_dict['ProjectID']
                if uid in list(project_dict.values):
                    print("This User already in your project")
                    return
                # Check if Duplicates
                filtered_table = i_table.filter(lambda x: x['ProjectID'] == project_id)
                filtered_table = filtered_table.filter(lambda x: x['ReceiverID'] == uid
                                                       and x['Response'] == 'Pending')
                if not all(i == '' for i in filtered_table.data[0].values()):
                    print('You already sent to this person')
                    return
                i_table.insert({"ProjectID": project_id,
                                "ReceiverID": uid,
                                "Response": 'Pending',
                                "Response_date": ''})
            else:
                raise LookupError("Table not found")
        else:
            print('No Receiver found')

    def request_advisor(self, l_uid):
        '''
        This function Handle Advisor Request
        :param l_uid: Lead UserID
        :return: None
        '''
        if l_uid != self.__uid:
            raise PermissionError("User ID Not Match")
        s_m = input('Search by Name or by ID \nSearch Mode: ')
        while s_m not in ['ID', 'Name']:
            print('Invalid Search Mode')
            s_m = input('Search by Name or by ID \nSearch Mode: ')
        s_q = input('Search Query: ')
        uid = self.__search_for_id(s_m, s_q, 'faculty')
        if uid == l_uid:
            print("You Can't Invite Your Self")
            return
        if uid:
            i_table = self.db.search('Advisor_pending_request')
            pr_table = self.db.search('Project')
            if i_table and pr_table:
                # Find Project ID and Project Lead by UID
                project_dict = pr_table.search('Lead', l_uid)
                project_id = project_dict['ProjectID']
                # Check if Duplicates
                filtered_table = i_table.filter(lambda x: x['ProjectID'] == project_id)
                filtered_table = filtered_table.filter(lambda x: x['ReceiverID'] == uid and x['Response'] == 'Pending')
                if not all(i == '' for i in filtered_table.data[0].values()):
                    print('You already sent to this person')
                    return
                i_table.insert({"ProjectID": project_id,
                                "ReceiverID": uid,
                                "Response": 'Pending',
                                "Response_date": ''})
            else:
                raise LookupError("Table not found")
        else:
            print('No Receiver found')

    def __accept_deny_request(self, request, response: bool, uid, to_be):
        '''
        The Method Take the response and change user role according to their response
        :param request: Request to Response
        :param response: User Response
        :param uid: UserID
        :param to_be: Role to Change TO
        :return: None
        '''
        if request['Response'] != 'Pending' and request['Response_date'] != '':
            print('Request Already Response')
            return
        if response:
            request['Response'] = 'Accepted'
            if to_be != 'reviewer':
                self.__update_role(uid, to_be)
            else:
                self.__update_role(uid, self.role + '/reviewer')
        else:
            request['Response'] = 'Denied'
        request['Response_date'] = self.time_format()
        self.__update_project()

    def response_request_menu(self, uid, table):
        '''
        The Method to display the request menu
        and give user an ability to response it
        :param uid: UserID
        :param table: Request Table to Response
        :return: None
        '''
        if uid != self.__uid:
            raise PermissionError()
        if not isinstance(table, Table):
            raise TypeError()
        pr_table = self.db.search('Project')
        if not pr_table:
            raise LookupError("Project Table not Found")
        # Print all user's request
        req_dict = {}
        to_be = ''
        if table.table_name == "Member_pending_request":
            to_be = 'member'
        if table.table_name == "Advisor_pending_request":
            to_be = 'advisor'
        if table.table_name == 'Pending_Reviewer_Request':
            to_be = 'reviewer'
            if 'reviewer' in self.__check_role(self.__uid):
                print('You Currently Assign to Another Project')
                return

        # Chck if to_be role is correctly assign(Return if not)
        if to_be == '':
            return
        # Read All inbox
        print("Inbox: ")
        request_data = table.filter(lambda x: x['ReceiverID'] == uid)
        request_data = request_data.filter(lambda x: x['Response'] == 'Pending')
        if all(i == '' for i in request_data.data[0].values()):
            print('Empty Inbox')
            print()
            return
        for i in range(len(request_data.data)):
            project_detail = pr_table.search('ProjectID', request_data.data[i]['ProjectID'])
            if project_detail:
                print(f'{i+1}. Project: {project_detail["ProjectID"]} '
                      f'{project_detail["Title"]}')
                req_dict[str(i+1)] = request_data.data[i]
            # Give User a Choice to Return or Response to request
            while True:
                print('Choice')
                print("1. Response \n2. Return")
                c = input('Choice: ')
                if c == '1':
                    while True:
                        inv = input('Select Request: ')
                        if inv in req_dict:
                            print('1 to Accept 2 to Deny')
                            r = input('Your Response: ')
                            _map = {'1': True, '2': False}
                            self.__accept_deny_request(req_dict[inv], _map[r], uid, to_be)
                            return
                if c == '2':
                    return

    def submit(self, uid):
        '''
        Submit Document Name for Advisor to Evaluate
        If Currently Don't Have the Advisor Reject The Submission
        :param uid: User ID
        :return: None
        '''
        if uid != self.__uid:
            raise PermissionError("User ID Not Match")
        pr_table = self.db.search('Project')
        if not pr_table:
            raise LookupError("Table not found")
        proj_detail = pr_table.search('Lead', uid)
        if not proj_detail:
            raise LookupError('Project Not Found')
        table = self.db.search('Pending_project_approval')
        if not table:
            raise LookupError("Table not found")
        pid = proj_detail['ProjectID']
        if proj_detail['Advisor'].isspace():
            print('No Advisor; Please Get an Advisor before submitting')
            return

        # Currently Document stored as simple string to represent its filename
        doc = input('Insert Document: ')
        request = {'ProjectID': pid,
                   'Document': doc,
                   'Advisor': proj_detail['Advisor'],
                   'Response': 'Pending',
                   'Response_date': ''
                   }
        table.insert(request)

    def advisor_evaluate(self, uid):
        '''
        Start Evaluation Process for the project (Advisor)
        Add Committee and Score Element to its table
        :param uid: User ID
        :return: None
        '''
        if uid != self.__uid:
            raise PermissionError("User ID Not Match")
        if 'advisor' not in self.role:
            raise PermissionError("Your role has no permission")
        app_table = self.db.search("Pending_project_approval")
        if not app_table:
            raise LookupError("Table not found")
        pr_table = self.db.search("Project")
        if not pr_table:
            raise PermissionError("User ID Not Match")

        # Print all Pending Request
        app_table = app_table.filter(lambda x: x['Advisor'] == uid
                                     and x['Response'] == 'Pending')

        req_dict = {}
        print("Pending Approval Request")
        if all(i == '' for i in app_table.data[0].values()):
            print("Inbox Empty")
            return

        project_detail = pr_table.search('ProjectID', app_table.data[0]['ProjectID'])
        if not project_detail:
            raise LookupError("Project Detail Error")

        for i in range(len(app_table.data)):
            print(f'{i+1}. {project_detail["ProjectID"]} '
                  f'{project_detail["Title"]}'
                  f', Current Status: {project_detail["Status"]}')
            req_dict[str(i+1)] = [app_table.data[i], project_detail]
        while True:
            print('Response or Return:')
            print('1. Response\n2. Return')
            c = input('Your Choice: ')
            if c == '1':
                while True:
                    print("Please Select Request to Process")
                    req = input('Select Request: ')
                    if req in req_dict:
                        break
                target = req_dict[req]
                status = target[1]["Status"]
                # Approve or Deny Proposal of the project does not request committee to do so
                if status == 'New':
                    # Approve or Deny
                    print("Please Enter Your Response")
                    print('1. Accept\n2. Deny')
                    while True:
                        r = input("Your Response: ")
                        if r in ["1", "2"]:
                            break
                        print('Invalid Input')
                    if r == '1':
                        target[0]["Response"] = 'Approve'
                        target[0]["Response_date"] = self.time_format()
                        target[1]["Status"] = "Ongoing"
                    if r == '2':
                        target[0]["Response"] = 'Denied'
                        target[0]["Response_date"] = self.time_format()
                    return
                # Change User Role and Return to Menu(To start Invitation Process)
                if status == 'Ongoing':
                    self.role += '/reviewer'
                    self.__update_role(uid, self.role)
                    committee_dict = {'ProjectID': project_detail['ProjectID'],
                                      'Advisor': uid,
                                      'Reviewer1': '',
                                      'Reviewer2': '',
                                      'Student1': '',
                                      'Student2': '',
                                      'Student3': '',
                                      'Student4': '',
                                      'Student5': '',
                                      'Status': 'Ongoing'}
                    table = self.db.search('Project_Evaluate_Committee')
                    if not table:
                        raise LookupError("Project Evaluate Committee Table Not Found")
                    table.insert(committee_dict)
                    score_dict = {'ProjectID': project_detail['ProjectID'],
                                   'Advisor': 'r + p',
                                   'Reviewer1': 'r + p',
                                   'Reviewer2': 'r + p',
                                   'Student1': 'r + p',
                                   'Student2': 'r + p',
                                   'Student3': 'r + p',
                                   'Student4': 'r + p',
                                   'Student5': 'r + p',
                                   'Status': 'Ongoing'}
                    table = self.db.search('Project_Score_Result')
                    if not table:
                        raise LookupError("Score Table Not Found")
                    table.insert(score_dict)
                    return

                # Return if project is completed(Should not be)
                if status == 'Completed':
                    return
            if c == '2':
                return
            print('Invalid Input\n')

    def request_reviewer(self, a_uid):
        '''
        The Method for Advisor to Request a Reviewer's to help evaluate project
        :param a_uid: UserID
        :return: None
        '''
        if a_uid != self.__uid:
            raise PermissionError("User ID Not Match")
        s_m = input('Search by Name or by ID \nSearch Mode: ')
        while s_m not in ['ID', 'Name']:
            print('Invalid Search Mode')
            s_m = input('Search by Name or by ID \nSearch Mode: ')
        s_q = input('Search Query: ')

        # Finding Requested User Uid
        uid = self.__search_for_id(s_m, s_q, 'faculty')
        if not uid:
            uid = self.__search_for_id(s_m, s_q, 'student')

        if uid == a_uid:
            print("You Can't Invite Your Self")
            return
        if uid:
            i_table = self.db.search('Pending_Reviewer_Request')
            pr_table = self.db.search('Project')
            if i_table and pr_table:
                # Find Project ID and Project Lead by UID
                project_dict = pr_table.search('Advisor', a_uid)
                project_id = project_dict['ProjectID']

                # Check if user already in committee
                cmm_table = self.db.search('Project_Evaluate_Committee')
                if cmm_table:
                    cmm_table = cmm_table.filter(lambda x: x['ProjectID'] == project_id
                                                 and x['Status'] != 'Completed')
                    if uid in cmm_table.data[0].values():
                        print("User Already in Committee")
                        return


                # Check if Duplicates
                filtered_table = i_table.filter(lambda x: x['ProjectID'] == project_id)
                filtered_table = filtered_table.filter(lambda x: x['ReceiverID'] == uid and x['Response'] == 'Pending')
                if not all(i == '' for i in filtered_table.data[0].values()):
                    print('You already sent to this person')
                    return
                if uid in [project_dict['Lead'], project_dict['Member1'], project_dict['Member2']]:
                    print("Reviewer Can not be Member")
                    return
                i_table.insert({"ProjectID": project_id,
                                "ReceiverID": uid,
                                "Response": 'Pending',
                                "Response_date": ''})
            else:
                raise LookupError("Table not found")
        else:
            print('No Receiver found')

    def add_paper_score(self, uid):
        '''
        Add Score for The Final Report Paper
        :param uid: UserID
        :return: None
        '''
        if uid != self.__uid:
            raise PermissionError("User ID not Match")
        cm_table = self.db.search('Project_Evaluate_Committee')
        if not cm_table:
            raise LookupError('Table Not Found')
        sc_table = self.db.search('Project_Score_Result')
        if not sc_table:
            raise LookupError('Table Not Found')
        committee_filtered = cm_table.filter(lambda x:
                                             x['Advisor'] == uid or
                                             x['Reviewer1'] == uid or
                                             x['Reviewer2'] == uid or
                                             x['Student1'] == uid or
                                             x['Student2'] == uid or
                                             x['Student3'] == uid or
                                             x['Student4'] == uid or
                                             x['Student5'] == uid)
        if all(i == '' for i in committee_filtered.data[0]):
            print('There are no Project Assign to You')
            return
        pid = committee_filtered.data[0]['ProjectID']
        score_dict = sc_table.search('ProjectID', pid)
        if not score_dict:
            print('No Score Sheet Found')
            return
        # Get Role of the person in committee
        role = ''
        for i in committee_filtered.data[0]:
            if committee_filtered.data[0][i] == uid:
                role = i
                break

        if role.isspace():
            print('user do not have a role in this project')
            return

        if score_dict[role][0] != 'r':
            print('You has been review this project')
            return
        # Max of 10
        while True:
            score = input('Enter Your Score(Max of 10): ')
            if not self.__is_int(score):
                score = '-1'
            if 0 <= int(score) <= 10:
                score_dict[role] = score + score_dict[role].removeprefix('r')
                break
        self.__check_score()

    def add_present_score(self, uid):
        '''
        Add Score for Project Presentation
        :param uid: UserID
        :return: None
        '''
        if uid != self.__uid:
            raise PermissionError("User ID not Match")
        cm_table = self.db.search('Project_Evaluate_Committee')
        if not cm_table:
            raise LookupError('Table Not Found')
        sc_table = self.db.search('Project_Score_Result')
        if not sc_table:
            raise LookupError('Table Not Found')
        committee_filtered = cm_table.filter(lambda x:
                                             x['Advisor'] == uid or
                                             x['Reviewer1'] == uid or
                                             x['Reviewer2'] == uid or
                                             x['Student1'] == uid or
                                             x['Student2'] == uid or
                                             x['Student3'] == uid or
                                             x['Student4'] == uid or
                                             x['Student5'] == uid)
        if all(i == '' for i in committee_filtered.data[0]):
            print('There are no Project Assign to You')
            return
        pid = committee_filtered.data[0]['ProjectID']

        score_dict = sc_table.search('ProjectID', pid)
        if not score_dict:
            print('No Score Sheet Found')
            return
        # Get Role of the person in committee
        role = ''
        for i in committee_filtered.data[0]:
            if committee_filtered.data[0][i] == uid:
                role = i
                break

        if role.isspace():
            print('user do not have a role in this project')
            return
        if score_dict[role][-1] != 'p':
            print('You has been review this project')
            return
        # Max of 5
        while True:
            score = input('Enter Your Score(Max of 5): ')
            if not self.__is_int(score):
                score = '-1'
            if 0 <= int(score) <= 5 :
                score_dict[role] = score_dict[role].removesuffix('p') + score
                break
        self.__check_score()
