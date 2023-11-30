import time
import database
from database import Table


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

    def __update_role(self):
        # Using Person as a main Table
        login_table = self.db.search('login')
        person_table = self.db.search('person')
        if not (login_table and person_table):
            raise LookupError("Table Not Found; Can't Update.")
        # Loop list of ID to Update Role
        for i in person_table.select('ID'):
            role_person = person_table.search('ID', i)['role']
            role_login = login_table.search('ID', i)['role']
            if role_person != role_login:
                login_table.search('ID', i)['role'] = role_person

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

    def __search_for_id(self, mode, query, role: list):
        uid = None
        p_table = self.db.search('persons')
        if p_table:
            # Search mode 'Name' / 'ID'
            if mode == 'Name':
                dict_p = p_table.search('first', query)
                if dict_p:
                    uid = dict_p['ID']
                else:
                    print('User not found')
                    return None
            elif mode == 'ID':
                uid = query
            # Check Role
            dict_p = p_table.search['ID', uid]
            if dict_p:
                if dict_p['role'] in role:
                    return uid
                else:
                    print('Invalid User Role')
                    return None
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
        if r in ['student', 'member', 'lead', 'faculty', 'advisor','admin']:
            self.__role = r
        else:
            ValueError('INVALID ROLE')

    def create_project(self, uid, project_title):
        if self.__uid != uid:
            raise PermissionError("User ID Not Match")
        else:
            table = self.db.search('Project')
            if table:
                project_id = self.__gen_project_id(project_title)
                if project_id:
                    table.insert(project_id, project_id, uid, '', '', '', 'New')

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
                project = table.search('lead', uid)
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
                print('Current Title',project['Title'])
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

    def send_invites(self, l_uid, search_mode, query):
        if l_uid != self.__uid:
            raise PermissionError("User ID Not Match")
        uid = self.__search_for_id(search_mode, query, ['student', 'member', 'lead'])
        if uid:
            i_table = self.db.search('Member_pending_request')
            pr_table = self.db.search('Project')
            if i_table and pr_table:
                # Find Project ID and Project Lead by UID
                project_id = pr_table.search('lead', l_uid)['ProjectID']
                i_table.insert(project_id, uid, 'Pending', 'Pending')
            else:
                raise LookupError("Table not found")
        else:
            print('No Receiver uid found')

    def request_advisor(self, l_uid, search_mode, query):
        if l_uid != self.__uid:
            raise PermissionError("User ID Not Match")
        uid = self.__search_for_id(search_mode, query, ['faculty', 'advisor'])
        if uid:
            i_table = self.db.search('Advisor_pending_request')
            pr_table = self.db.search('Project')
            if i_table and pr_table:
                # Find Project ID and Project Lead by UID
                project_id = pr_table.search('lead', l_uid)['ProjectID']
                i_table.insert(project_id, uid, 'Pending', 'Pending')
            else:
                LookupError("Table not found")
        else:
            print('No Receiver uid found')

    def accept_deny_request(self, request, response: bool):
        if not (request['response'] in ['Accepted', 'Denied'] and request['Response_date'] == ''):
            print('Request Already Response')
            return
        if response:
            request['Response'] = 'Accepted'
        else:
            request['Response'] = 'Denied'
        request['Response_date'] = self.time_format()
        
    def submit(self, uid, pid, doc):
        if uid != self.__uid:
            raise PermissionError("User ID Not Match")
        pr_table = self.db.search('Project')
        if not pr_table:
            raise LookupError("Table not found")
        proj_detail = pr_table.search('ID', pid)
        if not proj_detail:
            raise LookupError['Project Not Found']
        if proj_detail['lead'] != uid:
            raise PermissionError("User does not Have Permission")

        table = self.db.search('Pending_project_approval')
        if not table:
            raise LookupError("Table not found")

        request = {'ProjectID': pid,
                   'Document': doc,
                   'Advisor': proj_detail['Advisor'],
                   'Response': 'Pending',
                   'Response_date': 'Pending'
                   }
        table.insert(request)
            

