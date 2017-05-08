# Object to hold SmartStart command data
class Command:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return self.description

    def __repr__(self):
        return 'Command(name = {}, description = {})'.format(self.name, self.description)
