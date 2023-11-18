# import database module
import database
import random
# start by adding the admin related code
main_db = database.Database()

# create an object to read an input csv file, persons.csv
persons = database.read_csv('persons.csv')
# create a 'persons' table
persons_table = database.Table('persons', persons)
# add the 'persons' table into the database
main_db.insert(persons_table)
# create a 'login' table
# the 'login' table has the following keys (attributes):
login_table = database.Table('Login')

# add all persons into login Table with its information
for i in persons_table.data:
    login_info = {'person_id': i['ID'], 'username': i['fist'] + '.' + i['last'], 'password': '', 'role': ''}
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


# code that performs a login task; asking a user for a username and password;
# returning [person_id, role] if valid, otherwise returning None
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


# Test Code
print(main_db)
print(login())
