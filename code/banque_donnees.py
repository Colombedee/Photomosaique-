import os
import hashlib
import pickle
import numpy as np
from PIL import Image
from scipy.spatial import KDTree
from skimage import color as skcolor
from pillow_heif import register_heif_opener
register_heif_opener()
import mosaique_utils


def _signature_dossier(dossier, N):
    """Produit une signature unique basée sur les fichiers du dossier et N."""
    fichiers = sorted(f for f in os.listdir(dossier) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.heic')))
    contenu = f"N={N}|" + "|".join(
        f"{f}:{os.path.getmtime(os.path.join(dossier, f))}" for f in fichiers
    )
    return hashlib.md5(contenu.encode()).hexdigest()


class BanqueImages:
    def __init__(self, dossier_images, N, dossier_cache=None):
        self.N = N
        self.images_redimensionnees = []
        self.moyennes_rgb = []
        self.histogrammes = []
        self.moyennes_lab = []

        cache_charge = False
        if dossier_cache is not None:
            cache_charge = self._charger_cache(dossier_images, dossier_cache)

        if not cache_charge:
            self._charger_banque(dossier_images)
            if dossier_cache is not None:
                self._sauvegarder_cache(dossier_images, dossier_cache)

        self.tree = KDTree(self.moyennes_rgb)
        self.tree_lab = KDTree(self.moyennes_lab)
        self._histogrammes_array = np.array(self.histogrammes)

    def _chemin_cache(self, dossier_images, dossier_cache):
        sig = _signature_dossier(dossier_images, self.N)
        os.makedirs(dossier_cache, exist_ok=True)
        return os.path.join(dossier_cache, f"banque_{sig}.pkl")

    def _charger_cache(self, dossier_images, dossier_cache):
        chemin = self._chemin_cache(dossier_images, dossier_cache)
        if os.path.isfile(chemin):
            print(f"Banque chargée depuis le cache ({chemin})")
            with open(chemin, 'rb') as f:
                data = pickle.load(f)
            self.images_redimensionnees = data['images']
            self.moyennes_rgb = data['moyennes']
            self.moyennes_lab = data['moyennes_lab']
            self.histogrammes = data['histogrammes']
            return True
        return False

    def _sauvegarder_cache(self, dossier_images, dossier_cache):
        chemin = self._chemin_cache(dossier_images, dossier_cache)
        with open(chemin, 'wb') as f:
            pickle.dump({
                'images':      self.images_redimensionnees,
                'moyennes':    self.moyennes_rgb,
                'moyennes_lab': self.moyennes_lab,
                'histogrammes': self.histogrammes,
            }, f)
        print(f"Banque mise en cache : {chemin}")

    def _charger_banque(self, dossier):
        fichiers = [f for f in os.listdir(dossier) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        print(f"Chargement de {len(fichiers)} images...")

        for nom in fichiers:
            chemin = os.path.join(dossier, nom)
            try:
                img = Image.open(chemin).convert('RGB').resize((self.N, self.N), resample=Image.LANCZOS)
                img_np = np.array(img)
                self.images_redimensionnees.append(img_np)
                self.moyennes_rgb.append(np.mean(img_np, axis=(0, 1)))
                img_lab = skcolor.rgb2lab(img_np / 255.0)
                self.moyennes_lab.append(np.mean(img_lab, axis=(0, 1)))
                self.histogrammes.append(mosaique_utils.calculer_histogramme(img_np))
            except Exception as e:
                print(f"Erreur sur {nom}: {e}")

    def trouver_plus_proche_couleur(self, couleur_cible):
        _, index = self.tree.query(couleur_cible)
        return self.images_redimensionnees[index]

    def trouver_plus_proche_histogramme(self, hist_cible):
        scores = np.sum(np.minimum(hist_cible, self._histogrammes_array), axis=1)
        return self.images_redimensionnees[np.argmax(scores)]

    def trouver_batch_couleur(self, couleurs):
        _, indices = self.tree.query(couleurs)
        return [self.images_redimensionnees[i] for i in indices]

    def trouver_batch_histogramme(self, histogrammes, chunk_size=128):
        """Intersection d'histogrammes par chunks pour éviter les débordements mémoire."""
        histos = np.array(histogrammes, dtype=np.float32)
        banque = self._histogrammes_array.astype(np.float32)
        indices = np.empty(len(histos), dtype=np.int32)

        for debut in range(0, len(histos), chunk_size):
            chunk = histos[debut:debut + chunk_size]
            scores = np.minimum(chunk[:, None, :], banque[None, :, :]).sum(axis=2)
            indices[debut:debut + chunk_size] = np.argmax(scores, axis=1)

        return [self.images_redimensionnees[i] for i in indices]

    def trouver_batch_couleur_lab(self, blocs):
        moyennes = []
        for b in blocs:
            lab = skcolor.rgb2lab(b / 255.0)
            moyennes.append(np.mean(lab, axis=(0, 1)))
        _, indices = self.tree_lab.query(moyennes)
        return [self.images_redimensionnees[i] for i in indices]


