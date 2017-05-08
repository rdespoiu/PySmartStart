from .command import Command

# Object to hold SmartStart vehicle data and commands associated with each vehicle
class Vehicle:
    commands = []

    def __init__(self, deviceid, name):
        self.deviceid = deviceid
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Vehicle(deviceid = {}, name = {})'.format(self.deviceid, self.name)

    def addCommand(self, name, description):
        self.commands.append(Command(name, description))
