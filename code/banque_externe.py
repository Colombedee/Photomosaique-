import requests
import os

dossier = r"C:\Users\imanc\Downloads\Projet_Photomosaique\banque_externe"
os.makedirs(dossier, exist_ok=True)

for i in range(1000):
    url = f"https://picsum.photos/300/300?random={i}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            chemin = os.path.join(dossier, f"image_{i}.jpg")
            with open(chemin, 'wb') as f:
                f.write(r.content)
            print(f"Téléchargé : image_{i}.jpg")
        else:
            print(f"Erreur HTTP {r.status_code} pour image_{i}")
    except Exception as e:
        print(f"Erreur : {e}")