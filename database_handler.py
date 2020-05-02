import sqlite3
from sqlite3 import Error
from json_inspector import *


@timer
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


@timer
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


@timer
def execute_read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        if result is not None:
            return [col[0] for col in cursor.description], result
        else:
            return [col[0] for col in cursor.description], []
    except Error as e:
        print(f"The error '{e}' occurred")


@timer
def generate_query(*groups):
    query_front = 'SELECT * FROM spells'


@timer
def query_spell_table(query):
    path = 'files/spells.sqlite'
    connection = create_connection(path)
    return execute_read_query(connection, query)


@timer
def startup_database_init():

    table_layout = [
        ('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'),
        ('name', 'TEXT NOT NULL', str),              # both
        # ('subtitle', 'TEXT NOT NULL'),          # display

        # ('time', 'TEXT NOT NULL'),              # display
        # ('range', 'TEXT NOT NULL'),             # display
        ('components', 'TEXT NOT NULL', str),        # both
        # ('duration', 'TEXT NOT NULL'),          # display
        ('classes', 'TEXT NOT NULL', str),           # both
        ('source', 'TEXT NOT NULL', str),            # both
        # ('description', 'TEXT NOT NULL'),       # display
        # ('description_higher', 'TEXT'),         # display

        ('ritual', 'INTEGER NOT NULL', int),         # query
        ('concentration', 'INTEGER NOT NULL', int),  # query
        ('level', 'INTEGER NOT NULL', int),          # query
        ('school', 'TEXT NOT NULL', str),            # query
    ]

    path = 'files/spells.sqlite'
    connection = create_connection(path)

    # delete old table
    delete_query = 'DROP TABLE spells'
    execute_query(connection, delete_query)

    # create new table
    lines = [f'\t{col[0]} {col[1]}' for col in table_layout]
    create_query = 'CREATE TABLE spells (\n' + ',\n'.join(lines) + ')'
    execute_query(connection, create_query)

    # insert spells into new table
    key_q_line = 'spells (' + ', '.join([col[0] for col in table_layout[1:]]) + ')'
    value_q_lines = []
    for spell in load_clean_json_spells():
        values = []
        for col in table_layout[1:]:
            col_key, col_type = col[0], col[1].split(' ')[0]
            val = spell[col_key]
            if col_type == 'TEXT':
                values.append(f'\"{val}\"')
            if col_type == 'INTEGER':
                values.append(str(val))
        value_q_lines.append('(' + ', '.join(values) + ')')

    value_q_line = ',\n'.join(value_q_lines)

    insert_query = f"""
        INSERT INTO    
            {key_q_line}
        VALUES
            {value_q_line}
        """
    execute_query(connection, insert_query)
