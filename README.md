# Gestion_Coding


Le repos Gestion_coding est basé sur des scripts d'automatisation.    
Ces scripts permettent à un Administrateur système d'automatiser la réinitialisation d'un poste client Linux et l'installation du service DHCP sous Linux.


## Courte explications des fonctionnalités de base:

### Setup.py
-Le script setup.py est le script d'uilisation principal.

### Install_dhcp.py
-Le script install_dhcp.py installe le services DHCP. Il permet également de le configurer plus facilement, et rapidement.

### Reset_computeur.py
-Le script reset_computeur.py réinitialise automatiquement un poste client.


## A savoir:
Ce code fonctionne uniquement dans un environnement Linux, en communication avec des postes et serveurs Linux.
SSH mode serveur doit être installé sur les postes, du fait que ces scripts commmuniquent avec les machines via SSH.

### Installation du code en production
-git clone https://github.com/Kyossen/Gestion_Coding       
-pip3 install -r requirements.txt        

## Pré-requis:     
-Python 3.x       
-SSH Client et SSH Serveur  
