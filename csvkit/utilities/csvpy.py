#!/usr/bin/env python

import agate

from csvkit.cli import CSVKitUtility


class CSVPy(CSVKitUtility):
    description = 'Load a CSV file into a CSV reader and then drop into a Python shell.'
    override_flags = ['l', 'zero', 'H']

    def add_arguments(self):
        self.argparser.add_argument('--dict', dest='as_dict', action='store_true',
                                    help='Use a CSV DictReader instead of a normal reader.')

    def main(self):
        # Attempt reading filename, will cause lazy loader to access file and raise error if it does not exist
        filename = self.input_file.name

        if self.args.as_dict:
            reader_class = agate.DictReader
        else:
            reader_class = agate.reader

        reader = reader_class(self.input_file, **self.reader_kwargs)

        welcome_message = 'Welcome! "%s" has been loaded in a %s object named "reader".' % (filename, reader_class.__name__)

        try:
            from IPython.frontend.terminal.embed import InteractiveShellEmbed
            ipy = InteractiveShellEmbed(banner1=welcome_message)
            ipy()
        except ImportError:
            import code
            code.interact(welcome_message, local={'reader': reader})


def launch_new_instance():
    utility = CSVPy()
    utility.main()

if __name__ == "__main__":
    launch_new_instance()
