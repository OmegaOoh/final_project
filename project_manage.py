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

# define a function called exit
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

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id
if not val:
    raise LookupError()
if val[1] == 'admin':
    # see and do admin related activities
    ops = Operation(val[0], val[1], main_db)
    function_dict = {'Read Data': ops.read_all_db(val[0], val[1])}
    ops.read_all_db(val[0], val[1])

elif val[1] == 'student':
    # see and do student related activities
    pass
elif val[1] == 'member':
    # see and do member related activities
    pass
elif val[1] == 'lead':
    # see and do lead related activities
    pass
elif val[1] == 'faculty':
    # see and do faculty related activities
    pass
elif val[1] == 'advisor':
    # see and do advisor related activities
    pass


# once everyhthing is done, make a call to the exit function
exit()
