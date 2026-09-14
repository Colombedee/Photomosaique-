import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import coeur
import ajustements
from uniform_mosaique import demander_fichiers_etape_1

if __name__ == "__main__":
    # 1. Configuration
    choix_n = input("Entrez une taille N (ex: 20) : ").strip()
    N = int(choix_n) if choix_n else 20

    # 2. Sélection des fichiers
    cible_path, tuile_path = demander_fichiers_etape_1()

    if cible_path and tuile_path:
        # 3. Chargement des images
        cible_np = np.array(Image.open(cible_path).convert('RGB')).astype(np.float64)
        tuile_np = np.array(Image.open(tuile_path).convert('RGB').resize((N, N), resample=Image.LANCZOS)).astype(
            np.float64)

        # 4. Découpage de l'image cible
        blocs, nb_h, nb_w = coeur.decouper_image(cible_np, N)

        # 5. Définition des teintes RGB (Multiplicateurs : Rouge, Vert, Bleu)
        teintes = {
            "Normal": (1.0, 1.0, 1.0),  # Pas de modification
            "Bleu_Doux": (0.8, 0.85, 1.15),  # Teinte bleutée
            "Jaune_Solaire": (1.15, 1.1, 0.8),  # Teinte jaune/dorée
            "Rouge_Chaud": (1.15, 0.85, 0.85)  # Teinte rouge
        }

        for nom, mult in teintes.items():
            print(f"Traitement de la variante : {nom}...")
            tuiles_teintees = []

            for bloc in blocs:
                couleur_moy = coeur.calculer_couleur_moyenne(bloc)

                # On récupère le résultat de l'ajustement en float64 pour le calcul
                t_ajustee = ajustements.ajustement_multiplication(tuile_np, couleur_moy).astype(np.float64)

                # Application du multiplicateur (1.0 partout pour le "Normal")
                t_ajustee[:, :, 0] *= mult[0]
                t_ajustee[:, :, 1] *= mult[1]
                t_ajustee[:, :, 2] *= mult[2]

                # On clip et on repasse en uint8
                tuiles_teintees.append(np.clip(t_ajustee, 0, 255).astype(np.uint8))

            # 6. Assemblage et Sauvegarde
            image_finale = coeur.assembler_image(tuiles_teintees, nb_h, nb_w, N)
            image_finale = np.clip(image_finale, 0, 255).astype(np.uint8)

            res_path = f"Resultat_RGB_{nom}_{N}.png"
            Image.fromarray(image_finale).save(res_path)
            print(f"Sauvegardé : {res_path}")

        print("\nBravo ! Toutes tes variantes (incluant la normale) sont prêtes.")