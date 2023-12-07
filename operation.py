import time
import database
from database import Table


# Handle Common Methods
class Operation:
    @staticmethod
    def time_format():
        curr_time = time.localtime()
        formatted_time = str(curr_time.tm_mon) + '/' + str(curr_time.tm_mday) + '/' + str(curr_time.tm_year)
        return formatted_time
    
    @staticmethod
    def __is_int(x):
        try:
            int(x)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_name(db: database.Database, uid):
        p_table = db.search('persons')
        if p_table:
            p_table.search('ID', uid)
            
    def __init__(self, uid, db: database.Database):
        self.db = db
        self.__uid = uid
        self.role = self.__check_role(uid)

    def __check_role(self, uid):
        login_table = self.db.search('login')
        if not login_table:
            raise LookupError("Table Not Found; Can't Validate Roles.")
        login_data = login_table.search("ID", uid)
        if not login_data:
            raise LookupError('No User ID Found')
        return login_data['role']

    def __update_role(self, uid, new_role):
        if new_role in ['student', 'member', 'lead', 'faculty', 'advisor','admin']:
            table = self.db.search('login')
            if table:
                user_dict = table.search('ID', uid)
                user_dict['role'] = new_role
                self.role = new_role

    def __update_project(self):
        pr_table = self.db.search('Project')
        if not pr_table:
            raise LookupError("Project Table not Found")
        adv_req = self.db.search('Advisor_pending_request')
        if not adv_req:
            raise LookupError("Advisor Request Table not Found")
        mem_req = self.db.search('Member_pending_request')
        if not mem_req:
            raise LookupError("Member Invites Table not Found")

        adv_acc_req = adv_req.filter(lambda x: x['Response'] == 'Accepted')
        if adv_acc_req:
            for i in adv_acc_req.data:
                pr_id = i['ProjectID']
                project = pr_table.search('ProjectID', pr_id)
                if project and project['Advisor'] == '':
                    pr_table.search('ProjectID', pr_id)['Advisor'] = i['ReceiverID']
                adv_pending_req = adv_req.filter(lambda x: x['ProjectID'] == pr_id)
                if adv_pending_req:
                    for j in adv_pending_req.data:
                        if j['Response'] == 'Pending':
                            j['Response'] = 'Expired'
                            j['Response_date'] = self.time_format()

        mem_acc_req = mem_req.filter(lambda x: x['Response'] == 'Accepted')

        if mem_acc_req:
            for i in mem_acc_req.data:
                pr_id = i['ProjectID']
                project = pr_table.search('ProjectID', pr_id)
                if project:
                    if project and project['Member1'] == '':
                        pr_table.search('ProjectID', pr_id)['Member1'] = i['ReceiverID']
                    elif project and pr_table.search('ProjectID', pr_id)['Member2'] == '':
                        pr_table.search('ProjectID', pr_id)['Member2'] = i['ReceiverID']
                    mem_pending_req = mem_req.filter(lambda x: x['ProjectID'] == pr_id and x['Response'] == 'Pending')
                    if mem_pending_req:
                        if project['Member1'] != '' and project['Member2'] != '':
                            for j in mem_pending_req.data:
                                if j['Response'] == 'Pending':
                                    j['Response'] = 'Expired'
                                    j['Response_date'] = self.time_format()

    ###################################################################################################################
    # Admin Related Staff

    def read_all_db(self, uid):
        if uid != self.__uid or self.__role != 'admin':
            raise PermissionError()
        for i in range(len(self.db.table_name())):
            print(self.db.search(self.db.table_name()[i]).to_table())
            print()

    def __remove_by_data(self,uid, table_name, key, value):
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
        if uid != self.__uid or self.__role != 'admin':
            raise PermissionError()
        target_table = self.db.search(table_name)
        if not target_table:
            print('Table Not Found; Nothing was changed')
            return
        self.__remove_element(uid, target_table, order - 1)

    def __modify_data(self, uid, table_name, key_search, val_search, key_mod, val_mod):
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
        if uid != self.__uid or self.__role != 'admin':
            raise PermissionError()
        else:
            table.remove_data(index)

    def remove_data(self, uid):
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
        tab_name = input('Table Name: ')
        key_s = input('Key to Search: ')
        val_s = input('Searching Value: ')
        key_m = input('Key to Modify: ')
        val_m = input('Value to Modify: ')
        self.__modify_data(uid, tab_name, key_s, val_s, key_m, val_m)

    ###################################################################################################################

    def read_as_table(self, uid, table):
        if uid != self.__uid:
            raise PermissionError()
        print(table.to_table())

    def read_filtered_person(self, uid, key, val):
        if uid != self.__uid:
            raise PermissionError()
        project = self.db.search('persons')
        if project:
            filtered = project.filter(lambda x: x[key] == val)
            print(filtered.to_table())
        else:
            raise LookupError('Table not found')

    def __search_for_id(self, mode, query, type: str):
        uid = None
        p_table = self.db.search('persons')
        p_table = p_table.filter(lambda x: x['type'] == type)
        if p_table:
            # Search mode 'Name' / 'ID'
            if mode == 'Name':
                dict_p = p_table.search('first', query)
                if dict_p:
                    return dict_p['ID']
                else:
                    print('User not found')
                    return None
            elif mode == 'ID':
                dict_p = p_table.search('ID', query)
                if dict_p:
                    return query
                else:
                    print('User not found')
        else:
            raise LookupError("Table not found")
    
    def __get_role(self, uid):
        table = self.db.search('persons')
        if table:
            elem = table.search('ID', uid)
            return elem['role']
        else:
            raise LookupError("Table not found")
        
    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, r):
        if r in ['student', 'member', 'lead', 'faculty', 'advisor', 'admin']:
            self.__role = r
        else:
            ValueError('INVALID ROLE')

    def create_project(self, uid):
        if self.__uid != uid:
            raise PermissionError("User ID Not Match")
        else:
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
        uniqueid = str(time.gmtime().tm_year)[-2:]
        uniqueid += str(time.time_ns())[-8:-3]
        uniqueid += str(len(project_title) % 10)
        uniqueid += str(sum([int(i) for i in uniqueid]) % 100)
        return uniqueid

    def modify_project_detail(self, uid):
        if self.__uid != uid:
            raise PermissionError("User ID Not Match")
        else:
            table = self.db.search('Project')
            if table:
                project = table.search('Lead', uid)
                self.__project_modify_menu(project)
            else:
                raise LookupError("Table not found")

    def __project_modify_menu(self, project):
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
        if uid != self.__uid:
            raise PermissionError()
        project = self.db.search('Project')
        if project:
            filtered = project.filter(lambda x: uid in [x['Lead'], x['Member1'], x['Member2']])
            print(filtered.to_table())
        else:
            raise LookupError('Table not found')

    def send_invites(self, l_uid):
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

    def request_advisor(self, l_uid):
        if l_uid != self.__uid:
            raise PermissionError("User ID Not Match")
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
        if request['Response'] != 'Pending' and request['Response_date'] != '':
            print('Request Already Response')
            return
        if response:
            request['Response'] = 'Accepted'
            self.__update_role(uid, to_be)
        else:
            request['Response'] = 'Denied'
        request['Response_date'] = self.time_format()
        self.__update_project()

    def response_request_menu(self, uid, table):
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
        else:
            for i in range(len(request_data.data)):
                project_detail = pr_table.search('ProjectID', request_data.data[i]['ProjectID'])
                if project_detail:
                    print(f'{i+1}. Project: {project_detail["ProjectID"]} {project_detail["Title"]}')
                    req_dict[str(i+1)] = request_data.data[i]
            # Give User a Choice to Return or Response to request
            while True:
                print('Choice')
                print("1. Response \n2. Return")
                c = input('Choice: ')
                if c in ['1', '2']:
                    if c == '1':
                        while True:
                            inv = input('Select Request: ')
                            if inv in req_dict:
                                print('1 to Accept 2 to Deny')
                                r = input('Your Response: ')
                                _map = {'1': True, '2': False}
                                self.__accept_deny_request(req_dict[inv], _map[r], uid, to_be)
                                break
                    if c == '2':
                        return
                    break

    def submit(self, uid):
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

        # Currently Document stored as simple string to represent its filename
        doc = input('Insert Document: ')
        request = {'ProjectID': pid,
                   'Document': doc,
                   'Advisor': proj_detail['Advisor'],
                   'Response': 'Pending',
                   'Response_date': ''
                   }
        table.insert(request)

    def evaluate(self, uid):
        if uid != self.__uid:
            raise PermissionError("User ID Not Match")
        app_table = self.db.search("Pending_project_approval")
        if not app_table:
            raise LookupError("Table not found")
        pr_table = self.db.search("Project")
        if not pr_table:
            raise PermissionError("User ID Not Match")

        print("Project Status Changed.")


class Scoring:

    @staticmethod
    def __is_int(x):
        try:
            int(x)
            return True
        except ValueError:
            return False

    def __init__(self, uid):
        self.__uid = uid
        self.__score = 0

    @property
    def uid(self):
        return self.__uid

    @property
    def score(self):
        return self.__score

    def add_report_score(self):
        # Max of 10
        while True:
            score = input('Enter Your Score: ')
            if self.__is_int(score):
                score = int(score)
                if 0 <= score <= 10:
                    self.__score += score
                    break


    def add_presentation_score(self):
        # Max of 5
        while True:
            score = input('Enter Your Score: ')
            if self.__is_int(score):
                score = int(score)
                if 0 <= score <= 5:
                    self.__score += score
                    break