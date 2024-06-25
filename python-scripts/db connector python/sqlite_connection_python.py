import sqlite3
import datetime

'''
input_data_test = [
    ('Werkzeug', 'Bosch300', 'Heerbrugg', 6, datetime.date(2023, 7, 18), True, 'idprefix1_', 'Microshield', 'laboratory', 'A4228', 'Bosch', 'n/a', 'n/a', 'n/a', False, 'Hello this are some notes', 'This is a calibration description: \n First do this \n Second do this \n Third do this \n Fourth do this \n Fifth do this', 'Event Log PLACEHOLDER', 'Documents PLACEHOLDER'),
    ('Maschine', 'Bosch400', 'Widnau', 6, datetime.date(2024, 1, 22), True, 'idprefix2_', 'Microshield', 'workshop', 'A5888', 'Bosch', 'n/a', 'n/a', 'n/a', False, 'Hello this are some notes 2.0', 'This is a calibration description 2.0: \n First do this \n Second do this \n Third do this \n Fourth do this \n Fifth do this', 'Event Log PLACEHOLDER 2', 'Documents PLACEHOLDER 2')
]
'''

input_data_test_2 = [
    ('Werkzeug', 'Bosch300', 'Heerbrugg', 6, datetime.date(2023, 7, 18), True, 'idprefix1_'),
    ('Maschine', 'Bosch400', 'Widnau', 6, datetime.date(2024, 1, 25), True, 'idprefix2_')
]

connection = sqlite3.connect('db/test_equipment_database.db')
cursor = connection.cursor()

'''
    id                          INTEGER PRIMARY KEY AUTOINCREMENT, 
    type                        TEXT, 
    label                       TEXT, 
    location                    TEXT, 
    maintenance_period          INTEGER,  
    next_maintanance            DATETIME, 
    valid                       BOLEAN, 
    id_prefix                   TEXT, 
    owner                       TEXT, 
    departement                 TEXT, 
    pn                          TEXT, 
    manufacturer                TEXT, 
    span                        TEXT, 
    accuracy                    TEXT, 
    resolution                  TEXT, 
    disabled                    BOLEAN, 
    notes                       TEXT, 
    calibration_description     TEXT, 
    event_log                   TEXT, 
    documents                   TEXT
'''
#cursor.execute('CREATE TABLE IF NOT EXISTS test_equipment (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, label TEXT, location TEXT, maintenance_period INTEGER, next_maintanance DATETIME, valid BOLEAN, id_prefix TEXT, owner TEXT, departement TEXT, pn TEXT, manufacturer TEXT, span TEXT,, accuracy TEXT, resolution TEXT, disabled BOLEAN, notes TEXT, calibration_description TEXT, event_log TEXT, documents TEXT)')
#cursor.executemany('INSERT INTO test_equipment (type, label, location, maintenance_period, next_maintanance, valid, id_prefix, owner, departement, pn, manufacturer, span, accuracy, resolution, disabled, notes, calibration_description, event_log, documents) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', input_data_test)
cursor.execute('CREATE TABLE IF NOT EXISTS test_equipment (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, label TEXT, location TEXT, maintenance_period INTEGER, next_maintanance DATETIME, valid BOLEAN, id_prefix TEXT)')
cursor.executemany('INSERT INTO test_equipment (type, label, location, maintenance_period, next_maintanance, valid, id_prefix) VALUES (?,?,?,?,?,?,?)', input_data_test_2)

#print all rows in test_equipment table
for row in cursor.execute('SELECT * FROM test_equipment'):
    print('Row: ', row)


#filter (with * you will search all tables in the db)
cursor.execute('SELECT * FROM test_equipment WHERE type=:type', {'type': 'Werkzeug'})
test_equipment_search = cursor.fetchall()
print('Search: ', test_equipment_search)

#replace werkzeug with fisch
# for i in test_equipment_search:
#     ['Fisch' if value == 'Werkzeug' else value for value in i]

#print all rows in test_equipment table
# for row in cursor.execute('SELECT * FROM test_equipment'):
#     print('Row: ', row)

# delete
# cursor.execute('DELETE FROM test_equipment WHERE id = 1')

# for row in cursor.execute('SELECT * FROM test_equipment'):
#     print('After delete, Row: ', row)

# cursor.execute('DROP TABLE test_equipment')


# cursor.execute('CREATE TABLE IF NOT EXISTS te_types (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT')
# cursor.executemany('INSERT INTO te_types (type) VALUES (?)', ['Werkzeug', 'Maschine'])

# cursor.execute('CREATE TABLE IF NOT EXISTS te_owners (id INTEGER PRIMARY KEY AUTOINCREMENT, owner TEXT')
# cursor.executemany('INSERT INTO te_owners (owner) VALUES (?)', ['Michael', 'Roger'])

connection.commit() # ?
connection.close()