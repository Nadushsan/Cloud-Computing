#!/usr/bin/env python3
# Nada Oualadi + Bouchra Outafraout
import openstack
import sys
from openstack import exceptions

def connect_devstack_admin():
    """Connexion spécifique au cloud devstack-admin"""
    try:
        print("🔐 Connexion au cloud: devstack-admin")
        conn = openstack.connect(cloud='devstack-admin')
        
        # Test de la connexion
        token = conn.identity.get_token()
        print("✅ Connexion administrateur établie avec succès")
        print(f"📋 Projet: {getattr(token, 'project_name', 'Admin')}")
        return conn
    except Exception as e:
        print(f"❌ Erreur de connexion administrateur: {e}")
        sys.exit(1)

def list_all_projects(conn):
    """Lister tous les projets avec détails"""
    print("\n" + "="*80)
    print("🏢 PROJETS - INVENTAIRE COMPLET")
    print("="*80)
    
    try:
        projects = list(conn.identity.projects())
        print(f"📊 Total: {len(projects)} projets\n")
        
        for project in projects:
            print(f"📍 PROJET: {project.name}")
            print(f"   🆔 ID: {project.id}")
            
            description = getattr(project, 'description', 'Non spécifiée')
            if description:
                print(f"   📝 Description: {description}")
            
            enabled = getattr(project, 'enabled', True)
            status = "✅ ACTIF" if enabled else "❌ INACTIF"
            print(f"   📈 Statut: {status}")
            
            domain_id = getattr(project, 'domain_id', 'default')
            print(f"   🌐 Domain ID: {domain_id}")
            
            # Compter les ressources par projet
            try:
                servers = list(conn.compute.servers(all_projects=True))
                project_servers = [s for s in servers if s.project_id == project.id]
                print(f"   🖥️  Serveurs: {len(project_servers)}")
            except:
                print(f"   🖥️  Serveurs: Information non disponible")
            
            print("-" * 60)
            
    except Exception as e:
        print(f"❌ Erreur lors du listing des projets: {e}")

def list_all_users(conn):
    """Lister tous les utilisateurs avec détails complets"""
    print("\n" + "="*80)
    print("👥 UTILISATEURS - INVENTAIRE COMPLET")
    print("="*80)
    
    try:
        users = list(conn.identity.users())
        print(f"📊 Total: {len(users)} utilisateurs\n")
        
        for user in users:
            print(f"👤 UTILISATEUR: {user.name}")
            print(f"   🆔 ID: {user.id}")
            
            email = getattr(user, 'email', 'Non spécifié')
            if email:
                print(f"   📧 Email: {email}")
            
            enabled = getattr(user, 'enabled', True)
            status = "✅ ACTIF" if enabled else "❌ INACTIF"
            print(f"   📈 Statut: {status}")
            
            description = getattr(user, 'description', '')
            if description:
                print(f"   📝 Description: {description}")
            
            domain_id = getattr(user, 'domain_id', 'default')
            print(f"   🌐 Domain ID: {domain_id}")
            
            # Dernière connexion si disponible
            last_login = getattr(user, 'last_login_at', None)
            if last_login:
                print(f"   ⏰ Dernière connexion: {last_login}")
            
            print("-" * 60)
            
    except Exception as e:
        print(f"❌ Erreur lors du listing des utilisateurs: {e}")

