# Groupe de lecler_a 1005883

# Connexion ssh vm aws :

- ip : 16.16.122.157

- ssh 16.16.122.157

- ssh admin@16.16.122.157

- chmod 400 AnsibleKey.pem
- ssh -i "AnsibleKey.pem" admin@ec2-16-16-122-157.eu-north-1.compute.amazonaws.com

# Lancement du code :

- python3 setup.py install
- mla -f todos.yml -i inventory.yml (grace au fihcier setup.py, on a pu créer la commande mla)

# Explication du code :

Le code comporte un fichier mla_script.py qui va executer la fonction main du fichier mla.py  
Le fichier mla.py vient faire appel aux différents modules demandés  
Chaque module vient faire son job et retourne un status d'exécution afin de savoir si il s'est bien terminé ou non  
Les status sont stocké dans un dictionnaire "stats" afin d'être comptabilisés  
Une connexion en ssh est effectué sur les hosts d'inventory.yml et le programme execute les todos sur chaque hosts
