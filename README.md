# lamz-cli

<div align="center">
  <pre>
   <b> _                         ____ _     ___ 
  | |    __ _ _ __ ___  ____/ ___| |   |_ _|
  | |   / _` | '_ ` _ \|_  / |   | |    | | 
  | |__| (_| | | | | | |/ /| |___| |___ | | 
  |_____\__,_|_| |_| |_/___|\____|_____|___|</b>
  </pre>
  <h3>Le terminal ultime pour regarder et explorer des animes en streaming !</h3>
</div>

---

## 🚀 Présentation

**lamz-cli** est une interface interactive en ligne de commande pour rechercher, explorer et lancer des animes en streaming, directement depuis votre terminal, avec une navigation ultra fluide et colorée.

- 🔎 Recherche intelligente avec suggestions dynamiques
- 🎬 Navigation interactive (anime → saison → épisode)
- ⚡️ Lecture directe dans VLC (ou tout lecteur compatible)
- 🖱️ 100% clavier, aucune souris requise

---

## 📸 Aperçu

![lamz-cli demo](https://user-images.githubusercontent.com/0000000/lamz-cli-demo.gif) 

---

## 🛠️ Installation

### 1. **Cloner le dépôt**

```sh
git clone https://github.com/ton-pseudo/lamz-cli.git
cd lamz-cli
```

### 2. **Installer les dépendances**

Assurez-vous d’avoir Python 3.8 à 3.11 (recommandé) et pip installés.

```sh
pip install -r requirements.txt
```

### 2. **Lancer le programme**

```sh
python main_interactif.py
```

---

## 🎮 Utilisation

- **Recherche anime** : commence à taper le nom, choisis avec les flèches, valide avec Entrée.
- **Navigation** : sélectionne l’anime, la saison, puis l’épisode à l’aide du clavier.
- **Lecture** : l’épisode se lance automatiquement dans VLC.
- **Retour** : à chaque étape, choisis "Retour / Quitter" pour revenir en arrière ou relancer une recherche.

---

## 💡 Fonctionnalités

- **Recherche interactive** avec autocomplétion
- **Menus colorés** et logo ASCII art
- **Navigation fluide** entre animes, saisons et épisodes
- **Lecture sans pub** (lien direct extrait avec yt-dlp)
- **Support Windows (cmd, PowerShell, Windows Terminal)**

---

## 🖥️ Dépendances

- [prompt_toolkit]
- [colorama]
- [yt-dlp]
- [anime-sama-api] 

---

## ❓ FAQ

- **Q : Je vois des caractères bizarres au lieu des couleurs !**
  - Lance le script dans `cmd.exe` ou `Windows Terminal` (évite certains IDE).
- **Q : VLC ne se lance pas ?**
  - Vérifie le chemin de VLC dans le script (`C:\Program Files\VideoLAN\VLC\vlc.exe`).
- **Q : PyInstaller ne fonctionne pas avec Python 3.12+ ?**
  - Utilise Python 3.8 à 3.11 pour créer un exécutable, ou lance le script directement.

---

## 🤝 Contribuer

Les PR et suggestions sont les bienvenues !  
N’hésitez pas à ouvrir une issue ou à proposer une amélioration.

---

## 📝 Licence

MIT

---

