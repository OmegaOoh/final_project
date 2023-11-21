# BEGIN part 1

# import database module
import database
import random

main_db = database.Database()


# define a function called initializing
def initializing():
    # create an object to read an input csv file, persons.csv
    persons = database.read_csv('persons.csv')
    # create a 'persons' table
    persons = database.Table('persons', persons)
    # add the 'persons' table into the database
    main_db.insert(persons)
    # create a 'login' table
    # the 'login' table has the following keys (attributes):
    login_table = database.Table('Login')

    # add all persons into login Table with its information
    for i in persons.data:
        # let a username be a person's first name followed by a dot and the first letter of that person's last name
        login_info = {'person_id': i['ID'], 'username': i['fist'] + '.' + i['last'][0], 'password': '', 'role': ''}
        # Generate Password
        for _ in range(4):
            login_info['password'] += str(random.randint(0, 9))
        # Add role
        if i['type'] == 'student':
            login_info['role'] = 'Member'
        elif i['type'] == 'faculty':
            login_info['role'] = 'Faculty'
        elif i['type'] == 'admin':
            login_info['role'] = 'Admin'
        # create a login table by performing a series of insert operations; each insert adds a dictionary to a list
        login_table.insert_data(login_info)

    # add the 'login' table into the database
    main_db.insert(login_table)


def login():
    user = input('Please enter your username: ')
    table = main_db.search('Login')
    user_dict = table.search('username', user)
    if user_dict is None:
        print('user not found')
        return None
    pwd = input('Please enter your password: ')
    if user_dict['password'] == pwd:
        return user_dict['person_id'], user_dict['role']


# make calls to the initializing and login functions defined above
initializing()
print(main_db.search('Login'))
val = login()
print(val)

# END part 1

# CONTINUE to part 2 (to be done for the next due date)

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id

# if val[1] = 'admin':
    # do admin related activities
# elif val[1] = 'advisor':
    # do advisor related activities
# elif val[1] = 'lead':
    # do lead related activities
# elif val[1] = 'member':
    # do member related activities
# elif val[1] = 'faculty':
    # do faculty related activities
