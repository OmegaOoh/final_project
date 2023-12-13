import copy
import os
import database
from operation import Session

main_db = database.Database()


# define a function called initializing
def initializing():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    csv_ls = []
    for i in os.listdir(__location__):
        if i.endswith('.csv'):
            csv_ls.append(i)

    for i in csv_ls:
        table = database.Table(i[:-4], database.read_csv(i))
        main_db.insert(table)

    if 'Project.csv' not in csv_ls:
        table = database.Table("Project", {"ProjectID": '',
                                           'Title': '',
                                           'Lead': '',
                                           'Member1': '',
                                           'Member2': '',
                                           'Advisor': '',
                                           'Status': ''})
        main_db.insert(table)
    if 'Advisor_pending_request.csv' not in csv_ls:
        table = database.Table('Advisor_pending_request', {"ProjectID": '',
                                                           "ReceiverID": '',
                                                           "Response": '',
                                                           "Response_date": ''})
        main_db.insert(table)
    if 'Member_pending_request.csv' not in csv_ls:
        table = database.Table('Member_pending_request', {"ProjectID": '',
                                                          "ReceiverID": '',
                                                          "Response": '',
                                                          "Response_date": ''})

        main_db.insert(table)
    if 'Pending_project_approval' not in csv_ls:
        table = database.Table("Pending_project_approval", {'ProjectID': '',
                                                            'Document': '',
                                                            'Advisor': '',
                                                            'Response': '',
                                                            'Response_date': ''})
        main_db.insert(table)

    if "Pending_Reviewer_Request" not in csv_ls:
        table = database.Table("Pending_Reviewer_Request", {'ProjectID': '',
                                                            'ReceiverID': '',
                                                            'Response': '',
                                                            'Response_date': ''})
        main_db.insert(table)

    if "Project_Evaluate_Committee" not in csv_ls:
        table = database.Table("Project_Evaluate_Committee", {'ProjectID': '',
                                                              'Advisor': '',
                                                              'Reviewer1': '',
                                                              'Reviewer2': '',
                                                              'Student1': '',
                                                              'Student2': '',
                                                              'Student3': '',
                                                              'Student4': '',
                                                              'Student5': '',
                                                              'Status': ''})
        main_db.insert(table)

    if "Project_Score_Result" not in csv_ls:
        table = database.Table("Project_Score_Result", {'ProjectID': '',
                                                        'Advisor': '',
                                                        'Reviewer1': '',
                                                        'Reviewer2': '',
                                                        'Student1': '',
                                                        'Student2': '',
                                                        'Student3': '',
                                                        'Student4': '',
                                                        'Student5': '',
                                                        'Status': ''})
        main_db.insert(table)


def login():
    table = main_db.search('login')
    while True:
        user = input('Please enter your username: ')
        user_dict = table.search('username', user)
        if user_dict is None:
            print('user not found')
            continue
        break

    i = 0
    while i < 5:

        pwd = input('Please enter your password: ')
        if user_dict['password'] == pwd:
            return [user_dict['ID'], user_dict['role']]
        print('Access Denied')
        print()
        i += 1
    raise PermissionError("Maximum Tried Reached")


