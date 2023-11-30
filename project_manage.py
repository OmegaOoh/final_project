import os
import database
import operation
from operation import Operation

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
        else:
            print('Access Denied')
            print()
            i += 1
    raise PermissionError("Maximum Tried Reached")


########################################################################################################################
# Operation
def update_function(params):
    if params[1] == 'admin':
        # see and do admin related activities
        return {'Read Data': [ops.read_all_db, [params[0]]],
                'Modify Data': [ops.modify, [params[0]]],
                'Remove Data': [ops.remove_data, [params[0]]],
                'Exit': [exit, [None]]}

    elif params[1] == 'student':
        # see and do student related activities
        return {'Create Project': [ops.create_project, [params[0]]],
                'Show Invitation': [ops.response_request_menu, [params[0],
                                    main_db.search('Member_pending_request')]],
                'Exit': [exit, [None]]}
    elif params[1] == 'member':
        # see and do member related activities
        return {'See Project Detail': [ops.show_user_project, [params[0]]],
                'Show Invitation': [ops.response_request_menu, [params[0],
                                    main_db.search('Member_pending_request')]],
                'Exit': [exit, [None]]}
    elif params[1] == 'lead':
        # see and do lead related activities
        return {'Show Project Detail': [ops.show_user_project, [params[0]]],
                'Modify Project Detail': [ops.modify_project_detail, [params[0]]],
                'Find Member': [ops.read_filtered_person, [params[0], 'type', 'student']],
                'Sends Invites': [ops.send_invites, [params[0]]],
                'Find Advisor': [ops.read_filtered_person, [params[0], 'type', 'faculty']],
                'Request Advisor': [ops.request_advisor, [params[0]]],
                'Show Invitation': [ops.response_request_menu, [params[0],
                                    main_db.search('Member_pending_request')]],
                'Submit': [ops.submit, [params[0]]],
                'Exit': [exit, [None]]}
    elif params[1] == 'faculty':
        # see and do faculty related activities
        return {'Read Project Detail': [ops.read_as_table, main_db.search('Project')],
                'Show Request': [ops.response_request_menu, [params[0],
                                 main_db.search('Advisor_pending_request')]],
                'Exit': [exit, [None]]}
    elif params[1] == 'advisor':
        # see and do advisor related activities
        return {'Read Project Detail': [ops.read_as_table, main_db.search('Project')],
                'Show Request': [ops.response_request_menu, [params[0],
                                 main_db.search('Advisor_pending_request')]],
                'Exit': [exit, [None]]}


def menu():
    while True:
        print()
        table = main_db.search('login')
        r = table.search('ID', userid)
        func_dict = update_function([userid, r['role']])
        print(f"Login as {userid}. Role: {r['role']}")
        select_dict = {}
        for i in range((len(list(func_dict.keys())))):
            print(f'{i+1}. {list(func_dict.keys())[i]}')
            select_dict[str(i+1)] = list(func_dict.keys())[i]
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


########################################################################################################################
def exit():
    for i in main_db.table_name():
        table = main_db.search(i)
        table.write_to_csv()


# make calls to the initializing and login functions defined above
initializing()
print(main_db.search('login'))
val = login()

userid = val[0]

ops = Operation(val[0], main_db)
if not val:
    raise LookupError()


# Open Menu
menu()
# once everything is done, make a call to the exit function
exit()
