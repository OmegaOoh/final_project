# try wrapping the code below that reads a persons.csv file in a class and make it more general such that it can read in any csv file

import csv, os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

persons = []
with open(os.path.join(__location__, 'persons.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        persons.append(dict(r))


class Database:
    def __init__(self):
        self.__tables = []

    def insert(self, table: "Table Class"):
        self.__tables.append(table)

    def __str__(self):
        output = ''
        for i in self.__tables:
            output += str(i) + '\n'
        return output


class Table:
    def __init__(self, table_name: str, data: list):
        self.__table_name = table_name
        self.__data = data

    @property
    def table_name(self):
        return self.__table_name

    def __str__(self):
        return f'{self.__table_name} : {self.__data}'


# modify the code in the Table class so that it supports the insert operation where an entry can be added to a list of dictionary


test_table = Table('person', persons)
test_table2 = Table('test', [{"1": 1, "2": 2, "3": 3}])
my_db = Database()
my_db.insert(test_table)
my_db.insert(test_table2)
print(my_db)
