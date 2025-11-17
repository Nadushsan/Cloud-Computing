```bash
(venv) nada@nada-VM:~/Desktop$ python instance-script2.py 
🚀 CREATEUR D'INSTANCE OPENSTACK - MODE DIRECT
==================================================
🔗 Connexion au cloud: devstack-admin
✅ Connexion établie avec succès

🎯 Choisissez le mode de création:
1. 🔧 Mode interactif (vous choisissez tout)
2. ⚡ Mode automatique (paramètres par défaut)

Choisissez le mode (1 ou 2): 1
🚀 CRÉATION RAPIDE D'INSTANCE OPENSTACK
==================================================
📝 Entrez le nom de l'instance: testinstance

📡 Récupération des ressources disponibles...

🖼️  Images disponibles:
   1. Ubuntu2404
   2. cirros-0.6.3-x86_64-disk
Choisissez une image (numéro): 2

💾 Flavors disponibles:
   1. m1.tiny - 1vCPUs, 512MB RAM
   2. m1.small - 1vCPUs, 2048MB RAM
   3. m1.medium - 2vCPUs, 4096MB RAM
   4. m1.large - 4vCPUs, 8192MB RAM
   5. m1.nano - 1vCPUs, 192MB RAM
   6. m1.xlarge - 8vCPUs, 16384MB RAM
   7. sesnum.tiny - 1vCPUs, 128MB RAM
   8. m1.micro - 1vCPUs, 256MB RAM
   9. cirros256 - 1vCPUs, 256MB RAM
   10. ds512M - 1vCPUs, 512MB RAM
   11. ds1G - 1vCPUs, 1024MB RAM
   12. ds2G - 2vCPUs, 2048MB RAM
   13. ds4G - 4vCPUs, 4096MB RAM
Choisissez un flavor (numéro): 7

🌐 Réseaux disponibles:
   1. public
   2. shared
   3. private
Choisissez un réseau (numéro): 3

🔑 Clés SSH disponibles:
   0. Aucune clé SSH
   1. backup-key-1762103308
   2. mykey
Choisissez une clé SSH (numéro): 2

==================================================
📋 RÉSUMÉ DE LA CONFIGURATION
==================================================
📝 Nom: testinstance
🖼️  Image: cirros-0.6.3-x86_64-disk
💾 Flavor: sesnum.tiny
🌐 Réseau: private
🔑 Clé SSH: mykey

✅ Confirmer la création? (o/n): o

🚀 Démarrage de la création de l'instance: testinstance
📦 Création de l'instance en cours...
📨 Commande de création envoyée - ID: de141028-222c-44ac-a561-575e63462f61
⏳ Attente que l'instance devienne ACTIVE...
📊 Statut actuel: BUILD - Attente...
📊 Statut actuel: BUILD - Attente...
📊 Statut actuel: BUILD - Attente...
✅ Instance maintenant ACTIVE!
✅ Instance créée avec succès!

==================================================
📊 DÉTAILS DE L'INSTANCE
==================================================
🆔 ID: de141028-222c-44ac-a561-575e63462f61
📝 Nom: testinstance
📊 Statut: ACTIVE
🌐 Adresses IP:
   📍 private: 10.0.0.51

🔗 Pour vous connecter en SSH:
   ssh -i ~/.ssh/mykey cirros@10.0.0.51

🎉 Instance prête à l'emploi!
 ```