###################################################################################################
# Decide Roles and its function
def update_function(params):
    '''
    This Function will return function dict according to the role of the user
    :param params: List include userID and role
    :return: function dict
    '''
    if 'admin' in params[1]:
        # see and do admin related activities
        return {'Read Data':
                    [session.read_all_db, [params[0]]],
                'Modify Data':
                    [session.modify, [params[0]]],
                'Remove Data':
                    [session.remove_data, [params[0]]],
                'Exit': [exit, [None]]}

    if 'student' in params[1]:
        # see and do student related activities
        func_dict = {'Create Project':
                         [session.create_project, [params[0]]],
                     'Show Invitation':
                         [session.response_request_menu, [params[0],
                                                          main_db.search('Member_pending_request')]],
                     'Show Review Request':
                         [session.response_request_menu, [params[0],
                                                          main_db.search('Pending_Reviewer_Request')]]}
        # Add Reviewer Ability
        if 'reviewer' in params[1]:
            func_dict.pop('Show Review Request')
            func_dict['Add Paper Score'] = [session.add_paper_score, [params[0], func_dict]]
            func_dict['Add Presentation Score'] = [session.add_present_score, [params[0], func_dict]]

        func_dict['Exit'] = [exit, [None]]
        return func_dict
    if 'member' in params[1]:
        # see and do member related activities
        func_dict = {'See Project Detail':
                         [session.show_user_project, [params[0]]],
                     'Show Review Request':
                         [session.response_request_menu, [params[0],
                                                          main_db.search('Pending_Reviewer_Request')]]
                     }
        if 'reviewer' in params[1]:
            func_dict.pop('Show Review Request')
            func_dict['Add Paper Score'] = [session.add_paper_score, [params[0], func_dict]]
            func_dict['Add Presentation Score'] = [session.add_present_score, [params[0], func_dict]]

        func_dict['Exit'] = [exit, [None]]
        return func_dict
    if 'lead' in params[1]:
        # see and do lead related activities
        pr_table = main_db.search('Project')
        project = pr_table.search('Lead', userid)
        member_inv = (main_db.search('Member_pending_request')
                      .filter(lambda x: x['ProjectID'] == project['ProjectID']))
        advisor_inv = (main_db.search('Advisor_pending_request')
                       .filter(lambda x: x['ProjectID'] == project['ProjectID']))

        func_dict = {'Show Project Detail':
                         [session.show_user_project, [params[0]]],
                     'Modify Project Detail':
                         [session.modify_project_detail, [params[0]]],
                     'Find Member':
                         [session.read_filtered_person, [params[0], 'type', 'student']],
                     'Sends Invites':
                         [session.send_invites, [params[0]]],
                     'Find Advisor':
                         [session.read_filtered_person, [params[0], 'type', 'faculty']],
                     'Request Advisor':
                         [session.request_advisor, [params[0]]],
                     'Show Review Request':
                         [session.response_request_menu, [params[0],
                                                          main_db.search('Pending_Reviewer_Request')]],
                     'Show Sent Member Invitation':
                         [session.read_as_table, [val[0], member_inv]],
                     'Show Sent Advisor Request':
                         [session.read_as_table, [val[0], advisor_inv]],
                     'Submit':
                         [session.submit, [params[0]]]}

        # Remove Ability to Find and Send Member Invites
        if project['Member1'] != '' and project['Member2'] != '':
            func_dict.pop('Find Member')
            func_dict.pop('Sends Invites')

        # Remove Ability to Find and Request Advisor
        if project['Advisor'] != '':
            func_dict.pop('Find Advisor')
            func_dict.pop('Request Advisor')

        # Add Reviewer Ability
        if 'reviewer' in params[1]:
            func_dict.pop('Show Review Request')
            func_dict['Add Paper Score'] = [session.add_paper_score, [params[0], func_dict]]
            func_dict['Add Presentation Score'] = [session.add_present_score, [params[0], func_dict]]

        func_dict['Exit'] = [exit, [None]]
        return func_dict

    if 'faculty' in params[1]:
        # see and do faculty related activities
        func_dict = {'Read Project Detail':
                         [session.read_as_table, [params[0], main_db.search('Project')]],
                     'Show Request':
                         [session.response_request_menu, [params[0],
                                                          main_db.search('Advisor_pending_request')]],
                     'Show Review Request':
                         [session.response_request_menu, [params[0],
                                                          main_db.search('Pending_Reviewer_Request')]]
                     }
        # Add Reviewer Ability
        if 'reviewer' in params[1]:
            func_dict['Add Paper Score'] = [session.add_paper_score, [params[0], func_dict]]
            func_dict['Add Presentation Score'] = [session.add_present_score, [params[0], func_dict]]
        func_dict['Exit'] = [exit, [None]]
        return func_dict

    if 'advisor' in params[1]:
        # see and do advisor related activities
        func_dict = {'Read Project Detail': [session.read_as_table, [params[0], main_db.search('Project')]],
                     'Show Request':
                         [session.response_request_menu, [params[0],
                                                          main_db.search('Advisor_pending_request')]],
                     'Evaluate':
                         [session.advisor_evaluate, [params[0]]]}
        if 'reviewer' in params[1]:
            func_dict.pop('Evaluate')
            cmm_tab = main_db.search('Project_Evaluate_Committee')
            cmm_tab = cmm_tab.filter(lambda x: x['Status'] != 'Completed')
            committee = cmm_tab.search('Advisor', userid)
            b_faculty = all(committee[i] != '' for i in ['Reviewer1', 'Reviewer2'])
            b_student = all(committee[i] != '' for i in ['Student1', 'Student2', 'Student3', 'Student4', 'Student5'])
            if not b_student or not b_faculty:
                table = main_db.search('persons')
                table = table.filter(lambda x: x['type'] != 'admin')
                table.table_name = 'Reviewer'
                if table:
                    if not b_faculty and b_student:
                        table.filter(lambda x: x['type'] == 'faculty')
                    if not b_student and b_faculty:
                        table.filter(lambda x: x['type'] == 'student')
                    func_dict['Find Reviewer'] = [session.read_as_table, [params[0], table]]
                    func_dict['Request Reviewer'] = [session.request_reviewer, [params[0]]]
                    rev_inv = (main_db.search('Pending_Reviewer_Request')
                               .filter(lambda x: x['ProjectID'] == committee['ProjectID']))
                    func_dict['Show Sent Request'] = [session.read_as_table,[params[0], rev_inv]]
            func_dict['Add Paper Score'] = [session.add_paper_score, [params[0], func_dict]]
            func_dict['Add Presentation Score'] = [session.add_present_score, [params[0], func_dict]]
        func_dict['Exit'] = [exit, [None]]
        return func_dict


