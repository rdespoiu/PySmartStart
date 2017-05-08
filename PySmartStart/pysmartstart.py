import requests
from .vehicle import Vehicle
from .api_paths import *

class API:
    # List of vehicles
    vehicles = list()

    # Pass username and password on instantiation
    def __init__(self, username, password, verbose = False):
        self.verbose = verbose
        self.AUTH_PATH = SERVER + SESS_ID_PATH + '{}/{}'.format(username, password)
        self.getSessionID()
        self.getVehicleData()

    # Builder for send command path
    sendCmdPath = lambda self, vehicle, command :   SERVER              + \
                                                    CMD_PATH            + \
                                                    vehicle.deviceid    + \
                                                    '/'                 + \
                                                    command.name        + \
                                                    '?sessid='          + \
                                                    self.SESSION_ID

    # Get a new session ID
    def getSessionID(self):
        self.SESSION_ID = requests.get(self.AUTH_PATH)  \
                                      .json()           \
                                      .get('Return')    \
                                      .get('Results')   \
                                      .get('SessionID')

        if self.verbose: print('\nSession ID: ' + self.SESSION_ID)

    # Populate list of vehicles with raw request data
    def getVehicleData(self):
        vehicles_RAW = requests.get(SERVER + VEHICLES_PATH + self.SESSION_ID) \
                               .json()                                        \
                               .get('Return')                                 \
                               .get('Results')                                \
                               .get('Devices')

        for v in vehicles_RAW:
            # Create a new Vehicle() object by retrieving DeviceId and Name from raw vehicle data
            new = Vehicle(v.get('DeviceId'), v.get('Name'))

            if self.verbose: print('\nAdded new vehicle: {}'.format(new))

            # Iterate through each available command for this vehicle
            for action in v.get('AvailActions'):
                # Ensure there is a valid action code (DO NOT USE '0', unknown effects)
                if action.get('ActionCode') != '0':
                    # Add a new Command() object to the Vehicle() object by retrieving
                    # Name and Description from each command in the raw vehicle data
                    new.addCommand(action.get('Name'), action.get('Description'))

                    if self.verbose: print('\tAdded new command to {}: {}'.format(new, new.commands[-1]))

            # Append the new Vehicle() object to the vehicles list
            self.vehicles.append(new)

    # Send command to vehicle
    def sendCommand(self, vehicle, command):
        response = requests.get(self.sendCmdPath(vehicle, command)).json()

        try:
            summary = response.get('Return').get('ResponseSummary')
            statusCode = summary.get('StatusCode')
            errorMessage = summary.get('ErrorMessage')

            ok = not statusCode and not errorMessage

            print('\n{}: {}'.format('OK' if ok else 'NOT OK', statusCode))

            if self.verbose:
                results = response.get('Return').get('Results').get('Device')

                print('\nCommand Summary')
                print('\tCommand Type: {}'.format(response.get('Return').get('Type')))
                print('\tStatus Code: {}'.format(statusCode))
                print('\tError Message: {}'.format(errorMessage))
                print('\nCommand Results')

                for result in results:
                    print('\t{}: {}'.format(result, results[result]))

            return ok

        except:
            print('Session timed out. Please get a new session ID via getSessionID()')
            return False
