# usr/env/bin Python3.8
# coding:utf-8

"""
This import is obligatory for the good of the system
Lib imports, they are important to help the script a have all tools
for a good use
"""

# Import lib
import getpass
from fabric.api import *


def connect_ssh_reset():
    """ This method is used to connect to ssh server """

    # Variables for connection
    print("Bonjour, nous allons réinitialiser votre poste")
    print("Veuillez indiquer vos identifiants de connexion ssh")

    ip_addresse = input("Addresse IP : ")
    user = input("Utilisateur : ")
    password = getpass.getpass("Mot de passe : ")

    # Connection ssh
    env.host_string = ip_addresse
    env.user = user
    env.password = password
    return check_user_and_delete()


def check_user_and_delete():
    """ This method is used to allow of the deleted users """

    # Create the lists for delete users
    list_users = []
    list_del_users = []
    i = 0
    admin = 'user'
    users_check = run('ls /home')
    users = users_check.split()

    print('Vérifications des utilisateurs existants')
    # Check the users current
    for users_check in users:
        list_del_users.append(users_check)
    # Isolate administrator
    if admin in list_del_users:
        list_del_users.remove(admin)
        print('Fin des vérifications')
        print('Réinitialisation des utilisateurs en cours')
        # Delete the users current
        while i < len(list_del_users):
            run('sudo passwd --delete ' + list_del_users[i])
            run('sudo userdel -r -f ' + list_del_users[i])
            i += 1
        print('Les utilisateurs ont été réinitialisés !')
        return change_hostname()


def change_hostname():
    """ This method is used to change Hostname """

    print('L\'Hostname va être modifié')
    NewHostname = 'PC'
    # Get hostname current
    Hostname = run('sudo cat /etc/hostname')
    # Switch the hostname
    run('sudo sed -i "s/' + Hostname + '/' + NewHostname + '/g" /etc/hostname')
    run('sudo sed -i "s/' + Hostname + '/' + NewHostname + '/g" /etc/hosts')
    print('Hostname modifié')
    return dconf()


def dconf():
    """ This method is used to reset the desktop """
    print('Réinitialisation du bureau Linux')
    run('dconf reset -f /')
    return done_conf()


def done_conf():
    """ This method is used to notify the user of a restart """
    print('Réinitialisation terminée !')
    print('Votre machine va redémarrer')
    run('sudo reboot')
