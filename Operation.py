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

    def __init__(self, uid, role, db: database.Database):
        self.__uid = uid
        self.role = role
        self.db = db

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, r):
        if r in ['student', 'member', 'lead', 'faculty', 'advisor','admin']:
            self.__role = r
        else:
            ValueError('INVALID ROLE')

    def remove_element(self ,uid, table, index):
        if self.role != 'admin' or uid != self.__uid:
            ValueError('No Permission')
        else:
            table.data.remove(index)

    # TODO Actually Generate ProjectID
    def create_project(self, project_title, uid):
        if self.__uid != uid:
            return
        else:
            table = self.db.search('Project')
            if table:
                project_id = self.__gen_project_id(project_title)
                if project_id:
                    table.insert(project_id, project_id, uid, '', '', '', 'New')

    @staticmethod
    def __gen_project_id(project_title):
        proj_id = len(project_title)
        proj_id += str(time.time())[-6:-4]
        return proj_id

    def modify_project_detail(self, uid):
        if self.__uid != uid:
            return
        else:
            table = self.db.search('Project')
            if table:
                project = table.search('lead', uid)
                self.__project_modify_menu(project)

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
            return None

    def send_invites(self, l_uid, search_mode, query):
        if l_uid != self.__uid:
            return
        uid = self.__search_for_id(search_mode, query, ['student', 'member', 'lead'])
        if uid:
            i_table = self.db.search('Member_pending_request')
            pr_table = self.db.search('Project')
            if i_table and pr_table:
                # Find Project ID and Project Lead by UID
                project_id = pr_table.search('lead', l_uid)['ProjectID']
                i_table.insert(project_id, uid, 'pending', '')
        else:
            print('No Receiver uid found')

    def request_advisor(self, l_uid, search_mode, query):
        if l_uid != self.__uid:
            return
        uid = self.__search_for_id(search_mode, query, ['faculty', 'advisor'])
        if uid:
            i_table = self.db.search('Advisor_pending_request')
            pr_table = self.db.search('Project')
            if i_table and pr_table:
                # Find Project ID and Project Lead by UID
                project_id = pr_table.search('lead', l_uid)['ProjectID']
                i_table.insert(project_id, uid, 'pending', '')
        else:
            print('No Receiver uid found')

    def accept_deny_request(self, request, response: bool):
        if not (request['response'] and request['Response_date']):
            print('Request Invalid')
            return
        if response:
            request['response'] = 'Accepted'
        else:
            request['response'] = 'Denied'
        request['Response_date'] = self.time_format()

