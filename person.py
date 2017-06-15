class Person:

    def __init__(self, person_name, person_type, person_id):
        #constructor used to initialize the variables

        self.__person_name = person_name
        self.__person_type = person_type
        self.__person_id = person_id

    def get_person_name(self):
        #getter method that returns a person's name from the person object

        return self.__person_name

    def get_person_type(self):
        #getter method that returns a person type from the person object

        return self.__person_type

    def get_person_id(self):
        #getter method that returns a person ID from the person object

        return self.__person_id