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

    def table_name(self):
        return [i.table_name for i in self.__tables]

    def __str__(self):
        output = ''
        for i in self.__tables:
            output += str(i) + '\n'
        return output


class Table:
    def __init__(self, table_name: str, data: list or dict):
        self.__table_name = table_name
        if isinstance(data, dict):
            self.key = [i for i in data.keys()]
            self.__data = [data]
        elif isinstance(data, list):
            self.__data = data
            self.key = self.__data[0].keys()

    @property
    def table_name(self):
        return self.__table_name

    @property
    def data(self):
        return self.__data

    def insert(self, new_data):
        if isinstance(new_data, list):
            if self.__validate_new_data(new_data[0]):
                for i in new_data:
                    if list(self.__data[0].values()) == ['' for i in self.__data[0].keys()]:
                        self.__data = []
                    if self.__validate_new_data(i):
                        self.__data.append(i)
        else:
            if self.__validate_new_data(new_data):
                if list(self.__data[0].values()) == ['' for i in self.__data[0].keys()]:
                    self.__data = []
                self.__data.append(new_data)

    def __validate_new_data(self, x):
        if x.keys() == self.key:
            return True
        else:
            return False

    def search(self, key, search_query):
        for i in self.__data:
            if i[key] == search_query:
                return i
        return None

    def write_to_csv(self):
        with open(self.table_name + '.csv', 'w', encoding='UTF8',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.key)
            for i in self.__data:
                writer.writerow(i.values())

    def remove(self, x):
        return self.__data.pop(x)

    def __str__(self):
        return f'{self.__table_name} : {self.__data}'


# # Test code
# test_table = Table('person', persons)
# test_table2 = Table('test', [{"1": 1, "2": 2, "3": 3}])
# my_db = Database()
# my_db.insert(test_table)
# my_db.insert(test_table2)
# test_insert = [{"1" : 'L', "2": 'O', "3": "K"}, {1: 1, 2: 2, 3: 3}]
# test_insert2 = {"O": 1, "K":2}
# my_db.search('test').insert(test_insert)
# my_db.search('test').insert(test_insert2)
# print(my_db)
# test_table2.write_to_csv()


# modify the code in the Table class so that it supports the update operation where an entry's value associated with a key can be updated
