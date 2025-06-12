import qrcode
import re

def generer_qr_code(nom, data, save_local=False):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    if save_local:
        # Nettoie le nom pour créer un nom de fichier valide
        nom_nettoye = re.sub(r'[^a-zA-Z0-9]', '_', nom)
        file_name = f"qr_{nom_nettoye}.png"
        img.save(file_name)
        return file_name
    else:
        return img
