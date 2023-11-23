import database

class Operation:

    def __init__(self, uid, role, db: database.Database):
        self.uid = uid
        self.role = role
        self.db = db

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, r):
        if r in ['student', 'member', 'lead', 'faculty', 'advisor','admin']:
            self.__role = r
        else:
            ValueError('INVALID ROLE')

    def remove_element(self ,uid, table, index):
        if self.role != 'admin' or uid != self.uid:
            ValueError('No Permission')
        else:
            table.data.remove(index)
