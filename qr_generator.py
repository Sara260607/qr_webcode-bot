import qrcode

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
        nom_fichier = f"qr_{nom.replace('https://', '').replace('/', '_')}.png"
        img.save(nom_fichier)
        return nom_fichier
    else:
        return img
