from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from qr_generator import generer_qr_code
import os

# ✅ Le token est maintenant pris depuis les variables d'environnement (idéal pour Railway)
import os
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🎉 Bienvenue !\n\n"
        "Envoie-moi le lien du site web que tu veux transformer en QR code.\n"
        "Exemple : exemple.com\n\n"
        "Le QR code te sera envoyé en fichier téléchargeable (format PNG)."
    )

def handle_message(update: Update, context: CallbackContext):
    url = update.message.text.strip()
    
    if not url:
        update.message.reply_text("❌ Tu dois envoyer un lien valide.\nExemple : https://exemple.com ou juste exemple.com")
        return

    # Ajoute https:// s’il n’est pas présent
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        file_path = generer_qr_code(url, url, save_local=True)
        with open(file_path, 'rb') as qr_file:
            update.message.reply_document(
                document=InputFile(qr_file),
                filename=os.path.basename(file_path),
                caption=f"📎 QR Code pour : {url}",
                parse_mode="Markdown"
            )
        os.remove(file_path)
    except Exception as e:
        update.message.reply_text(f"⚠️ Une erreur est survenue : {e}")

    update.message.reply_text("Tu peux envoyer un autre lien si tu veux 😊")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
