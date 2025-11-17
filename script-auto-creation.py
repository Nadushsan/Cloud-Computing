#!/usr/bin/env python3
import openstack
import sys
import time
from openstack import exceptions

def connect_openstack(cloud_name='devstack-admin'):
    """Connexion à OpenStack"""
    try:
        print(f"🔗 Connexion au cloud: {cloud_name}")
        conn = openstack.connect(cloud=cloud_name)
        print("✅ Connexion établie avec succès")
        return conn
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        sys.exit(1)

def wait_for_server_status(conn, server, expected_status='ACTIVE', max_wait=300):
    """Attendre qu'un serveur atteigne un statut spécifique"""
    print(f"⏳ Attente que l'instance devienne {expected_status}...")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            server = conn.compute.get_server(server.id)
            current_status = server.status
            
            if current_status == expected_status:
                print(f"✅ Instance maintenant {expected_status}!")
                return server
            elif current_status == 'ERROR':
                print("❌ L'instance est en erreur")
                return None
            
            print(f"📊 Statut actuel: {current_status} - Attente...")
            time.sleep(5)
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la vérification du statut: {e}")
            time.sleep(5)
    
    print(f"❌ Timeout: L'instance n'est pas devenue {expected_status} après {max_wait} secondes")
    return None

def create_instance_simple(conn):
    """Créer une instance de manière simple et directe"""
    print("🚀 CRÉATION RAPIDE D'INSTANCE OPENSTACK")
    print("="*50)
    
    # Nom de l'instance
    instance_name = input("📝 Entrez le nom de l'instance: ").strip()
    if not instance_name:
        instance_name = f"instance-{time.strftime('%Y%m%d-%H%M%S')}"
    
    # Obtenir les ressources disponibles
    print("\n📡 Récupération des ressources disponibles...")
    
    # Images
    images = list(conn.image.images())
    print("\n🖼️  Images disponibles:")
    for i, image in enumerate(images):
        print(f"   {i+1}. {image.name}")
    
    image_choice = int(input("Choisissez une image (numéro): ")) - 1
    selected_image = images[image_choice]
    
    # Flavors
    flavors = list(conn.compute.flavors())
    print("\n💾 Flavors disponibles:")
    for i, flavor in enumerate(flavors):
        print(f"   {i+1}. {flavor.name} - {flavor.vcpus}vCPUs, {flavor.ram}MB RAM")
    
    flavor_choice = int(input("Choisissez un flavor (numéro): ")) - 1
    selected_flavor = flavors[flavor_choice]
    
    # Réseaux
    networks = list(conn.network.networks())
    print("\n🌐 Réseaux disponibles:")
    for i, network in enumerate(networks):
        print(f"   {i+1}. {network.name}")
    
    network_choice = int(input("Choisissez un réseau (numéro): ")) - 1
    selected_network = networks[network_choice]
    
    # Clé SSH
    keypair_name = None
    keypairs = list(conn.compute.keypairs())
    if keypairs:
        print("\n🔑 Clés SSH disponibles:")
        print("   0. Aucune clé SSH")
        for i, keypair in enumerate(keypairs):
            print(f"   {i+1}. {keypair.name}")
        
        key_choice = int(input("Choisissez une clé SSH (numéro): "))
        if key_choice != 0:
            keypair_name = keypairs[key_choice - 1].name
    else:
        print("\n⚠️  Aucune clé SSH trouvée - création sans clé SSH")
    
    # Confirmation
    print("\n" + "="*50)
    print("📋 RÉSUMÉ DE LA CONFIGURATION")
    print("="*50)
    print(f"📝 Nom: {instance_name}")
    print(f"🖼️  Image: {selected_image.name}")
    print(f"💾 Flavor: {selected_flavor.name}")
    print(f"🌐 Réseau: {selected_network.name}")
    print(f"🔑 Clé SSH: {keypair_name or 'Aucune'}")
    
    confirmation = input("\n✅ Confirmer la création? (o/n): ").lower()
    if confirmation != 'o':
        print("❌ Création annulée")
        return
    
    # Création de l'instance
    print(f"\n🚀 Démarrage de la création de l'instance: {instance_name}")
    
    try:
        # Configuration du serveur
        server_config = {
            'name': instance_name,
            'image_id': selected_image.id,
            'flavor_id': selected_flavor.id,
            'networks': [{'uuid': selected_network.id}]
        }
        
        if keypair_name:
            server_config['key_name'] = keypair_name
        
        # Créer l'instance
        print("📦 Création de l'instance en cours...")
        server = conn.compute.create_server(**server_config)
        print(f"📨 Commande de création envoyée - ID: {server.id}")
        
        # Attendre que l'instance soit active avec notre propre fonction
        server = wait_for_server_status(conn, server, 'ACTIVE', 300)
        
        if not server:
            print("❌ Échec de la création de l'instance")
            return
        
        print(f"✅ Instance créée avec succès!")
        
        # Afficher les détails
        print("\n" + "="*50)
        print("📊 DÉTAILS DE L'INSTANCE")
        print("="*50)
        print(f"🆔 ID: {server.id}")
        print(f"📝 Nom: {server.name}")
        print(f"📊 Statut: {server.status}")
        
        # Récupérer les informations fraîches du serveur
        server = conn.compute.get_server(server.id)
        
        # Afficher les adresses IP
        if server.addresses:
            print("🌐 Adresses IP:")
            for network_name, addresses in server.addresses.items():
                for address in addresses:
                    if address['version'] == 4:
                        print(f"   📍 {network_name}: {address['addr']}")
        else:
            print("🌐 Aucune adresse IP assignée pour le moment")
        
        # Commande SSH si clé utilisée
        if keypair_name and server.addresses:
            for network_name, addresses in server.addresses.items():
                for address in addresses:
                    if address['version'] == 4:
                        print(f"\n🔗 Pour vous connecter en SSH:")
                        # Deviner l'utilisateur selon l'image
                        username = "cirros" if "cirros" in selected_image.name.lower() else "ubuntu"
                        print(f"   ssh -i ~/.ssh/{keypair_name} {username}@{address['addr']}")
                        break
                break
        
        print(f"\n🎉 Instance prête à l'emploi!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        import traceback
        traceback.print_exc()

def create_instance_auto(conn, instance_name=None, image_name=None, flavor_name=None, network_name=None):
    """Créer une instance avec des paramètres automatiques"""
    if not instance_name:
        instance_name = f"auto-instance-{time.strftime('%Y%m%d-%H%M%S')}"
    
    print(f"🚀 CRÉATION AUTOMATIQUE: {instance_name}")
    print("="*50)
    
    try:
        # Trouver l'image (par défaut: cirros)
        images = list(conn.image.images())
        if image_name:
            image = next((img for img in images if image_name in img.name), None)
        else:
            # Prendre la première image disponible
            image = images[0] if images else None
        
        if not image:
            print("❌ Aucune image trouvée")
            return
        
        # Trouver le flavor (par défaut: m1.tiny)
        flavors = list(conn.compute.flavors())
        if flavor_name:
            flavor = next((flv for flv in flavors if flavor_name in flv.name), None)
        else:
            # Prendre le plus petit flavor
            flavor = min(flavors, key=lambda x: x.ram) if flavors else None
        
        if not flavor:
            print("❌ Aucun flavor trouvé")
            return
        
        # Trouver le réseau (par défaut: premier réseau disponible)
        networks = list(conn.network.networks())
        if network_name:
            network = next((net for net in networks if network_name in net.name), None)
        else:
            network = networks[0] if networks else None
        
        if not network:
            print("❌ Aucun réseau trouvé")
            return
        
        print("📋 Configuration automatique:")
        print(f"   Image: {image.name}")
        print(f"   Flavor: {flavor.name}")
        print(f"   Réseau: {network.name}")
        
        # Créer l'instance
        server_config = {
            'name': instance_name,
            'image_id': image.id,
            'flavor_id': flavor.id,
            'networks': [{'uuid': network.id}]
        }
        
        print("📦 Création en cours...")
        server = conn.compute.create_server(**server_config)
        server = wait_for_server_status(conn, server, 'ACTIVE', 300)
        
        if server:
            print(f"✅ Instance créée: {server.name}")
            
            # Afficher l'IP
            server = conn.compute.get_server(server.id)
            if server.addresses:
                for network_name, addresses in server.addresses.items():
                    for address in addresses:
                        if address['version'] == 4:
                            print(f"🌐 IP: {address['addr']}")
                            break
                    break
        else:
            print("❌ Échec de la création de l'instance")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def main():
    """Fonction principale"""
    print("🚀 CREATEUR D'INSTANCE OPENSTACK - MODE DIRECT")
    print("="*50)
    
    # Connexion
    conn = connect_openstack('devstack-admin')
    
    # Demander le mode
    print("\n🎯 Choisissez le mode de création:")
    print("1. 🔧 Mode interactif (vous choisissez tout)")
    print("2. ⚡ Mode automatique (paramètres par défaut)")
    
    choice = input("\nChoisissez le mode (1 ou 2): ").strip()
    
    if choice == '1':
        create_instance_simple(conn)
    elif choice == '2':
        instance_name = input("Nom de l'instance (laisser vide pour auto-généré): ").strip()
        create_instance_auto(conn, instance_name)
    else:
        print("❌ Choix invalide, utilisation du mode interactif")
        create_instance_simple(conn)

if __name__ == "__main__":
    main()
