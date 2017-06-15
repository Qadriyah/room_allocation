"""
    Usage:
        TheDojo create_room <Office | Living> <name>...
        TheDojo create_person <name> <Fellow | Staff> [want_accomodation]
        TheDojo print_room <room_name>
        TheDojo print_allocations [--file=<filename>]
        TheDojo reallocate_person <person_identifier> <new_room>
        TheDojo print_unallocated [-o=<filename>]
        TheDojo print_people
        TheDojo print_all_rooms
        TheDojo load_people
        TheDojo (-i | --interactive)
        TheDojo (-h | --help | --version)
        TheDojo quit Exit application
    Options:
        -i, --interactive  Interactive Mode
        -h, --help  Show this screen and exit.
"""

import sys
import cmd
from docopt import docopt
from docopt import DocoptExit
from dojo import Dojo


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive (cmd.Cmd):
    intro = "\n\n\t::::::::::::::::: WELCOME TO THEDOJO APP :::::::::::::::::::\n\n"
    prompt = '(TheDojo) '
    file = None
    __dojo = Dojo()

    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room <room_type> <room_name>..."""

        self.__dojo.create_room(args)

    @docopt_cmd
    def do_create_person(self, args):
        """Usage: create_person <person_name> <person_type> [<want_accomodation>]"""

        self.__dojo.create_person(args)

    @docopt_cmd
    def do_print_room(self, args):
        """Usage: print_room <room_name>"""

        self.__dojo.print_room(args)

    @docopt_cmd
    def do_print_allocations(self, args):
        """Usage: print_allocations [--o=<filename>]"""

        self.__dojo.print_allocations(args)

    @docopt_cmd
    def do_print_people(self, args):
        """Usage: print_people"""

        self.__dojo.print_people()

    @docopt_cmd
    def do_reallocate_person(self, args):
        """Usage: reallocate_person <person_identifier> <new_room>"""

        self.__dojo.reallocate_person(args)

    @docopt_cmd
    def do_load_people(self, args):
        """Usage: load_people"""

        self.__dojo.load_people()

    @docopt_cmd
    def do_save_state(self, args):
        """Usage: save_state <sqlite_database>"""

        self.__dojo.save_state(args)

    @docopt_cmd
    def do_load_state(self, args):
        """Usage: load_state <sqlite_database>"""

        self.__dojo.load_state(args)

    def do_quit(self, args):
        """Quits out of Interactive Mode."""

        print('\n\n\tGood Bye\n\n')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)