def list_all_servers(conn):
    """Lister tous les serveurs de tous les projets"""
    print("\n" + "="*80)
    print("🖥️  SERVEURS - INVENTAIRE COMPLET")
    print("="*80)
    
    try:
        # all_projects=True pour voir tous les serveurs de tous les projets
        servers = list(conn.compute.servers(all_projects=True))
        print(f"📊 Total: {len(servers)} serveurs\n")
        
        for server in servers:
            # Icône de statut
            status_icon = "🟢" if server.status == "ACTIVE" else "🔴" if server.status == "SHUTOFF" else "🟡"
            
            print(f"{status_icon} SERVEUR: {server.name}")
            print(f"   🆔 ID: {server.id}")
            print(f"   📊 Statut: {server.status}")
            print(f"   📂 Projet ID: {server.project_id}")
            
            # Trouver le nom du projet
            try:
                project = conn.identity.get_project(server.project_id)
                print(f"   🏢 Projet: {project.name}")
            except:
                print(f"   🏢 Projet: {server.project_id}")
            
            # Informations sur le flavor
            if hasattr(server, 'flavor'):
                flavor_info = server.flavor
                if hasattr(flavor_info, 'original_name'):
                    print(f"   💾 Flavor: {flavor_info.original_name}")
                else:
                    print(f"   💾 Flavor ID: {flavor_info.get('id', 'N/A')}")
            
            # Adresses IP détaillées
            if server.addresses:
                print(f"   🌐 Adresses IP:")
                for network, addresses in server.addresses.items():
                    for addr in addresses:
                        version = "IPv4" if addr['version'] == 4 else "IPv6"
                        print(f"      - {network}: {addr['addr']} ({version})")
            else:
                print(f"   🌐 Aucune adresse IP")
            
            print(f"   📅 Créé le: {server.created_at}")
            print(f"   🔄 Mis à jour: {server.updated_at}")
            print("-" * 60)
            
    except Exception as e:
        print(f"❌ Erreur lors du listing des serveurs: {e}")

def list_all_images(conn):
    """Lister toutes les images avec détails"""
    print("\n" + "="*80)
    print("🖼️  IMAGES - INVENTAIRE COMPLET")
    print("="*80)
    
    try:
        images = list(conn.image.images())
        print(f"📊 Total: {len(images)} images\n")
        
        for image in images:
            print(f"📸 IMAGE: {image.name}")
            print(f"   🆔 ID: {image.id}")
            print(f"   📊 Statut: {getattr(image, 'status', 'N/A')}")
            
            size = getattr(image, 'size', None)
            if size and isinstance(size, int):
                size_mb = size // 1024 // 1024
                size_gb = size_mb // 1024
                if size_gb > 0:
                    print(f"   💾 Taille: {size_gb} GB ({size_mb} MB)")
                else:
                    print(f"   💾 Taille: {size_mb} MB")
                print(f"   📏 Taille en octets: {size}")
            
            print(f"   👁️  Visibilité: {getattr(image, 'visibility', 'N/A')}")
            print(f"   📁 Format: {getattr(image, 'disk_format', 'N/A')}")
            print(f"   📦 Conteneur: {getattr(image, 'container_format', 'N/A')}")
            
            protected = getattr(image, 'protected', False)
            print(f"   🛡️  Protégée: {'✅ OUI' if protected else '❌ NON'}")
            
            # Tags
            tags = getattr(image, 'tags', [])
            if tags:
                print(f"   🏷️  Tags: {', '.join(tags)}")
            
            print(f"   📅 Créé le: {getattr(image, 'created_at', 'N/A')}")
            print(f"   🔄 Mis à jour: {getattr(image, 'updated_at', 'N/A')}")
            print("-" * 60)
            
    except Exception as e:
        print(f"❌ Erreur lors du listing des images: {e}")

def list_all_flavors(conn):
    """Lister tous les flavors disponibles"""
    print("\n" + "="*80)
    print("💾 FLAVORS - INVENTAIRE COMPLET")
    print("="*80)
    
    try:
        flavors = list(conn.compute.flavors())
        print(f"📊 Total: {len(flavors)} flavors\n")
        
        for flavor in flavors:
            print(f"⚡ FLAVOR: {flavor.name}")
            print(f"   🆔 ID: {flavor.id}")
            print(f"   📝 Description: {getattr(flavor, 'description', 'N/A')}")
            print(f"   🎯 VCPUs: {flavor.vcpus}")
            print(f"   💽 RAM: {flavor.ram} MB")
            print(f"   💾 Disk: {flavor.disk} GB")
            print(f"   📊 Swap: {flavor.swap} MB")
            
            enabled = getattr(flavor, 'is_public', True)
            print(f"   🌐 Public: {'✅ OUI' if enabled else '❌ NON'}")
            
            ephemeral = getattr(flavor, 'ephemeral', 0)
            if ephemeral > 0:
                print(f"   🗂️  Disk éphemère: {ephemeral} GB")
            
            print("-" * 60)
            
    except Exception as e:
        print(f"❌ Erreur lors du listing des flavors: {e}")

