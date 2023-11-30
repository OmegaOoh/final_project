import os
import database
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
        table = database.Table("Project", {"ID": '',
                                                             'Title': '',
                                                             'Lead': '',
                                                             'Member1': '',
                                                             'Member2': '',
                                                             'Advisor': '',
                                                             'Status': ''
                                                             })
        main_db.insert(table)
    if 'Advisor_pending_request.csv' not in csv_ls:
        table = database.Table('Advisor_pending_request', {"ProjectID": '',
                                                                             "ReceiverID": '',
                                                                             "Response": '',
                                                                             "Response_date": ''
                                                                             })
        main_db.insert(table)
    if 'Member_pending_request.csv' not in csv_ls:
        table = database.Table('Member_pending_request', {"ProjectID": '',
                                                                            "ReceiverID": '',
                                                                            "Response": '',
                                                                            "Response_date": ''
                                                                           })

        main_db.insert(table)

    if 'Pending_project_approval' not in csv_ls:
        table = database.Table("Pending_project_approval", {'ProjectID': '',
                                                                              'Document': '',
                                                                              'Advisor': '',
                                                                              'Response': '',
                                                                              'Response_date': ''})
        main_db.insert(table)


def login():
    user = input('Please enter your username: ')
    table = main_db.search('login')
    user_dict = table.search('username', user)
    if user_dict is None:
        print('user not found')
        return None
    pwd = input('Please enter your password: ')
    if user_dict['password'] == pwd:
        return [user_dict['ID'], user_dict['role']]
    return None


########################################################################################################################
# Operation
def menu(func_dict):
    while True:
        select_dict = {}
        for i in range((len(list(func_dict.keys())))):
            print(f'{i+1}. {list(func_dict.keys())[i]}')
            select_dict[str(i+1)] = list(func_dict.keys())[i]
        while True:
            c = input('Enter Choice: ')
            if c in select_dict:
                func_key = select_dict[c]
                func = func_dict[func_key][0]
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
print(main_db)
print(main_db.search('login'))
val = login()
print(val)

ops = Operation(val[0], main_db)
if not val:
    raise LookupError()

function_dict = {}
if val[1] == 'admin':
    # see and do admin related activities
    function_dict = {'Read Data': [ops.read_all_db, [val[0]]],
                     'Modify Data': [ops.modify, [val[0]]],
                     'Remove Data': [ops.remove_data, [val[0]]],
                     'Exit': [exit, None]}

elif val[1] == 'student':
    # see and do student related activities
    function_dict = {'Create Project': [ops.create_project, [val[0],]]}
elif val[1] == 'member':
    # see and do member related activities
    function_dict = {}
elif val[1] == 'lead':
    # see and do lead related activities
    function_dict = {}
elif val[1] == 'faculty':
    # see and do faculty related activities
    function_dict = {'Read Project Detail': [ops.read_as_table, main_db.search('Project')],
                     'Response To Request': [ops.response_request_menu, [val[0], 'Advisor_pending_request']],
                     'Exit': [exit, None]}
elif val[1] == 'advisor':
    # see and do advisor related activities
    function_dict = {'Read Project Detail': [ops.read_as_table, main_db.search('Project')],
                     'Response To Request': [ops.response_request_menu, [val[0], 'Advisor_pending_request']],
                     'Exit': [exit, None]}

# Call Open Menu
if function_dict != {}:
    menu(function_dict)
# once everything is done, make a call to the exit function
exit()
