class DatabaseObjects:

    room_table = """ CREATE TABLE IF NOT EXISTS room(
                  id INTEGER PRIMARY KEY,
                  room_id INTEGER NOT NULL,
                  room_name VARCHAR,
                  room_type VARCHAR,
                  nccoupants INTEGER
                );"""

    person_table = """ CREATE TABLE IF NOT EXISTS person(
                  id INTEGER PRIMARY KEY,
                  peron_id INTEGER NOT NULL,
                  person_name MESSAGE_TEXT,
                  person_type MESSAGE_TEXT,
                  accomodation MESSAGE_TEXT
                );"""

    allocaation_table = """ CREATE TABLE IF NOT EXISTS allocation(
                  id INTEGER PRIMARY KEY,
                  room_id INTEGER,
                  person_id INTEGER
                );"""

    unallocated_table = """ CREATE TABLE IF NOT EXISTS unallocated(
                  id INTEGER PRIMARY KEY,
                  person_id INTEGER
                );"""