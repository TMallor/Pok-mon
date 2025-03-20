# Simulateur de Combat Pokémon

Un simulateur de combat Pokémon textuel implémenté en Python.

## Fonctionnalités

- Choisissez parmi une variété de Pokémon, chacun avec ses propres statistiques et attaques
- Affrontez un adversaire contrôlé par l'ordinateur ou jouez contre un ami en mode multijoueur
- Système de combat au tour par tour fidèle aux jeux Pokémon
- Catégories d'attaques physiques et spéciales
- Système d'efficacité des types (super efficace, pas très efficace)
- Conditions de statut (brûlure, poison, etc.)
- Modifications de statistiques
- Effets météorologiques
- Gestion des PP (Points de Pouvoir)
- Interface colorée avec noms et attaques colorés selon leur type
- Barres de PV qui changent de couleur en fonction des PV restants
- Retour visuel pour les événements de combat et les statuts

## Gameplay

Le gameplay suit le système de combat traditionnel des Pokémon :

1. Choisissez le mode de jeu (solo contre ordinateur ou multijoueur contre un ami)
2. Choisissez une équipe de 3 Pokémon (chaque joueur choisit sa propre équipe en mode multijoueur)
3. Alternez entre sélectionner des attaques ou changer de Pokémon
4. Le Pokémon le plus rapide attaque en premier à chaque tour
5. Battez tous les Pokémon de votre adversaire pour gagner

## Comment exécuter

D'abord, installez les dépendances requises :

```bash
pip install -r requirements.txt
```

Puis lancez le jeu :

```bash
python game.py
```

ou

```bash
python main.py
```

## Contrôles du jeu

- Utilisez les touches numériques pour sélectionner les options pendant le combat
- Suivez les instructions à l'écran pour choisir les attaques ou changer de Pokémon
- En mode multijoueur, les joueurs alternent leurs tours sur le même appareil

## Prérequis

- Python 3.6 ou supérieur
- colorama 0.4.6 (pour les couleurs du terminal)

## Détails d'implémentation

Le simulateur implémente les mécaniques de combat Pokémon suivantes :

- Calcul des dégâts en utilisant la formule officielle de Pokémon
- Tableau d'efficacité des types
- Coups critiques
- STAB (Bonus d'Attaque du Même Type)
- Effets météorologiques sur les dégâts
- Conditions de statut et leurs effets
- Modifications des paliers de statistiques
- Mode multijoueur pour jouer à deux sur le même appareil

## Structure du projet

- `pokemon.py` - Contient la classe Pokemon
- `move.py` - Contient la classe Move pour les attaques Pokémon
- `battle.py` - Contient la classe Battle qui gère les mécaniques de combat
- `data.py` - Contient la base de données des Pokémon et des attaques
- `game.py` - Fichier principal du jeu avec la logique d'interface utilisateur

## Améliorations futures

- Ajouter plus de Pokémon et d'attaques
- Implémenter les talents
- Ajouter des objets tenus
- Implémenter plus de mécaniques de combat (pièges, effets de changement)
- Créer une interface utilisateur graphique
- Améliorer le mode multijoueur avec la possibilité de jouer en réseau

## Auteur

Créé comme projet de programmation pour Ynov B2. 