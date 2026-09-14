import numpy as np
from skimage import color


def ajustement_multiplication(tuile, couleur_bloc_rgb):
    """
    Méthode 1 : Ajustement par multiplication (Espace RGB).
    Ratio = couleur_bloc / couleur_tuile
    """
    # Calcul de la couleur moyenne de la tuile originale
    couleur_tuile_rgb = np.mean(tuile, axis=(0, 1))

    # Éviter la division par zéro
    couleur_tuile_rgb[couleur_tuile_rgb == 0] = 1

    # Calcul du ratio pour chaque canal (R, G, B)
    ratio = couleur_bloc_rgb / couleur_tuile_rgb

    # Application du ratio et limitation des valeurs entre 0 et 255
    tuile_ajustee = np.clip(tuile * ratio, 0, 255).astype(np.uint8)

    return tuile_ajustee


def ajustement_translation_lab(tuile_rgb, couleur_bloc_rgb):
    """
    Méthode 2 : Ajustement par translation dans l'espace LAB. [cite: 23]
    Plus précis pour la perception humaine.
    """
    # 1. Conversion de la tuile et de la couleur cible en LAB
    tuile_lab = color.rgb2lab(tuile_rgb / 255.0)
    couleur_bloc_lab = color.rgb2lab(couleur_bloc_rgb.reshape(1, 1, 3) / 255.0).reshape(3)

    # 2. Calcul de la couleur moyenne de la tuile en LAB
    moyenne_tuile_lab = np.mean(tuile_lab, axis=(0, 1))

    # 3. Calcul de la différence (translation)
    diff = couleur_bloc_lab - moyenne_tuile_lab

    # 4. Application de la translation sur les canaux L, A, et B [cite: 23]
    tuile_lab_ajustee = tuile_lab + diff

    # 5. Reconversion vers RGB pour l'affichage
    tuile_rgb_ajustee = color.lab2rgb(tuile_lab_ajustee) * 255

    return np.clip(tuile_rgb_ajustee, 0, 255).astype(np.uint8)