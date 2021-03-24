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


def connect_ssh():
    """ This method is used to connect to ssh server """

    # Variables for connection
    print("Bonjour, nous allons configurer votre serveur DHCP")
    print("Veuillez indiquer vos identifiants de connexion ssh")

    ip_addresse = input("Addresse IP : ")
    user = input("Utilisateur : ")
    password = getpass.getpass("Mot de passe : ")

    # Connection ssh
    env.host_string = ip_addresse
    env.user = user
    env.password = password
    return install_dhcp()


def install_dhcp():
    """ This method is used to install the DHCP server """

    # Install DHCP
    print('Installation du serveur DHCP ...')
    run('sudo apt-get update')
    run('sudo apt-get install -y isc-dhcp-server')
    print('Installation terminée !')
    return configure_dhcp()


def configure_dhcp():
    """ This method is used to configure the DHCP server """

    i = 0
    # Check if user have need the vlans
    Vlans = input('Voulez-vous utiliser des vlans (répondre par yes ou no) ? ')
    if Vlans == 'yes':
        return configure_dhcp_with_vlans()
    if Vlans == 'no':
        newtork_numbers = input('De combien de '
                                'sous-réseaux aves-vous besoin ? ')

        while i < int(newtork_numbers):
            # Get informations for subnets
            ip_network = input('Indiquez l\'addresse '
                               'IP du sous réseau (ex: 192.168.1.0) ')
            netmask = input('Indiquez le masque du réseau'
                            ' (ex: 255.255.255.0) ')
            range_ip_1 = input('Indiquez le range d\'addresses IP (départ) ')
            range_ip_2 = input('Indiquez le range d\'addresses IP (fin) ')
            option_domain_name_servers = input('Indiquez le DNS ')
            option_domain_name = input('Indiquez le nom de domaine ')
            option_routers = input('Indiquez la passerelle à utiliser ')
            option_broadcast_address = input('Indiquez l\'IP broadcast ')
            default_lease_time = input(
                'Indiquez la durée d\'attribution et de reservation'
                ' d\'une IP en seconde par défault (ex: 600) ')
            max_lease_time = input(
                'Indiquez la durée d\'attribution et de'
                ' reservation maximal d\'une IP en seconde (ex: 7200) ')

            run(
                'sudo bash -c \'echo "subnet '
                + ip_network + ' netmask ' + netmask +
                ' {"' + '>> /etc/dhcp/dhcpd.conf\'')
            run('sudo bash -c \'echo " range '
                + range_ip_1 + ' ' + range_ip_2 + ';"'
                + '>> /etc/dhcp/dhcpd.conf\'')
            run(
                'sudo bash -c \'echo " option domain-name-servers '
                + option_domain_name_servers + ';"'
                + '>> /etc/dhcp/dhcpd.conf\'')
            run(
                'sudo bash -c \'echo " option domain-name \"'
                + option_domain_name + '\";"' + '>> /etc/dhcp/dhcpd.conf\'')
            run(
                "sudo sed -i 's/option domain-name "
                + option_domain_name + ";/option domain-name \""
                + option_domain_name + "\";/g' /etc/dhcp/dhcpd.conf")
            run('sudo bash -c \'echo " option routers '
                + option_routers + ';"' + '>> /etc/dhcp/dhcpd.conf\'')
            run(
                'sudo bash -c \'echo " option broadcast-address '
                + option_broadcast_address +
                ';"' + '>> /etc/dhcp/dhcpd.conf\'')
            run('sudo bash -c \'echo " default-lease-time '
                + default_lease_time + ';"' + '>> /etc/dhcp/dhcpd.conf\'')
            run('sudo bash -c \'echo " max-lease-time '
                + max_lease_time + ';"' + '>> /etc/dhcp/dhcpd.conf\'')
            run('sudo bash -c \'echo "}" >> /etc/dhcp/dhcpd.conf\'')
            i += 1
        return configure_network_card_no_vlans()


