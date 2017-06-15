from person import Person


class Fellow(Person):

    def __init__(self, person_name, person_type, person_id, want_accomodation):
        #call to super class contructor

        super(Fellow, self).__init__(person_name, person_type, person_id)
        self.__want_accomodation = want_accomodation

    def get_accomodation_option(self):
        #getter method thats returns want accomodation option

        return self.__want_accomodation