class ArgumentError(Exception):
    def __init__(self, ErrorArgument):
        super().__init__(self)
        self.errorArgument = ErrorArgument

    def __str__(self):
        return 'Argument {} got an error value'.format(self.errorArgument)


