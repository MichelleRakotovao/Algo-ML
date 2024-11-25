# Sliding Puzzle Solver

---

## 🧩 Description du projet

Le projet **Sliding Puzzle Solver** est une application interactive et éducative permettant de jouer à des puzzles glissants (8-puzzle et 15-puzzle) et de les résoudre à l'aide de l'algorithme **A***. L'objectif est d'aligner les chiffres dans l'ordre croissant avec la case vide en dernière position.

---

## Fonctionnalités principales

- **Mode jouable** :
  - L'utilisateur peut déplacer les tuiles pour résoudre manuellement le puzzle.
  - Une interface graphique intuitive affiche chaque déplacement.
  
- **Mode solveur** :
  - Une fonctionnalité automatique permet de résoudre le puzzle en utilisant l'algorithme A*.
  - Affichage en temps réel des étapes de résolution.

- **Options de configuration** :
  - Choix entre un puzzle 8-puzzle (3x3) et un 15-puzzle (4x4).
  - Boutons pour mélanger, réinitialiser ou résoudre le puzzle.

---

## 🎮 Utilisation

### Prérequis

- Python 3.10+
- Pygame 2.6.1+

### Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-repo/sliding-puzzle-solver.git
   cd sliding-puzzle-solver
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
3. Lancez l'installation :
   ```bash
   python main.py

---

## **Interface utilisateur**

L'interface utilisateur est conçue avec `pygame` pour fournir une expérience interactive et visuelle. Elle inclut :

1. Une grille pour afficher les tuiles du puzzle (8-puzzle ou 15-puzzle, selon le choix de l'utilisateur).
2. Trois boutons principaux :
   - **Shuffle** : Mélange aléatoirement les tuiles pour commencer un nouveau puzzle.
   - **Reset** : Réinitialise la grille à son état initial.
   - **Solver** : Déclenche le solveur pour afficher les étapes vers la solution.
3. Les étapes de la résolution par le solveur sont affichées une à une avec des animations.

---

## **Structure du projet**

Voici une description des fichiers et modules principaux du projet :

- `main.py` : Point d'entrée principal du programme. Il gère la boucle de jeu principale.
- `modules/` : Contient les fichiers nécessaires au fonctionnement du jeu.
  - `settings.py` : Définit les constantes utilisées dans le projet (dimensions, couleurs, etc.).
  - `sprite.py` : Définit les classes et méthodes liées aux tuiles et à leur interaction.
  - `interface.py` : Gère l'interface utilisateur et la logique du jeu, y compris le solveur automatique.
- `requirements.txt` : Liste des dépendances nécessaires pour exécuter le projet.

---

## **Membres de l'équipe**

Ce projet a été réalisé par une équipe de 6 membres. Voici la répartition des rôles :

1. **TOVO Jean Bien Aimé** : Gestion de projet et intégration finale. Tests et optimisation des performances.
2. **RAHERIMANANA Koloina Mandresy** : Développement du solveur avec l'algorithme A*. Exportation sous format .csv
3. **RAMAHEFARISON Nambinitsoa Thierry** : Conception de l'interface utilisateur.
4. **RAJOHARIVELO Andriarivony Antenaina** : Documentation et rédaction du README.
5. **RAKOTOVAO Josée Michelle** : Implémentation des fonctionnalités du mode jouable.
6. **RAKOTOMAHARAVO Vali Fanomezantsoa**

---
