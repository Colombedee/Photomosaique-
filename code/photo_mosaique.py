import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import coeur
import mosaique_utils
from banque_donnees import BanqueImages


def _appliquer_critere(blocs, banque, critere):
    if critere == 'couleur':
        moyennes = np.array([coeur.calculer_couleur_moyenne(b) for b in blocs])
        return banque.trouver_batch_couleur(moyennes)
    elif critere == 'couleur_lab':
        return banque.trouver_batch_couleur_lab(blocs)
    else:
        histos = [mosaique_utils.calculer_histogramme(b) for b in blocs]
        return banque.trouver_batch_histogramme(histos)

def generer_etape_2(image_cible_path, dossier_banque, N, critere='couleur', output_path=None, banque=None):
    """
    Crée une photomosaïque complète.
    Passer banque= pour réutiliser une banque déjà chargée et éviter de la recharger.
    critere : 'couleur' (KDTree, rapide) ou 'histogramme' (intersection, précis)
    """
    cible_np = np.array(Image.open(image_cible_path).convert('RGB'))

    if banque is None:
        banque = BanqueImages(dossier_banque, N)

    blocs, nb_h, nb_w = coeur.decouper_image(cible_np, N)
    total = len(blocs)
    print(f"Recherche ({total} blocs, critère: {critere})...")

    tuiles = _appliquer_critere(blocs, banque, critere)

    # Visualisation : on part de l'image cible et on remplace les blocs progressivement
    nom_cible = os.path.splitext(os.path.basename(image_cible_path))[0]
    resultat_np = cible_np[:nb_h * N, :nb_w * N].copy()

    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axis('off')
    ax.set_title(f"{nom_cible} — image originale")
    im = ax.imshow(resultat_np)
    plt.tight_layout()
    plt.pause(1.0)

    rafraichissement = max(1, total // 10)  # 5 mises à jour au total
    for idx, tuile in enumerate(tuiles):
        i, j = idx // nb_w, idx % nb_w
        resultat_np[i*N:(i+1)*N, j*N:(j+1)*N] = tuile

        if (idx + 1) % rafraichissement == 0 or idx == total - 1:
            im.set_data(resultat_np)
            ax.set_title(f"{nom_cible} — N={N} — {critere} ({idx+1}/{total})")
            fig.canvas.draw()
            fig.canvas.flush_events()

    plt.ioff()
    plt.show()

    nom_fichier = f"photomosaique_{nom_cible}_N{N}_{critere}.png"
    chemin_sortie = os.path.join(output_path, nom_fichier) if output_path else nom_fichier
    if output_path:
        os.makedirs(output_path, exist_ok=True)
    Image.fromarray(resultat_np).save(chemin_sortie, compress_level=1)
    print(f"Sauvegardé : {chemin_sortie}")

    return resultat_np

def generer_comparatif_etape_2(image_cible_path, dossier_banque, N=16, output_path=None):
    print(f"\n=== Photomosaïque N={N} — chargement de la banque... ===")
    banque = BanqueImages(dossier_banque, N, dossier_cache="../cache")

    generer_etape_2(image_cible_path, dossier_banque, N, 'couleur',     output_path, banque)
    generer_etape_2(image_cible_path, dossier_banque, N, 'couleur_lab', output_path, banque)
    generer_etape_2(image_cible_path, dossier_banque, N, 'histogramme', output_path, banque)