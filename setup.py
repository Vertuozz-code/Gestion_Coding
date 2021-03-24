# usr/env/bin Python3.8
# coding:utf-8

"""
This import is obligatory for the good of the system
Files imports, they are important to help the script a have all tools
for a good use
"""

# Import file
from install_dhcp import connect_ssh
from reset_computer import connect_ssh_reset


def choice_setup():
    """ This method allows the user to choose the script they wxant to use """

    choice = input('Bonjour, quel configuration voulez-vous utiliser ? \n'
                   '1 = Install DHCP (mode serveur) / '
                   '2 = Reset computeur client ')

    if int(choice) == 1:
        return connect_ssh()
    if int(choice) == 2:
        return connect_ssh_reset()


choice_setup()
