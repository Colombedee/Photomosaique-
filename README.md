# 🖼️ Photomosaïque

**Reconstruction d'images par mosaïque uniforme et vraie photomosaïque**

Projet réalisé en Python dans le cadre du cours **GIF-4105/7105 Photographie Algorithmique**, Université Laval (Hiver 2026).

🔗 **[Voir le site du projet](https://colombedee.github.io/Photomosaique-/)**

---

## 👥 Équipe

- Colombe Diallo
- Tadagbé Dhossou

---

## 📌 Description

Ce projet explore deux techniques de reconstruction d'images à partir de tuiles :

1. **Mosaïque uniforme**: une image cible est recréée à partir d'une seule image miniaturisée, ajustée en couleur pour chaque bloc.
2. **Vraie photomosaïque**: chaque bloc de l'image cible est remplacé par l'image la plus similaire provenant d'une banque de plus de 1000 images.

Le projet compare également l'impact de différents **espaces colorimétriques** (RGB vs LAB) et **critères de correspondance** (couleur moyenne vs histogramme) sur la qualité visuelle du résultat.

---

## ⚙️ Fonctionnalités

- Découpage d'une image cible en blocs N×N pixels
- Ajustement colorimétrique par multiplication (RGB) ou translation (LAB)
- Recherche de correspondance dans une banque d'images via KDTree
- Comparaison de critères : couleur moyenne (RGB/LAB) et intersection d'histogrammes
- Limitation des répétitions de tuiles pour plus de diversité visuelle
- Exploration créative : teintes forcées, mosaïques hybrides N&B/couleur

---

## 🛠️ Technologies

- **Langage** : Python
- **Structures** : KDTree (scipy) pour la recherche de correspondance rapide
- **Interface** : site web HTML/CSS/JS pour la présentation des résultats

---

## 📂 Structure du dépôt

Photomosaique-/

├── index.html # Site de présentation du projet

├── images/ # Images utilisées (cibles, tuiles, résultats)

├── code/ # Code source Python

└── presentation.pdf # Document de présentation du projet


---

## 📊 Résultats clés

- **LAB > RGB** pour la fidélité colorimétrique perceptuelle
- **Couleur moyenne > histogramme** pour la cohérence visuelle globale
- Une banque d'images diversifiée améliore significativement la qualité de la photomosaïque
- Compromis fondamental entre taille des tuiles (N) et lisibilité vs précision

---

## 🎓 Contexte académique

Projet final réalisé sous la supervision de **M. Yannick Hold-Geoffroy**, cours GIF-4105/7105 Photographie Algorithmique, Université Laval, Hiver 2026.
