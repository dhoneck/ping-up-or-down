"""This module allows you to check if a list of network hosts are up or down."""

import os
import time
from subprocess import Popen, PIPE
from datetime import datetime


class UpOrDownPinger:
    def __init__(self):
        """Creates a list of network hosts.

        Can add hosts by:
            - Name (e.g. dell-xps.local)
            - IP address (e.g. 192.168.1.1)
            - IP range (e.g. 192.168.1.1/255)
        """
        os.system('cls')
        self.host_list = []
        self.ping_statuses = []
        host = input('What is a network host you want to ping?\
            \n(e.g. dell-xps.local, 192.168.1.1, or 192.168.1.1/255)\n')
        self.process_host_input(host)
        while True:
            add_another = input('\nAdd another? (y/n) ')
            if add_another.lower() == 'n' or add_another.lower() == 'no':
                break
            elif add_another.lower() == 'y' or add_another.lower() == 'yes':
                host = input('What is a network host you want to ping? ')
                self.process_host_input(host)
            else:
                print('That is an invalid input. Try again.')
        os.system('cls')

    def process_host_input(self, host_input):
        """Adds hosts to a list and will call the method to expand IP ranges if needed"""
        if '/' in host_input:
            self.host_list += self.add_ip_range(host_input)
        else:
            self.host_list.append(host_input)

    def add_ip_range(self, raw_ip_range):
        """Expands IP range that falls in format of 192.168.1.0/255"""
        octets = raw_ip_range.split('.')
        for oct_idx, octet in enumerate(octets):
            ip_range = octet.split('/')
            if '/' in octet:
                octets[oct_idx] = (int(ip_range[0]), int(ip_range[1]))
            elif '/' not in octet:
                octets[oct_idx] = (int(ip_range[0]), int(ip_range[0]))
        expanded_ip_list = []
        for a in range(octets[0][0],octets[0][1] + 1):
            for b in range(octets[1][0],octets[1][1] + 1):
                for c in range(octets[2][0],octets[2][1] + 1):
                    for d in range(octets[3][0],octets[3][1] + 1):
                        expanded_ip_list.append(str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d))
            return expanded_ip_list

    def start_pinging(self):
        """Checks list of network hosts to see if they are up or down."""
        
        # Give the user an update of how many items that will be pinged
        if len(self.host_list) == 1:
            print('Pinging 1 item, please wait...')
        elif len(self.host_list) > 1:
            print('Pinging %d items, please wait...' % len(self.host_list))
        
        # Start pinging
        while True:
            # Reset ping_statuses list
            self.ping_statuses = []

            # Ping all hosts
            for host in self.host_list:
                # Get output of ping command
                output = str(Popen('ping -n 1 -w 250 {}'.format(host), stdout=PIPE).communicate()[0])

                if 'unreachable' in output:
                    result = FONT['RED'] + 'Offline - unreachable' + FONT['END']
                elif 'could not find' in output:
                    result = FONT['RED'] + 'Offline - could not find' + FONT['END']
                elif 'transmit failed' in output:
                    result = FONT['RED'] + 'Offline - transmit failed' + FONT['END']
                elif 'timed out' in output:
                    result = FONT['RED'] + 'Offline - timed out' + FONT['END']
                else:
                    result = FONT['GREEN'] + 'Online' + FONT['END']
                self.ping_statuses.append((host, result))

            # Clear screen before printing new statuses
            os.system('cls')

            # Print header
            print(FONT['BOLD'] + FONT['UNDERLINE'] + '{:25}'.format('Network Hosts') + '{:25}'.format('Status') + FONT['END'])

            # Print statuses
            for status in self.ping_statuses:
                print('{:25}'.format(status[0]) + status[1])

            # Print timestamp footer
            print('\nLast Updated: ' + datetime.now().strftime('%a %b %d, %Y %X'))


            time.sleep(3)


# Used for modifying terminal font color and style.
FONT = {
    'GREEN': '\033[92m',
    'RED': '\033[91m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
    'END': '\033[0m',
}


if __name__ == '__main__':
    """Calls the methods to create and ping a list of network hosts."""
    h_list = UpOrDownPinger()
    h_list.start_pinging()