from photo_mosaique import generer_comparatif_etape_2
import os
import random
import tkinter as tk
from tkinter import filedialog

DOSSIER_IMG = r"C:\Users\imanc\Downloads\Projet_Photomosaique\img"
OUTPUT_PATH = r"C:\Users\imanc\Downloads\Projet_Photomosaique\resultats"

def mosaique_aleatoire(dossier_img=DOSSIER_IMG, output_path=OUTPUT_PATH, values_n=None):
    if values_n is None:
        values_n = [30]

    extensions = ('.png', '.jpg', '.jpeg', '.heic')
    toutes_images = [
        f for f in os.listdir(dossier_img)
        if f.lower().endswith(extensions) and not f.startswith("resultat_")
    ]

    cible = random.choice(toutes_images)
    cible_path = os.path.join(dossier_img, cible)
    print(f"Image cible choisie au hasard : {cible}")

    for n in values_n:
        generer_comparatif_etape_2(
            image_cible_path=cible_path,
            dossier_banque=dossier_img,
            N=n,
            output_path=output_path,
        )


def mosaique_manuelle(dossier_img=DOSSIER_IMG, output_path=OUTPUT_PATH, values_n=None):
    if values_n is None:
        values_n = [30]

    # Sélection de l'image cible
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    cible_path = filedialog.askopenfilename(title="Choisir l'image cible")
    root.destroy()

    if not cible_path:
        print("Aucune image sélectionnée.")
        return

    for n in values_n:
        generer_comparatif_etape_2(
            image_cible_path=cible_path,
            dossier_banque=dossier_img,
            N=n,
            output_path=output_path,
        )


if __name__ == "__main__":
    # Demander la taille
    choix_n = input("Entrez une taille N (ex: 30) ou appuyez sur Entrée pour garder N=30 : ").strip()
    try:
        N = int(choix_n) if choix_n else 30
    except ValueError:
        print("Valeur invalide, N=30 utilisé.")
        N = 30

    # Demander la banque
    banque = input("Banque externe ? (o/n) : ").strip().lower()
    dossier = r"C:\Users\imanc\Downloads\Projet_Photomosaique\banque_externe" if banque == 'o' else DOSSIER_IMG

    # Demander le mode
    mode = input("Choisir l'image manuellement ? (o/n) : ").strip().lower()
    if mode == 'o':
        mosaique_manuelle(dossier_img=dossier, values_n=[N])
    else:
        mosaique_aleatoire(dossier_img=dossier, values_n=[N])