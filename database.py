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
            self.key = list(data.keys())
            self.__data = [data]
        elif isinstance(data, list):
            self.__data = data
            self.key = list(data[0].keys())

    @property
    def table_name(self):
        return self.__table_name

    @table_name.setter
    def table_name(self, new_name):
        org_name = self.table_name.removesuffix('filtered')
        # Prevent from change original table name(Only filtered that can be change)
        if org_name != self.table_name:
            self.__table_name = org_name + new_name

    @property
    def data(self):
        return self.__data

    def __validate_new_data(self, x):
        if [i for i in x.keys()] == self.key:
            return True
        else:
            return False

    def insert(self, x):
        if self.__validate_new_data(x):
            if all(i == '' for i in self.__data[0].values()):
                self.data.clear()
            self.data.append(x)
            return True
        else:
            return False

    def search(self, key, search_query):
        for i in self.__data:
            if i[key] == search_query:
                return i
        return None

    def write_to_csv(self):
        with open(self.table_name + '.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.key)
            for i in self.__data:
                writer.writerow(i.values())

    def select(self, key):
        return [i[key] for i in self.data]

    def filter(self, condition):
        data = []
        for item1 in self.data:
            if condition(item1):
                data.append(item1)
        if not data:
            data = [{i: '' for i in self.__data[0].keys()}]
        return Table(self.table_name + '_filtered', data)

    def remove_data(self, x):
        return self.__data.pop(x)

    def __str__(self):
        return f'{self.__table_name} : {self.__data}'

    def to_table(self):
        # Get Longest Element of each rows
        spaces_key = {}
        for j in self.key:
            ls = self.select(j)
            ls = [len(k) + 15 for k in ls]
            spaces_key[j] = max(ls)

        # Key
        key_temp = '     |'
        for i in self.key:
            key_temp += f" {i: ^{spaces_key[i]}} |"
        table_name = 'Table Name : ' + self.table_name
        o_put = f"{table_name : ^{(3* len(spaces_key)) + sum([i for i in spaces_key.values()])}}\n"
        o_put += key_temp + '\n'
        # Divider
        o_put += '-----|'
        for i in spaces_key.values():
            o_put += "-" * (i + 2) + "|"
        o_put += '\n'

        # Element
        for i in range(len(self.__data)):
            temp = f'{i+1: ^4} |'
            for j in self.key:
                temp += f" {self.__data[i][j]: ^{spaces_key[j]}} |"
            o_put += temp + '\n'

        # Divider
        o_put += '-----|'
        for i in spaces_key.values():
            o_put += "-" * (i + 2) + "|"
        return o_put


# # Test code
# test_table = Table('person', read_csv('persons.csv'))
# test_table2 = Table('test', [{"1": 1, "2": 2, "3": 3}])
# my_db = Database()
# my_db.insert(test_table)
# my_db.insert(test_table2)
# test_insert = [{"1" : 'L', "2": 'O', "3": "K"}, {1: 1, 2: 2, 3: 3}]
# test_insert2 = {"O": 1, "K":2}
# my_db.search('test').insert(test_insert)
# my_db.search('test').insert(test_insert2)
# print(my_db)
# ps = my_db.search('person')
# print(ps.to_table())
# test_table2.write_to_csv()


# modify the code in the Table class so that it supports the update operation where an entry's value associated with a key can be updated
