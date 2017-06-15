from person import Person


class Staff(Person):

    def __init__(self, person_name, person_type, person_id):
        #call to the super class contructor

        super(Staff, self).__init__(person_name, person_type, person_id)
