from random import randint
import sqlite3
from sqlite3 import Error
from beautifultable import BeautifulTable

from room import Room
from fellow import Fellow
from staff import Staff
from office import Office
from livingroom import LivingRoom
from databse_tables import DatabaseObjects


class Dojo:

    rooms = []  #all rooms in the Dojo
    people = []  #all people who joined the Dojo
    allocations = {}  #all room allocations
    unallocations = []  #all room unallocations

    def __init__(self):
        pass

    def create_person(self, args):

        person_id = self.generate_person_id()
        if args['<person_type>'].lower() == 'staff':
            staff_member = Staff(args['<person_name>'], args['<person_type>'], person_id)

            #add staff member to a general list of people
            self.people.append(staff_member)
            print('Staff ' + args['<person_name>'] + ' has been successfully added')

        elif args['<person_type>'].lower() == 'fellow':
            fellow_member = Fellow(
                args['<person_name>'],
                args['<person_type>'],
                person_id,
                args['<want_accomodation>'])

            #add fellow member to a general list of people
            self.people.append(fellow_member)
            print('Fellow ' + args['<person_name>'] + ' has been successfully added')

        else:
            print('Failed to add person, person_type should be either Staff|Fellow')
            return None

        self.allocate_room(
            args['<person_name>'],
            person_id,
            args['<person_type>'],
            args['<want_accomodation>'])

        return 1

    def generate_person_id(self):
        #increment the number of registered people by one to get the new person ID

        return len(self.people) + 1

    def create_room(self, args):

        if args['<room_type>'].lower() == 'office':
            for room in args['<room_name>']:
                room_id = self.generate_room_id()
                office_space = Office(args['<room_type>'], room, room_id)
                self.rooms.append(office_space)
                print('An office called ' + room + ' has been successfully created')
        elif args['<room_type>'].lower() == 'living':
            for room in args['<room_name>']:
                room_id = self.generate_room_id()
                living_space = LivingRoom(args['<room_type>'], room, room_id)
                self.rooms.append(living_space)
                print('A Living room called ' + room + ' has been successfully created')
        else:
            print('Failed to create room, room_type should either be Office|Living')
            return None

        return 1


    def generate_room_id(self):
        #increment the number of created rooms by one to get the new room ID

        return len(self.rooms) + 1

    def allocate_room(self, person_name, person_id, person_type, option):
        #allocate a person to a room

        if person_type.lower() == 'fellow':
            if option == 'Y' or option == 'y':
                #if the person is a fellow and wants accomodation space,
                #allocate office space

                office_room = self.get_random_office(self.generate_random_number())
                check = 0
                for id_ in self.allocations:
                    if id_ == office_room.get_room_id():
                        self.allocations[id_].append(person_id)
                        check = 1
                        break
                if check == 0:
                    self.allocations.update({office_room.get_room_id(): [person_id]})
                office_room.increase_no_of_occupants()
                print(person_name + ' has been allocated to office ' + office_room.get_room_name())

                #and then allocate accomodation space
                living_room = self.get_random_living_room(self.generate_random_number())
                check = 0
                for id_ in self.allocations:
                    if id_ == living_room.get_room_id():
                        self.allocations[id_].append(person_id)
                        check = 1
                        break
                if check == 0:
                    self.allocations.update({living_room.get_room_id(): [person_id]})
                living_room.increase_no_of_occupants()
                print(person_name + ' has been allocated to living room ' + living_room.get_room_name())

            else:
                #if person is a fellow and does not want accomodation space,
                #allocate office space only

                office_room = self.get_random_office(self.generate_random_number())
                check = 0
                for id_ in self.allocations:
                    if id_ == office_room.get_room_id():
                        self.allocations[id_].append(person_id)
                        check = 1
                        break
                if check == 0:
                    self.allocations.update({office_room.get_room_id(): [person_id]})
                office_room.increase_no_of_occupants()
                print(person_name + ' has been allocated to office ' + office_room.get_room_name())

        elif person_type.lower() == 'staff':
            #if person is staff, allocate office space only

            office_room = self.get_random_office(self.generate_random_number())
            check = 0
            for id_ in self.allocations:
                if id_ == office_room.get_room_id():
                    self.allocations[id_].append(person_id)
                    check = 1
                    break
            if check == 0:
                self.allocations.update({office_room.get_room_id(): [person_id]})
            office_room.increase_no_of_occupants()
            print(person_name + ' has been allocated to office ' + office_room.get_room_name())
        else:
            return None

        return 1

    def generate_random_number(self):
        #get a random number that is used as an index
        #to allocate a room randomly

        return randint(0, len(self.rooms) - 1)

    def get_random_office(self, index):
        #randomly select an office to be allocated

        room = self.rooms[index]
        if room.get_room_type().lower() == 'office' and room.get_no_of_occupants() < 6:
            return room
        return self.get_random_office(self.generate_random_number())

    def get_random_living_room(self, index):
        #randomly select a living room to be allocated
        room = self.rooms[index]
        if room.get_room_type().lower() == 'living' and room.get_no_of_occupants() < 4:
            return room
        return self.get_random_living_room(self.generate_random_number())

    def print_room(self, args):
        for room in self.rooms:
            if room.get_room_name().lower() == args['<room_name>'].lower():
                try:
                    room_allocation = self.allocations[room.get_room_id()]
                except KeyError as e:
                    print('\nRoom ' + room.get_room_name() + ' has not been allocated yet\n')
                    return None
                print('\n' + room.get_room_type().upper() + ' ROOM ' + args['<room_name>'].upper())
                table = BeautifulTable()
                table.column_headers = ['#', 'ID', 'NAME', 'TYPE']
                counter = 1
                for person_id in room_allocation:
                    for person in self.people:
                        if person.get_person_id() == person_id:
                            table.append_row([counter, person_id, person.get_person_name(), person.get_person_type()])
                    counter += 1
                table._column_alignments['NAME'] = BeautifulTable.ALIGN_LEFT
                table._column_alignments['TYPE'] = BeautifulTable.ALIGN_LEFT
                print(table)
                print()
                return 1
        return None

    def print_allocations(self, args):
        if len(self.allocations) > 0:
            for room_id in self.allocations:
                for room in self.rooms:
                    if room.get_room_id() == room_id:
                        room_allocation = self.allocations[room_id]
                        print('\n' + room.get_room_type().upper() + ' ROOM'.upper() + ' ' + room.get_room_name().upper())
                        table = BeautifulTable()
                        table.column_headers = ['#', 'ID', 'NAME', 'TYPE']
                        counter = 1
                        for person_id in room_allocation:
                            for person in self.people:
                                if person.get_person_id() == person_id:
                                    table.append_row([counter, person_id, person.get_person_name(), person.get_person_type()])
                            counter += 1
                        table._column_alignments['NAME'] = BeautifulTable.ALIGN_LEFT
                        table._column_alignments['TYPE'] = BeautifulTable.ALIGN_LEFT
                        print(table)
                        print()
                        break
            if args['--o'] is not None and args['--o'].endswith('.txt'):
                self.write_to_file(args['--o'], self.allocations)
            return 1
        return None

    def print_unallocarions(self):
        if len(self.unallocations) > 0:
            for room_id in self.unallocations:
                for room in self.rooms:
                    if room.get_room_id() == room_id:
                        room_allocation = self.unallocations[room_id]
                        print('\n' + room.get_room_type().upper() + ' ROOM'.upper() + ' ' + room.get_room_name().upper())
                        table = BeautifulTable()
                        table.column_headers = ['#', 'ID', 'NAME', 'TYPE']
                        counter = 1
                        for person_id in room_allocation:
                            for person in self.people:
                                if person.get_person_id() == person_id:
                                    table.append_row([counter, person_id, person.get_person_name(), person.get_person_type()])
                            counter += 1
                        table._column_alignments['NAME'] = BeautifulTable.ALIGN_LEFT
                        table._column_alignments['TYPE'] = BeautifulTable.ALIGN_LEFT
                        print(table)
                        print()
                        break
            return 1
        return None

    def write_to_file(self, file_name, data):
        if file_name.endswith('.txt'):
            target = open('db/' + file_name, 'a')
            if len(data) > 0:
                for room_id in data:
                    for room in self.rooms:
                        if room.get_room_id() == room_id:
                            room_allocation = self.allocations[room_id]
                            target.write(room.get_room_type().upper() + ' ROOM'.upper() + ' ' + room.get_room_name().upper() + '\n')
                            for person_id in room_allocation:
                                for person in self.people:
                                    if person.get_person_id() == person_id:
                                        target.write(person.get_person_name() + ', ')
                            target.write('\n\n')
                            break
            return 1
        else:
            print('Operations failed, file should be a text (.txt) file')
            return None

    def print_people(self):
        #  Print a list of all people registered with their unique identifiers

        table = BeautifulTable()
        table.column_headers = ['ID', 'NAME', 'TYPE']
        for person in self.people:
            table.append_row([person.get_person_id(), person.get_person_name(), person.get_person_type()])
        table._column_alignments['NAME'] = BeautifulTable.ALIGN_LEFT
        table._column_alignments['TYPE'] = BeautifulTable.ALIGN_LEFT
        print(table)

    def reallocate_person(self, args):
        new_room = self.get_new_room(args['<new_room>'])
        if new_room is not None:
            current_room = self.get_current_allocation(int(args['<person_identifier>']), new_room.get_room_type())
            current_room_members = self.allocations[current_room.get_room_id()]
            current_room_members.remove(int(args['<person_identifier>']))
            current_room.reduce_no_of_occupants()
            for room_id in self.allocations:
                if room_id == new_room.get_room_id():
                    self.allocations[room_id].append(int(args['<person_identifier>']))
                    new_room.increase_no_of_occupants()
                    print('Person re-allocated from '
                          + current_room.get_room_type() + ' '
                          + current_room.get_room_name()
                          + ' to ' + new_room.get_room_type() + ' '
                          + new_room.get_room_name())
                    break
        else:
            print('New room is full or it does not exist')

    def get_new_room(self, room_name):
        #get the room id from a list of added rooms for reallocation

        for room in self.rooms:
            if room.get_room_name().lower() == room_name.lower() and room.get_room_type().lower() == 'office':
                #check if new room is an office and its not full

                if room.get_no_of_occupants() < 6:
                    return room
            elif room.get_room_name().lower() == room_name.lower() and room.get_room_type().lower() == 'living':
                #check if new room is a living room and its not full

                if room.get_no_of_occupants() < 4:
                    return room
        return None

    def get_current_allocation(self, person_id, new_room_type):
        #new_room_type determines if person is moving from one office to another,
        #or from one living space to another

        for room_id, occupants in self.allocations.items():
            if person_id in occupants:
                for room in self.rooms:
                    if room.get_room_id() == room_id and room.get_room_type().lower() == new_room_type.lower():
                        return room
        return None

    def load_people(self):
        #  Load data from from a text file into the application

        #  Open the file for reading
        if len(self.rooms) > 0:
            args = {}
            with open('db/file.txt', 'r') as target:
                for line in target:
                    result = line.rstrip('\r\n').split()
                    person_name = result[0] + ' ' + result[1]
                    result.remove(result[0])
                    result.remove(result[0])
                    result.insert(0, person_name)
                    if len(result) < 3:
                        args.update(
                            {
                                '<person_name>': result[0],
                                '<person_type>': result[1],
                                '<want_accomodation>': None
                            })
                    else:
                        args.update(
                            {
                                '<person_name>': result[0],
                                '<person_type>': result[1],
                                '<want_accomodation>': result[2]
                            })
                    self.create_person(args)
                    args.clear()
            print('Data loaded successfully')
            return 1
        else:
            print('Data loading failed, there are no rooms created yet')
            return 0

    def create_connection(self, db_file):
        """
            create a database connection to SQLite database.
            if database does not exist, create a new database
            and return a database connection object
        """
        if db_file.endswith('.db'):
            try:
                conn = sqlite3.connect(db_file)
                return conn
            except Error as e:
                print(e)
        else:
            return None

    def create_databse_tables(self, conn, sql_statement):
        #  create table from sql_statement
        #  conn is a database connection object
        #  sql_statement is a CREATE TABLE statement

        try:
            cursor = conn.cursor()
            cursor.execute(sql_statement)
        except Error as e:
            print(e)

    def add_room_to_database(self, conn, room):
        sql = ''' INSERT INTO room(room_id, room_name, room_type, occupants)
                  VALUES(?, ?, ?, ?); '''
        data = (room.get_room_id(), room.get_room_name(), room.get_room_type(), room.get_no_of_occupants())
        cur = conn.cursor()
        try:
            cur.execute(sql, data)
            conn.commit()
        except Error as e:
            print(e)

    def add_person_to_database(self, conn, person):
        sql = ''' INSERT INTO person(person_id, person_name, person_type, accomodation)
                  VALUES(?, ?, ?, ?); '''
        if person.get_person_type().lower() == 'fellow':
            data = (person.get_person_id(),
                    person.get_person_name(),
                    person.get_person_type(),
                    person.get_accomodation_option())
        else:
            data = (person.get_person_id(),
                    person.get_person_name(),
                    person.get_person_type(),
                    None)
        cur = conn.cursor()
        try:
            cur.execute(sql, data)
            conn.commit()
        except Error as e:
            print(e)

    def add_allocation_to_database(self, conn, room_id, person_id):
        sql = ''' INSERT INTO allocation(room_id, person_id) VALUES(?, ?); '''
        data = (room_id, person_id)
        cur = conn.cursor()
        try:
            cur.execute(sql, data)
            conn.commit()
        except Error as e:
            print(e)

    def save_state(self, args):
        #  persists all the data stored in the app to a SQLite database

        conn = self.create_connection('db/' + args['<sqlite_database>'])
        if conn is not None:
            print('[+] Saving state...')
            #  Create room table
            self.create_databse_tables(conn, DatabaseObjects.room_table)

            #  Create person table
            self.create_databse_tables(conn, DatabaseObjects.person_table)

            #  Create allocation table
            self.create_databse_tables(conn, DatabaseObjects.allocaation_table)

            #  Create unallocation table
            self.create_databse_tables(conn, DatabaseObjects.unallocated_table)

            #  add rooms to the database
            print('[+] Saving rooms...')
            for room in self.rooms:
                self.add_room_to_database(conn, room)

            #  Add people to the database
            print('[+] Saving people...')
            for person in self.people:
                self.add_person_to_database(conn, person)

            #  Add allocations to the database
            print('[+] Saving allocations...')
            for room_id in self.allocations:
                for person_id in self.allocations[room_id]:
                    self.add_allocation_to_database(conn, room_id, person_id)
            print('[+] State saved successful')
        else:
            print("Could not save state, database name specified must end with (.db)")

    def load_rooms(self, conn):
        sql = '''
                SELECT
                    room_id,
                    room_name,
                    room_type,
                    occupants
                FROM room '''
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            room = Room(row[2], row[1], row[0])
            room.set_no_of_occupants(row[3])
            self.rooms.append(room)

    def load_persons(self, conn):
        sql = '''
                SELECT
                    person_id,
                    person_name,
                    person_type,
                    accomodation
                FROM person '''
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            if row[2].lower() == 'fellow':
                person = Fellow(row[1], row[2], row[0], row[3])
            else:
                person = Staff(row[1], row[2], row[0])
            self.people.append(person)

    def load_allocations(self, conn):
        sql = ''' SELECT DISTINCT room_id FROM allocation '''
        sql2 = ''' SELECT person_id FROM allocation WHERE room_id = ? '''
        cur = conn.cursor()
        cur2 = conn.cursor()
        cur.execute(sql)
        for row in cur.fetchall():
            cur2.execute(sql2, row)
            persons = cur2.fetchall()
            occupants = []
            for p in persons:
                occupants.append(p[0])
            self.allocations.update({row[0]: occupants})

    def load_state(self, args):
        #  Load data from the database into the application

        conn = self.create_connection('db/' + args['<sqlite_database>'])
        if conn is not None:
            #  Load rooms into the application
            print('[+] Loading rooms...')
            self.load_rooms(conn)

            #  Load people into the application
            print('[+] Loading people...')
            self.load_persons(conn)

            #  load allocations into the application
            print('[+] Loading allocations...')
            self.load_allocations(conn)

            print('[+] State loaded successfully')
        else:
            print('Failed to load state, database file provided must end with (.db)')