# Print out menu and give user ability to use the program
def menu():
    '''
    Function to using as a main menu of the application
    This Function will call method inside Session Class
    :return: None
    '''
    while True:
        print()
        table = main_db.search('login')
        r = table.search('ID', userid)
        func_dict = update_function([userid, r['role']])
        # Handle Reviewed content
        if 'reviewer' in r['role'][1]:
            cm_table = main_db.search('Project_Evaluate_Committee')
            if not cm_table:
                raise LookupError('Table Not Found')
            sc_table = main_db.search('Project_Score_Result')
            if not sc_table:
                raise LookupError('Table Not Found')
            committee_filtered = cm_table.filter(lambda x:
                                                 x['Advisor'] == userid or
                                                 x['Reviewer1'] == userid or
                                                 x['Reviewer2'] == userid or
                                                 x['Student1'] == userid or
                                                 x['Student2'] == userid or
                                                 x['Student3'] == userid or
                                                 x['Student4'] == userid or
                                                 x['Student5'] == userid)

            pid = committee_filtered.data[0]['ProjectID']

            score_dict = sc_table.search('ProjectID', pid)
            if not score_dict:
                print('No Score Sheet Found')
                return
            # Get Role of the person in committee
            role = ''
            if committee_filtered:
                for i in committee_filtered.data[0]:
                    if committee_filtered.data[0][i] == userid:
                        role = i
                        break
            if not role.isspace():
                session.update_review_status(score_dict[role], func_dict)
                print(func_dict)

        print(f"Login as {userid}. Role: {r['role']}")
        select_dict = {}
        for i in range((len(list(func_dict.keys())))):
            print(f'{i + 1}. {list(func_dict.keys())[i]}')
            select_dict[str(i + 1)] = list(func_dict.keys())[i]
        while True:
            c = input('Enter Choice: ')
            if c in select_dict:
                func_key = select_dict[c]
                func = func_dict[func_key][0]
                if func == exit:
                    return
                params = func_dict[func_key][1]
                func(*params)
                break
            print('Invalid Input')


###################################################################################################
def exit():
    '''
    Write Data in The Table into csv file
    Exit the program
    :return: None
    '''
    for i in main_db.table_name():
        table = main_db.search(i)
        table.write_to_csv()


# make calls to the initializing and login functions defined above
initializing()
val = login()

userid = val[0]

session = Session(val[0], main_db)
if not val:
    raise LookupError()

# Open Menu
menu()
# once everything is done, make a call to the exit function
exit()
