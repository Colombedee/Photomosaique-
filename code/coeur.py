import numpy as np
from PIL import Image


def decouper_image(image_np, N):
    """
    Divise l'image cible en une grille de blocs de taille N x N[cite: 17].
    """
    h, w, _ = image_np.shape
    nb_blocs_h = h // N
    nb_blocs_w = w // N

    # On tronque l'image pour qu'elle soit parfaitement divisible par N
    image_tronquee = image_np[:nb_blocs_h * N, :nb_blocs_w * N]

    blocs = []
    for i in range(nb_blocs_h):
        for j in range(nb_blocs_w):
            bloc = image_tronquee[i * N:(i + 1) * N, j * N:(j + 1) * N]
            blocs.append(bloc)

    return blocs, nb_blocs_h, nb_blocs_w


def calculer_couleur_moyenne(bloc):
    """
    Calcule la couleur moyenne d'un bloc (RGB)[cite: 18, 31].
    """
    return np.mean(bloc, axis=(0, 1))


def assembler_image(liste_tuiles, nb_h, nb_w, N):
    """
    Recrée l'image finale en plaçant les tuiles côte à côte[cite: 24, 25].
    """
    image_finale = np.zeros((nb_h * N, nb_w * N, 3), dtype=np.uint8)

    idx = 0
    for i in range(nb_h):
        for j in range(nb_w):
            image_finale[i * N:(i + 1) * N, j * N:(j + 1) * N] = liste_tuiles[idx]
            idx += 1

    return image_finale