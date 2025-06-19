# 🎮 P_D-moMot

**P_D-moMot** est un jeu multijoueur en Python avec interface graphique, où plusieurs joueurs peuvent rejoindre un lobby et participer à des parties en temps réel.

---

## 🚀 Fonctionnalités

- 🎮 Plusieurs mini-jeux intégrés (Snake, Pendu, Morpion, Blackjack, etc.)
- 🖥️ Interface utilisateur responsive avec **Pygame**
- 🧑‍🤝‍🧑 Système de lobby multijoueur (en cours de développement)
- 💾 Sauvegarde des scores (à venir)
- ⚙️ Gestion des textures et des ressources graphique
- 🎴 Système complet de cartes pour les jeux de type Blackjack

---

## 🛠️ Technologies utilisées

- 🐍 Python 3.13
- 🎮 Pygame

---

## 📁 Structure du projet


```bash
P_Dmot/
├── __pycache__/
│   └── main.cpython-311.pyc
├── game/
│   ├── __pycache__/
│   ├── cards/
│   │   ├── 2-C.png
│   │   ├── 2-D.png
│   │   ├── 2-H.png
│   │   ├── 2-S.png
│   │   ├── 3-C.png
│   │   ├── 3-D.png
│   │   ├── 3-H.png
│   │   ├── 3-S.png
│   │   ├── 4-C.png
│   │   ├── 4-D.png
│   │   ├── 4-H.png
│   │   ├── 4-S.png
│   │   ├── 5-C.png
│   │   ├── 5-D.png
│   │   ├── 5-H.png
│   │   ├── 5-S.png
│   │   ├── 6-C.png
│   │   ├── 6-D.png
│   │   ├── 6-H.png
│   │   ├── 6-S.png
│   │   ├── 7-C.png
│   │   ├── 7-D.png
│   │   ├── 7-H.png
│   │   ├── 7-S.png
│   │   ├── 8-C.png
│   │   ├── 8-D.png
│   │   ├── 8-H.png
│   │   ├── 8-S.png
│   │   ├── 9-C.png
│   │   ├── 9-D.png
│   │   ├── 9-H.png
│   │   ├── 9-S.png
│   │   ├── 10-C.png
│   │   ├── 10-D.png
│   │   ├── 10-H.png
│   │   ├── 10-S.png
│   │   ├── J-C.png
│   │   ├── J-D.png
│   │   ├── J-H.png
│   │   ├── J-S.png
│   │   ├── Q-C.png
│   │   ├── Q-D.png
│   │   ├── Q-H.png
│   │   ├── Q-S.png
│   │   ├── K-C.png
│   │   ├── K-D.png
│   │   ├── K-H.png
│   │   ├── K-S.png
│   │   ├── A-C.png
│   │   ├── A-D.png
│   │   ├── A-H.png
│   │   ├── A-S.png
│   │   └── BACK.png
│   ├── snake/
│   │   ├── angle.png
│   │   ├── bg.jpg
│   │   ├── bg1.jpg
│   │   ├── corps1.png
│   │   ├── keu.png
│   │   ├── pomme.png
│   │   └── tete.png
│   ├── blackjack.py
│   ├── fpc.py
│   ├── french.txt
│   ├── memoir.py
│   ├── morpoin.py
│   ├── pendu.py
│   ├── pong2.py
│   ├── pongbot.py
│   ├── snak.py
│   ├── template.py
│   └── tetris.py
├── textures/
│   ├── bleu.png
│   ├── cyan.png
│   ├── green.png
│   ├── logo.ico
│   ├── logo.png
│   ├── orange.png
│   ├── red.png
│   ├── violet.png
│   └── yellow.png
├── main.py
├── README.md
└── task.md
```

bash
Copier
Modifier

## ▶️ Lancer le projet

### 1. Cloner le dépôt

```bash
git clone https://github.com/djdams1/P_D-moMot.git
cd P_D-moMot
```
2. Installer les dépendances
```bash
pip install pygame
```
3. Lancer le jeu
```bash
python main.py
```
🧠 TODO
Optimiser le lobby

Gérer les déconnexions

Ajouter des animations

Sauvegarder les scores

🤝 Contribuer
Fork le repo, crée ta branche (git checkout -b feat/ma-fonctionnalité), code, push et propose une Pull Request.

## 📄 Licence

Ce projet est protégé par la **GNU General Public License v3.0**.

Cela signifie que :
- ✅ Vous pouvez copier, modifier, redistribuer le code...
- ❗️ ...à condition que toute version dérivée soit aussi libre (même licence).
- 🚫 Utilisation dans des logiciels propriétaires interdite.

🧾 Voir le fichier [LICENSE](./LICENSE) pour la version complète de la licence.
