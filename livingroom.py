from room import Room


class LivingRoom(Room):

    def __init__(self, room_type, room_name, room_id):
        #call to super class constructor

        super(LivingRoom, self).__init__(room_type, room_name, room_id)

        #set the room capacity for a living room to 4
        self.__room_capacity = 4

    def get_room_capacity(self):
        #getter methods that returns the maximum capacity of the room

        return self.__room_capacity