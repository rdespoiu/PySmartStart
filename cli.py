import sys
import argparse
from PySmartStart.pysmartstart import API

def getOptions():
    parser = argparse.ArgumentParser('PySmartStart API', add_help = True)
    parser.add_argument('-u', '- Username/Email')
    parser.add_argument('-p', '- Password')

    return parser.parse_args()

def PYSMSTCLI(username = None, password = None):
    print('PySmartStart CLI\n')

    verbose = input('Verbose mode? [y/n]\n') == 'y'

    username = username if username else input('Please enter your username: ')
    password = password if password else input('Please enter your password: ')

    api = API(username, password, verbose)

    while True:
        if input('\nConnection: OK\nPress enter to continue, or \'q\' to exit\n') == 'q': exit(0)
        print('\nSelect desired vehicle number from the list:')
        for i in range(len(api.vehicles)):
            print('[{}] - {}'.format(i, api.vehicles[i]))

        vehicle = api.vehicles[int(input())]

        while True:
            print('\nSelect desired command number from the list:')
            for i in range(len(vehicle.commands)):
                print('[{}] - {}'.format(i, vehicle.commands[i]))

            command = vehicle.commands[int(input())]

            input('\nPress any key to send the command\n')
            print('\nSENDING...')

            api.sendCommand(vehicle, command)

            if input('Press enter to select another command, or \'q\' to go back\n') == 'q': break



if __name__ == '__main__':
    options = getOptions()
    PYSMSTCLI(options.u, options.p)
