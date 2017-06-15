class Room:

    def __init__(self, room_type, room_name, room_id):
        #constructor that initializes the variables

        self.__room_name = room_name
        self.__room_type = room_type
        self.__no_of_occupants = 0
        self.__room_id = room_id

    def get_room_name(self):
        #getter method that returns the room name

        return self.__room_name

    def get_room_type(self):
        #getter method that returns the room type

        return self.__room_type

    def get_no_of_occupants(self):
        #getter method that returns the number of occupants in a room

        return self.__no_of_occupants

    def get_room_id(self):
        #getter method that returns the room ID

        return self.__room_id

    def increase_no_of_occupants(self):
        #setter method that increases the number of occupants in a room by 1

        self.__no_of_occupants += 1

    def reduce_no_of_occupants(self):
        #setter method that reduces the number of occupants in a room by 1

        self.__no_of_occupants -= 1

    def set_no_of_occupants(self, number):
        self.__no_of_occupants = number