def configure_network_card_no_vlans():
    """ This method is used to configure the network card """

    i = 0
    # Create a list for get the cards name and for use
    list_cards = []

    # Config isc-dhcp-server
    run('sudo bash -c \'echo "INTERFACESv4=" > /etc/default/isc-dhcp-server\'')

    number_network_cards = input('Combien de carte '
                                 'réseaux voulez-vous utiliser ? '
                                 '(ex: 1) ')
    if int(number_network_cards) == 1:
        network_card = input('Quel carte réseau voulez-vous utiliser ? '
                             '(ex: enp0s3) ')

        # Add the card in /etc/default/isc-dhcp-server
        run("sudo sed -i 's/INTERFACESv4=/INTERFACESv4=\""
            + network_card + "\"/g' /etc/default/isc-dhcp-server")
        return nat_mode()

    if int(number_network_cards) > 1:
        while i < int(number_network_cards):
            network_card = input('Quel carte réseau voulez-vous '
                                 'utiliser ? (ex: enp0s3) ')
            list_cards.append(network_card)
            i += 1

        # Create a loop for config the file
        for cards in list_cards:
            # Create a file for get cards
            run('touch network_cards_nbr')
            run('sudo bash -c \'echo "' + cards + '" >> network_cards_nbr\'')
            run('sudo tr "\n" " " < network_cards_nbr > network_cards_nbr_out')
        used_cards = run('cat network_cards_nbr_out')

        # Add the cards in /etc/default/isc-dhcp-server
        run("sudo sed -i 's/INTERFACESv4=/INTERFACESv4=\""
            + used_cards + "\"/g' /etc/default/isc-dhcp-server")
        run('sudo rm network_cards_nbr')
        run('sudo rm network_cards_nbr_out')
    return nat_mode()


def configure_dhcp_with_vlans():
    """ This method is used to configure the vlans to the DHCP server  """
    i = 0
    newtork_numbers = input('De combien de sous-réseaux '
                            'aves-vous besoin ? ')
    network_card = input('Quel carte réseau voulez-vous utiliser ? ')

    while i < int(newtork_numbers):
        # Get informations for subnets
        vlans_name = input('Indiquez le nom de '
                           'votre vlans (ex: VLAN 1 Commercial) ')
        ip_network = input('Indiquez l\'addresse IP '
                           'du sous réseau (ex: 192.168.1.0) ')
        netmask = input('Indiquez le masque du réseau (ex: 255.255.255.0) ')
        range_ip_1 = input('Indiquez le range d\'addresses IP (départ) ')
        range_ip_2 = input('Indiquez le range d\'addresses IP (fin) ')
        option_domain_name_servers = input('Indiquez le DNS ')
        option_domain_name = input('Indiquez le nom de domaine ')
        option_routers = input('Indiquez la passerelle à utiliser ')
        option_broadcast_address = input('Indiquez l\'IP broadcast ')
        default_lease_time = input(
            'Indiquez la durée d\'attribution et de reservation d\'une IP'
            ' en seconde par défault (ex: 600) ')
        max_lease_time = input(
            'Indiquez la durée d\'attribution et de'
            ' reservation maximal d\'une IP en seconde (ex: 7200) ')

        run('sudo bash -c \'echo "#' + vlans_name +
            '" >> /etc/dhcp/dhcpd.conf\'')
        run('sudo bash -c \'echo "subnet ' + ip_network +
            ' netmask ' + netmask + ' {"' + '>> /etc/dhcp/dhcpd.conf\'')
        run('sudo bash -c \'echo " range ' + range_ip_1 + ' '
            + range_ip_2 + ';"' + '>> /etc/dhcp/dhcpd.conf\'')
        run('sudo bash -c \'echo " option domain-name-servers '
            + option_domain_name_servers + ';"' + '>> /etc/dhcp/dhcpd.conf\'')
        run('sudo bash -c \'echo " option domain-name \"'
            + option_domain_name + '\";"' + '>> /etc/dhcp/dhcpd.conf\'')
        run("sudo sed -i 's/option domain-name " +
            option_domain_name + ";/option domain-name \""
            + option_domain_name + "\";/g' /etc/dhcp/dhcpd.conf")
        run('sudo bash -c \'echo " option routers '
            + option_routers + ';"' + '>> /etc/dhcp/dhcpd.conf\'')
        run('sudo bash -c \'echo " option broadcast-address '
            + option_broadcast_address + ';"' + '>> /etc/dhcp/dhcpd.conf\'')
        run('sudo bash -c \'echo " default-lease-time '
            + default_lease_time + ';"' + '>> /etc/dhcp/dhcpd.conf\'')
        run('sudo bash -c \'echo  " max-lease-time '
            + max_lease_time + ';"' + '>> /etc/dhcp/dhcpd.conf\'')
        run('sudo bash -c \'echo "}" >> /etc/dhcp/dhcpd.conf\'')
        i += 1
    return configure_network_cards_vlans(newtork_numbers, network_card)


