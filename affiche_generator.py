from PIL import Image, ImageDraw, ImageFont
import qrcode
import requests
from io import BytesIO
import os

def generer_affiche(url, save_local=False):
    # Exemple simple : affiche avec un QR code et texte
    qr = qrcode.make(url)
    qr = qr.resize((200, 200))

    # Créer une image blanche
    img = Image.new('RGB', (600, 400), color='white')
    draw = ImageDraw.Draw(img)

    # Télécharger une image à partir du site (exemple, facultatif)
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        site_img = Image.open(BytesIO(response.content)).resize((350, 350))
        img.paste(site_img, (10, 25))
    except Exception:
        # si échec, on laisse blanc
        pass

    # Coller le QR code
    img.paste(qr, (380, 100))

    # Texte d’accroche
    font = ImageFont.load_default()
    draw.text((380, 320), "Venez découvrir notre site !", fill="black", font=font)
    draw.text((380, 340), "Scanner le QR code pour visiter.", fill="black", font=font)

    if save_local:
        file_name = "affiche.png"
        img.save(file_name)
        return file_name
    else:
        return img
