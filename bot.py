from telegram import (
    Update,
    InputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler
)
from qr_generator import generer_qr_code
from affiche_generator import generer_affiche
import validators
import json
import os
from datetime import datetime

# Récupère les variables d’environnement (utilisé par Railway)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

LOG_FILE = 'user_logs.json'

def log_user_action(user, url, action):
    log_entry = {
        "user_id": user.id,
        "username": user.username if user.username else "None",
        "first_name": user.first_name if user.first_name else "None",
        "url": url,
        "action": action,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    logs.append(log_entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

def start(update: Update, context: CallbackContext):
    welcome_text = (
        "🎉 *Bienvenue !*\n\n"
        "Envoie-moi le lien du site web que tu souhaites transformer en QR code ou en affiche.\n\n"
        "Exemple : `https://exemple.com` ou simplement `exemple.com`\n\n"
        "_⚠️ En utilisant ce bot, tu acceptes que tes données (nom, identifiant Telegram, lien généré) "
        "soient enregistrées pour des raisons de sécurité._\n"
    )
    update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN
    )

def handle_message(update: Update, context: CallbackContext):
    url = update.message.text.strip()
    user = update.message.from_user

    if not validators.url(url) and not validators.domain(url):
        update.message.reply_text(
            "❌ Le lien envoyé n'est pas valide.\n"
            "Exemple de lien valide : `https://exemple.com` ou juste `exemple.com`\n\n"
            "Merci d'envoyer un lien correct.\n\n"
            "👉 Choisis ensuite :\n"
            "1️⃣ *QR code simple*\n"
            "2️⃣ *Belle affiche avec QR code et résumé du site* 🌐",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    context.user_data['url'] = url
    log_user_action(user, url, "lien reçu")

    keyboard = [
        [
            InlineKeyboardButton("1️⃣ QR code simple", callback_data='qr_simple'),
            InlineKeyboardButton("2️⃣ Belle affiche", callback_data='affiche'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Que souhaites-tu générer ?",
        reply_markup=reply_markup
    )

def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    url = context.user_data.get('url')

    if not url:
        query.answer()
        query.edit_message_text("❌ Aucun lien trouvé dans la session, envoie un lien d'abord.")
        return

    query.answer()

    try:
        if query.data == 'qr_simple':
            log_user_action(user, url, "QR code simple généré")
            file_path = generer_qr_code(url, url, save_local=True)
            with open(file_path, 'rb') as qr_file:
                query.edit_message_text(f"Voici ton QR code pour : {url}")
                query.message.reply_document(document=InputFile(qr_file), filename=os.path.basename(file_path))
            os.remove(file_path)

        elif query.data == 'affiche':
            log_user_action(user, url, "Affiche générée")
            file_path = generer_affiche(url, save_local=True)
            with open(file_path, 'rb') as affiche_file:
                query.edit_message_text(f"Voici ton affiche avec QR code et résumé pour : {url}")
                query.message.reply_document(document=InputFile(affiche_file), filename=os.path.basename(file_path))
            os.remove(file_path)
    except Exception as e:
        query.edit_message_text(f"⚠️ Une erreur est survenue : {e}")

def send_logs(update: Update, context: CallbackContext):
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'rb') as f:
                update.message.reply_document(document=f, filename="user_logs.json")
        else:
            update.message.reply_text("Aucun fichier de logs trouvé.")
    except Exception as e:
        update.message.reply_text(f"Erreur lors de la lecture des logs : {e}")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("logs", send_logs))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CallbackQueryHandler(button_callback))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