def configure_network_cards_vlans(newtork_numbers, network_card):
    """ This method is used to configure the network vlans """

    i = 0
    a = 2
    # Config isc-dhcp-server
    run('sudo bash -c \'echo "INTERFACESv4=" > /etc/default/isc-dhcp-server\'')

    # Create a list for config vlans
    list_vlans = []
    while i < int(newtork_numbers):
        list_vlans.append(network_card + '.' + str(a))
        i += 1
        a += 1

    # Create a loop for config the file
    for vlans in list_vlans:
        # Create a file for get cards
        run('touch network_vlans_nbr')
        run('sudo bash -c \'echo "' + vlans + '" >> network_vlans_nbr\'')
        run('sudo tr "\n" " " < network_vlans_nbr > network_vlans_nbr_out')
    used_vlans = run('cat network_vlans_nbr_out')

    # Add the vlans in /etc/default/isc-dhcp-server
    run("sudo sed -i 's/INTERFACESv4=/INTERFACESv4=\""
        + used_vlans + "\"/g' /etc/default/isc-dhcp-server")
    run('sudo rm network_vlans_nbr')
    run('sudo rm network_vlans_nbr_out')
    return nat_mode()


def nat_mode():
    """ This method is used to configure the NAT mode with POSTROUTING  """

    nat_mode = input('Voulez vous que votre serveur'
                     ' utilise le POSTROUTING NAT ? (répondre par yes ou no) ')
    # Check if user have need the nat mode
    if nat_mode == 'yes':
        # Install iptables-persistent
        run('sudo apt-get update')
        run('sudo apt-get install -y iptables-persistent')

        # Modify intial configuration for the forwading IPv4
        run('sudo bash -c \'echo "1" > /proc/sys/net/ipv4/ip_forward\'')
        run('sudo sed -i "s/#net.ipv4.ip_forward/net.ipv4.ip_forward/g"'
            ' /etc/sysctl.conf')

        # Choice the card for POSTROUTING
        network_card_nat = input('Indiquez la carte réseau qui '
                                 'permettra le POSTROUTING (ex: enp0s3) ')
        run('sudo iptables -t nat -A POSTROUTING -o '
            + network_card_nat + ' -j MASQUERADE')
        # Save POSTROUTING
        run('touch persitent')
        run('sudo iptables-save >> persitent')
        iptables_persistent = run('sudo cat persitent')
        run('sudo bash -c \'echo "' +
            iptables_persistent + '" >> /etc/iptables/rules.v4\'')
        run('sudo rm persitent')
        print('POSTROUTING NAT effectif !')
        # Restart DHCP
        run('sudo systemctl restart isc-dhcp-server')
        return done_configuration()

    if nat_mode == 'no':
        # Restart DHCP
        run('sudo systemctl restart isc-dhcp-server')
        return done_configuration()


def done_configuration():
    """ This method is used to done the config """

    print('Vos configuration sont terminées !')
    done_conf = input('Voulez-vous redémarrer le serveur ?'
                      ' (répondre par yes ou no) ')
    if done_conf == 'yes':
        run('sudo reboot')
    else:
        pass