def list_all_networks(conn):
    """Lister tous les réseaux"""
    print("\n" + "="*80)
    print("🌐 RÉSEAUX - INVENTAIRE COMPLET")
    print("="*80)
    
    try:
        networks = list(conn.network.networks())
        print(f"📊 Total: {len(networks)} réseaux\n")
        
        for network in networks:
            print(f"🔗 RÉSEAU: {network.name}")
            print(f"   🆔 ID: {network.id}")
            print(f"   📂 Projet ID: {network.project_id}")
            
            status = getattr(network, 'status', 'N/A')
            status_icon = "🟢" if status == "ACTIVE" else "🔴" if status == "DOWN" else "🟡"
            print(f"   📊 Statut: {status_icon} {status}")
            
            admin_state = "✅ UP" if network.is_admin_state_up else "❌ DOWN"
            print(f"   🏃 Admin State: {admin_state}")
            
            shared = "✅ OUI" if network.is_shared else "❌ NON"
            print(f"   🔗 Partagé: {shared}")
            
            external = "✅ OUI" if network.is_router_external else "❌ NON"
            print(f"   🌍 Externe: {external}")
            
            # Sous-réseaux
            subnets = getattr(network, 'subnet_ids', [])
            print(f"   📡 Sous-réseaux: {len(subnets)}")
            for subnet_id in subnets[:3]:  # Afficher les 3 premiers
                print(f"      - {subnet_id}")
            if len(subnets) > 3:
                print(f"      ... et {len(subnets) - 3} autres")
            
            print("-" * 60)
            
    except Exception as e:
        print(f"❌ Erreur lors du listing des réseaux: {e}")

def list_all_services(conn):
    """Lister tous les services OpenStack"""
    print("\n" + "="*80)
    print("🔧 SERVICES OPENSTACK - INVENTAIRE COMPLET")
    print("="*80)
    
    try:
        services = list(conn.identity.services())
        print(f"📊 Total: {len(services)} services\n")
        
        # Grouper par type
        services_by_type = {}
        for service in services:
            service_type = service.type
            if service_type not in services_by_type:
                services_by_type[service_type] = []
            services_by_type[service_type].append(service)
        
        for service_type, service_list in services_by_type.items():
            print(f"\n📋 {service_type.upper()}:")
            for service in service_list:
                print(f"   🛠️  {service.name}")
                print(f"      🆔 ID: {service.id}")
                description = getattr(service, 'description', 'Non spécifiée')
                if description:
                    print(f"      📝 Description: {description}")
                enabled = getattr(service, 'enabled', True)
                status = "✅ ACTIF" if enabled else "❌ INACTIF"
                print(f"      📈 Statut: {status}")
            
    except Exception as e:
        print(f"❌ Erreur lors du listing des services: {e}")

def main():
    """Fonction principale - Inventaire complet avec devstack-admin"""
    print("="*80)
    print("🚀 INVENTAIRE OPENSTACK COMPLET - devstack-admin")
    print("="*80)
    
    # Connexion avec devstack-admin
    conn = connect_devstack_admin()
    
    # Inventaire complet
    list_all_projects(conn)
    list_all_users(conn)
    list_all_servers(conn)
    list_all_images(conn)
    list_all_flavors(conn)
    list_all_networks(conn)
    list_all_services(conn)
    
    print("\n" + "="*80)
    print("✅ INVENTAIRE COMPLET TERMINÉ AVEC SUCCÈS!")
    print("="*80)

if __name__ == "__main__":
    main()
