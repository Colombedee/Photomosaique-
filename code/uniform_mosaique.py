import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import coeur
import ajustements
import tkinter as tk
from tkinter import filedialog
from pillow_heif import register_heif_opener
register_heif_opener()


def demander_fichiers_etape_1():
    """
    Ouvre des fenêtres de sélection pour l'image source et la tuile.
    """
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    print("En attente de la sélection des fichiers...")
    cible = filedialog.askopenfilename(title="Étape 1 : Choisir l'image SOURCE (Fond)")
    tuile = filedialog.askopenfilename(title="Étape 1 : Choisir la TUILE UNIQUE (Motif)")

    root.destroy()
    return cible, tuile


def generer_comparatif_etape_1(image_cible_path=None, tuile_path=None, N=16):
    """
    Génère et sauvegarde les deux versions (RGB et LAB) en haute qualité.
    """

    # 0. Vérification / Sélection des fichiers
    if not image_cible_path or not tuile_path:
        image_cible_path, tuile_path = demander_fichiers_etape_1()

    if not image_cible_path or not tuile_path:
        print("Erreur : Aucun fichier sélectionné. Arrêt de l'étape 1.")
        return

    # 1. Chargement et préparation
    print(f"Chargement de la cible : {image_cible_path}")
    try:
        # Amélioration 1 : On convertit en float64 pour éviter les erreurs d'arrondi
        cible_np = np.array(Image.open(image_cible_path).convert('RGB')).astype(np.float64)

        # Amélioration 2 : Utilisation de Image.LANCZOS pour un redimensionnement très net
        tuile_pil = Image.open(tuile_path).convert('RGB')
        tuile_np = np.array(tuile_pil.resize((N, N), resample=Image.LANCZOS)).astype(np.float64)
    except Exception as e:
        print(f"Erreur lors de l'ouverture des images : {e}")
        return

    # 2. Découpage via le coeur
    blocs, nb_h, nb_w = coeur.decouper_image(cible_np, N)

    tuiles_rgb = []
    tuiles_lab = []

    print(f"Traitement de {len(blocs)} blocs...")

    # 3. Traitement
    for bloc in blocs:
        couleur_moyenne = coeur.calculer_couleur_moyenne(bloc)

        # Méthode RGB
        t_rgb = ajustements.ajustement_multiplication(tuile_np, couleur_moyenne)
        tuiles_rgb.append(t_rgb)

        # Méthode LAB
        t_lab = ajustements.ajustement_translation_lab(tuile_np, couleur_moyenne)
        tuiles_lab.append(t_lab)

    # 4. Assemblage
    # Amélioration 3 : On s'assure que les valeurs restent entre 0 et 255 (clip) avant l'assemblage final
    image_finale_rgb = np.clip(coeur.assembler_image(tuiles_rgb, nb_h, nb_w, N), 0, 255).astype(np.uint8)
    image_finale_lab = np.clip(coeur.assembler_image(tuiles_lab, nb_h, nb_w, N), 0, 255).astype(np.uint8)

    # --- MODIFICATIONS : NOMMAGE ET QUALITÉ ---

    # Extraction des noms sans extension
    nom_cible = os.path.splitext(os.path.basename(image_cible_path))[0]
    nom_tuile = os.path.splitext(os.path.basename(tuile_path))[0]
    base_nom = f"resultat_{nom_cible}_avec_{nom_tuile}_N{N}"

    # Conversion en images PIL
    img_rgb = Image.fromarray(image_finale_rgb)
    img_lab = Image.fromarray(image_finale_lab)

    # Sauvegarde en PNG (sans perte) pour pouvoir zoomer proprement
    img_rgb.save(f"{base_nom}_RGB.png", compress_level=1)
    img_lab.save(f"{base_nom}_LAB.png", compress_level=1)

    print(f"Sauvegardé : {base_nom}_RGB.png")
    print(f"Sauvegardé : {base_nom}_LAB.png")

    # 6. Affichage
    plt.figure(figsize=(14, 7))

    plt.subplot(1, 2, 1)
    plt.imshow(image_finale_rgb)
    plt.title(f"RGB (N={N}) - {nom_tuile}")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(image_finale_lab)
    plt.title(f"LAB (N={N}) - {nom_tuile}")
    plt.axis('off')

    plt.tight_layout()
    print("Affichage en cours... (Zoom possible dans la fenêtre)")
    plt.show()

