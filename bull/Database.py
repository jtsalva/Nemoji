import os
import sqlite3

DIRECTORY_LOCATION = './databases'


if not os.path.exists(DIRECTORY_LOCATION):
    os.mkdir(DIRECTORY_LOCATION)


def _auto_connect(query_fn):
    def auto_connect_query_fn(self, *args, **kwargs):
        self._connect()
        response = query_fn(self, *args, **kwargs)
        self._close()
        return response
    return auto_connect_query_fn


class Database:
    directory_location = DIRECTORY_LOCATION
    file_extension = 'sqlite'

    @classmethod
    def drop_database(cls, name: str) -> None:
        database_location = '{path}/{name}.{extension}'.\
            format(path=cls.directory_location,
                   name=name,
                   extension=cls.file_extension)
        if os.path.exists(database_location):
            os.remove(database_location)

    def __init__(self, name: str, extension=None):
        self.name = name
        self.location = '{path}/{name}.{extension}'.\
            format(path=self.__class__.directory_location,
                   name=name,
                   extension=extension or self.__class__.file_extension)
        self.conn = None
        self.cur = None

        if not os.path.isfile(self.location):
            try:
                conn = sqlite3.connect(self.location)
                conn.close()
            except Exception as e:
                print(e)

    def _connect(self):
        self.conn = sqlite3.connect(self.location)
        self.cur = self.conn.cursor()

    def _close(self):
        self.conn.commit()
        self.conn.close()
        self.conn = None
        self.cur = None

    @_auto_connect
    def execute(self, query: str, params: list=None) -> list or None:
        try:
            response = self.cur.execute(query) if params is None\
                else self.cur.execute(query, params)
        except Exception as e:
            print(query, os.path.basename(__file__), ':', e)
            return

        return response.fetchall()

    def select(self, table_name: str, field_names: list or str, condition: str=None, order: str=None) -> list:
        select_query = 'SELECT {field_names} FROM {table_name} {where} {order};'.\
            format(field_names=', '.join(field_names) if isinstance(field_names, list) else field_names,
                   table_name=table_name,
                   where='WHERE {condition}'.format(condition=condition) if condition else '',
                   order='ORDER BY {order}'.format(order=order) if order else '')

        return self.execute(select_query)

    def create_table(self, table_name: str, fields: dict or list) -> list:
        create_table_query = 'CREATE TABLE {name}({fields});'.\
            format(name=table_name,
                   fields=', '.join(str(field) for field in fields))

        # print(create_table_query)
        # exit()

        return self.execute(create_table_query)

    def update(self, table_name: str, values: dict, condition: str=None) -> list:
        update_query = 'UPDATE {table_name} SET {values} {where};'.\
            format(table_name=table_name,
                   values=', '.join([' = '.join([field_name, '?']) for field_name in values]),
                   where='WHERE {condition}'.format(condition=condition) if condition else '')

        return self.execute(update_query, list(values.values()))

    def insert(self, table_name: str, values: dict) -> list:
        insert_query = 'INSERT INTO {table_name}({field_names}) VALUES({values});'.\
            format(table_name=table_name,
                   field_names=', '.join(values.keys()),
                   values=', '.join(['?' for _ in range(len(values))]))

        return self.execute(insert_query, list(values.values()))

    # not tried to use yet
    def delete(self, table_name: str, values: list, condition: str) -> list:
        delete_query = 'DELETE {values} FROM {table_name} WHERE {condition};'.\
            format(values=', '.join(values),
                   table_name=table_name,
                   condition=condition)

        return self.execute(delete_query)

    def list_tables(self):
        response = self.select(table_name='sqlite_master',
                               field_names='name',
                               condition='type="table"')
        tables = {}
        for name in response:
            table_info = self.execute('PRAGMA table_info({name});'.format(name=name[0]))
            tables[name[0]] = []
            for x in table_info:
                tables[name[0]].append(x)

        return tables

    def __repr__(self):
        return '{class_name} {db_name}'.format(class_name=self.__class__.__name__, db_name=self.name)


def connect(db_name, extension=None):
    return Database(db_name, extension)
