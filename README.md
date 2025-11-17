# Rapport du cloud computing 
# ☁️ OpenStack Cloud Management Toolkit

**Outils d'automatisation et d'inventaire pour OpenStack**  
*Développé par Nada Oualadi & Bouchra Outafraout*

---

## 📋 Description

Ce projet fournit des scripts Python pour automatiser la gestion et l'inventaire des ressources OpenStack. Il permet aux administrateurs cloud de :

- 🔍 **Inventorier automatiquement** toutes les ressources OpenStack
- 🚀 **Créer des instances** de manière programmatique
- 📊 **Générer des rapports détaillés** sur l'état du cloud

---

## 🛠️ Fonctionnalités

### 📜 Script d'Inventaire (`inventory.py`)
Inventaire complet de toutes les ressources OpenStack :

- **🏢 Projets** - Liste complète avec statut et métriques
- **👥 Utilisateurs** - Détails des comptes et permissions
- **🖥️ Serveurs** - Instances avec statuts, IPs et ressources
- **🖼️ Images** - Catalogue d'images avec tailles et formats
- **💾 Flavors** - Configurations de ressources disponibles
- **🌐 Réseaux** - Topologie réseau et sous-réseaux
- **🔧 Services** - État des services OpenStack

### 🚀 Script d'Automatisation
Création automatisée d'instances avec configuration flexible.

---

## ⚙️ Installation

### Prérequis
```bash
# Installer le client OpenStack Python
pip install python-openstackclient

# Installer les dépendances
pip install openstacksdk
