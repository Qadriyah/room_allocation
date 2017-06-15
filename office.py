from room import Room


class Office(Room):

    def __init__(self, room_type, room_name, room_id):
        #call to super class constructor

        super(Office, self).__init__(room_type, room_name, room_id)

        #set room capacity for an office to 6
        self.__room_capacity = 6

    def get_room_capacity(self):
        #getter method that returns the capacity of the room

        return self.__room_capacity