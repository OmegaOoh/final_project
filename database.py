# try wrapping the code below that reads a persons.csv file in a class and make it more general such that it can read in any csv file

import csv, os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def read_csv(file_name: str):
    ls = []
    with open(os.path.join(__location__, file_name)) as f:
        rows = csv.DictReader(f)
        for r in rows:
            ls.append(dict(r))
        return ls


persons = read_csv('persons.csv')

# Class implementation
class Database:
    def __init__(self):
        self.__tables = []

    def insert(self, table: "Table Class"):
        self.__tables.append(table)

    def search(self, table_name: str):
        for i in self.__tables:
            if i.table_name == table_name:
                return i
        return None

    def __str__(self):
        output = ''
        for i in self.__tables:
            output += str(i) + '\n'
        return output


class Table:
    def __init__(self, table_name: str, data: list = []):
        self.__table_name = table_name
        self.__data = data

    @property
    def table_name(self):
        return self.__table_name

    @property
    def data(self):
        return self.__data

    def insert_data(self, new_data):
        if isinstance(new_data, list):
            for i in new_data:
                self.__data.append(i)
        else:
            self.__data.append(new_data)

    def search(self, key, search_query):
        for i in self.__data:
            if i[key] == search_query:
                return i
        return None

    def __str__(self):
        return f'{self.__table_name} : {self.__data}'


# # Test code
# test_table = Table('person', persons)
# test_table2 = Table('test', [{"1": 1, "2": 2, "3": 3}])
# my_db = Database()
# my_db.insert(test_table)
# my_db.insert(test_table2)
# print(my_db)