def generer_exploration_teinte(image_cible_path=None, tuile_path=None, N=16, decalage_lab=(0, 30, 0)):
    """
    Exploration créative : applique une teinte forcée sur la tuile après ajustement LAB.
    decalage_lab = (dL, da, db) — ex: (0, 30, 0) pour forcer du rouge/magenta
    """
    if not image_cible_path or not tuile_path:
        image_cible_path, tuile_path = demander_fichiers_etape_1()

    if not image_cible_path or not tuile_path:
        print("Erreur : Aucun fichier sélectionné.")
        return

    print(f"Chargement : {image_cible_path}")
    try:
        cible_np = np.array(Image.open(image_cible_path).convert('RGB')).astype(np.float64)
        tuile_pil = Image.open(tuile_path).convert('RGB')
        tuile_np = np.array(tuile_pil.resize((N, N), resample=Image.LANCZOS)).astype(np.float64)
    except Exception as e:
        print(f"Erreur : {e}")
        return

    blocs, nb_h, nb_w = coeur.decouper_image(cible_np, N)
    print(f"Traitement de {len(blocs)} blocs avec teinte forcée {decalage_lab}...")

    from skimage import color as skcolor

    tuiles_rgb = []
    tuiles_lab = []

    for bloc in blocs:
        couleur_moyenne = coeur.calculer_couleur_moyenne(bloc)

        # Ajustement LAB normal
        t_lab = ajustements.ajustement_translation_lab(tuile_np, couleur_moyenne).astype(np.float64)

        # Teinte forcée : décalage sur les canaux LAB
        t_lab_teinte = skcolor.rgb2lab(t_lab / 255.0)
        t_lab_teinte[:, :, 0] += decalage_lab[0]
        t_lab_teinte[:, :, 1] += decalage_lab[1]
        t_lab_teinte[:, :, 2] += decalage_lab[2]
        t_teinte = np.clip(skcolor.lab2rgb(t_lab_teinte) * 255, 0, 255).astype(np.uint8)

        tuiles_rgb.append(ajustements.ajustement_multiplication(tuile_np, couleur_moyenne))
        tuiles_lab.append(t_teinte)

    image_finale_rgb = np.clip(coeur.assembler_image(tuiles_rgb, nb_h, nb_w, N), 0, 255).astype(np.uint8)
    image_finale_lab = np.clip(coeur.assembler_image(tuiles_lab, nb_h, nb_w, N), 0, 255).astype(np.uint8)

    nom_cible = os.path.splitext(os.path.basename(image_cible_path))[0]
    nom_tuile = os.path.splitext(os.path.basename(tuile_path))[0]
    base_nom = f"exploration_{nom_cible}_avec_{nom_tuile}_N{N}_teinte{decalage_lab}"

    Image.fromarray(image_finale_rgb).save(f"{base_nom}_RGB.png", compress_level=1)
    Image.fromarray(image_finale_lab).save(f"{base_nom}_LAB_teinte.png", compress_level=1)

    print(f"Sauvegardé : {base_nom}_RGB.png")
    print(f"Sauvegardé : {base_nom}_LAB_teinte.png")

    plt.figure(figsize=(14, 7))
    plt.subplot(1, 2, 1)
    plt.imshow(image_finale_rgb)
    plt.title(f"RGB normal (N={N})")
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(image_finale_lab)
    plt.title(f"LAB + teinte {decalage_lab} (N={N})")
    plt.axis('off')
    plt.tight_layout()
    plt.show()