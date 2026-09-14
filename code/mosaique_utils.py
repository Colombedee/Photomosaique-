import numpy as np
from skimage import color

def convertir_en_lab(image_rgb):
    """
    Convertit une image ou un bloc de l'espace RGB vers l'espace LAB.
    L'espace LAB est plus adapté à la perception humaine[cite: 34, 48].
    """
    # skimage attend des valeurs entre 0 et 1 pour la conversion
    return color.rgb2lab(image_rgb / 255.0)

def calculer_histogramme(bloc):
    hists = []
    for c in range(3):  # R, G, B séparément
        h, _ = np.histogram(bloc[:, :, c], bins=256, range=(0, 255))
        hists.append(h)
    return np.concatenate(hists)  # vecteur de 768 valeurs