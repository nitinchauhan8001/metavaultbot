import os
import threading
import time
import json
import random
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode  # Use enum for parse modes

# === Bot Credentials ===
API_ID = 25089395
API_HASH = "ee3bc5af4a3109cbcc2edb6dd54b206a"
BOT_TOKEN = "8032993341:AAHKPcx-Z5qfIkHBs1R_vuAqh1E5BLpKzII"

# === Channel and Admin Info ===
CHANNEL_USERNAME = "MetaaVault"  # Public channel for updates
ADMIN_USERNAME = "NITINGURJAR800800"  # Admin link for requests

# === Delete Locked Session File ===
if os.path.exists("Metavaults_bot.session"):
    os.remove("Metavaults_bot.session")

# === Load Movies Data from JSON File ===
def load_movies_data():
    try:
        with open("movies.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            print("✅ Movies Loaded Successfully!")
            return data
    except Exception as e:
        print("Error loading movies.json:", e)
        return []

movies_data = load_movies_data()

# === Initialize Bot ===
app = Client("Metavaults_bot",
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN)

# === Flask Server for Uptime (Optional) ===
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Bot is running on your Desktop!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

# Uncomment these lines if you want to run Flask for uptime monitoring:
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()
time.sleep(2)

# === /test Command for Inline Keyboard Testing ===
@app.on_message(filters.command("test"))
def test_keyboard(client, message):
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("Test Button", url="https://example.com")]])
    # Use enum value for parse_mode
    message.reply_text("Testing Keyboard", reply_markup=kb, parse_mode=ParseMode.MARKDOWN)

# === /start Command Handler (Welcome Message + Dashboard) ===
@app.on_message(filters.command("start"))
def start(client, message):
    welcome_text = (
        "<b>✨ Welcome to Metavaults Bot! ✨</b>\n\n"
        "<b>Movies & Web Series</b>\n"
        "Enjoy the latest movies and web series curated just for you.\n\n"
        "<b>Education</b>\n"
        "Access a wide range of educational resources including Sample Papers and Study Material for Classes 1 to 12.\n\n"
        "<b>Earn Money Online</b>\n"
        "Discover exciting online earning opportunities. Get in touch with our admin for details.\n\n"
        "Explore the dashboard below to get started.\n\n"
        "<b>🚀 Developed by Nitin Chauhan</b>"
    )
    client.send_message(message.chat.id, welcome_text, parse_mode=ParseMode.HTML, reply_markup=main_menu_keyboard())

# === Main Menu Inline Keyboard (Dashboard) ===
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Bollywood Movies", callback_data="bollywood"),
         InlineKeyboardButton("👶 Kids", callback_data="kids")],
        [InlineKeyboardButton("📺 Hollywood", callback_data="hollywood"),
         InlineKeyboardButton("🎭 Web Series", callback_data="web_series")],
        [InlineKeyboardButton("🙏 Devotional", callback_data="devotional"),
         InlineKeyboardButton("🌍 Regional", callback_data="regional")],
        [InlineKeyboardButton("🎥 Trending Movies", callback_data="trending"),
         InlineKeyboardButton("💡 Surprise Me!", callback_data="surprise")],
        [InlineKeyboardButton("🔍 Search Movie", callback_data="search")],
        [InlineKeyboardButton("📩 Request Movie", url="https://t.me/NITINGURJAR800800")],
        [InlineKeyboardButton("📚 Education", callback_data="education")],
        [InlineKeyboardButton("💰 Earn Money Online", callback_data="earn_money")],
        [InlineKeyboardButton("👍 Facebook", url="https://www.facebook.com/share/1F6MqUMUDz/"),
         InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/chitra.manthan?igsh=MW5nMDJtNjRubTFwdw==")]
    ])

# === Utility: Check Channel Membership (For Movie Sections) ===
def is_channel_member(client, user_id):
    try:
        member = client.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ["left", "kicked"]:
            return False
        return True
    except Exception as e:
        print("Membership check error:", e)
        return False

# === Utility: Send Movie Details ===
def send_movie_details(client, chat_id, movie):
    if not is_channel_member(client, user_id=chat_id):
        client.send_message(chat_id, f"Please join our channel: https://t.me/{CHANNEL_USERNAME}", parse_mode=ParseMode.MARKDOWN)
        return
    try:
        client.send_document(chat_id, movie["file_id"])
    except Exception as e:
        client.send_message(chat_id, "Error sending movie file.", parse_mode=ParseMode.MARKDOWN)
        print("Error sending file:", e)
        return
    warning_text = "Please use the file for personal use only."
    client.send_message(chat_id, f"{movie['description']}\n\n{warning_text}", parse_mode=ParseMode.MARKDOWN)

# === Callback Handlers for Movie Categories ===

@app.on_callback_query(filters.regex("^bollywood$"))
def bollywood_handler(client, callback_query):
    buttons = []
    for movie in movies_data:
        if movie.get("category", "").lower() == "bollywood":
            buttons.append([InlineKeyboardButton(movie["title"], callback_data=f"movie_{movie['id']}")])
    if not buttons:
        callback_query.answer("No Bollywood movies available.", show_alert=True)
        return
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_main")])
    callback_query.message.edit_text("Select a Bollywood movie:", parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("^kids$"))
def kids_handler(client, callback_query):
    buttons = []
    for movie in movies_data:
        if movie.get("category", "").lower() == "kids":
            buttons.append([InlineKeyboardButton(movie["title"], callback_data=f"movie_{movie['id']}")])
    if not buttons:
        callback_query.answer("No Kids movies available.", show_alert=True)
        return
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_main")])
    callback_query.message.edit_text("Select a Kids movie:", parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("^regional$"))
def regional_handler(client, callback_query):
    languages = set()
    for movie in movies_data:
        if movie.get("category", "").lower() == "regional" and movie.get("language"):
            languages.add(movie["language"].capitalize())
    if not languages:
        callback_query.answer("No Regional movies available.", show_alert=True)
        return
    buttons = []
    for lang in sorted(languages):
        buttons.append([InlineKeyboardButton(lang, callback_data=f"regional_{lang.lower()}")])
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_main")])
    callback_query.message.edit_text("Select a regional language:", parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("^regional_"))
def regional_language_handler(client, callback_query):
    lang = callback_query.data.split("_")[1]
    buttons = []
    for movie in movies_data:
        if movie.get("category", "").lower() == "regional" and movie.get("language", "").lower() == lang:
            buttons.append([InlineKeyboardButton(movie["title"], callback_data=f"movie_{movie['id']}")])
    if not buttons:
        callback_query.answer(f"No {lang.capitalize()} movies available.", show_alert=True)
        return
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="regional")])
    callback_query.message.edit_text(f"{lang.capitalize()} Movies:", parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("^web_series$"))
def web_series_handler(client, callback_query):
    buttons = []
    for movie in movies_data:
        if movie.get("category", "").lower() == "web series":
            buttons.append([InlineKeyboardButton(movie["title"], callback_data=f"movie_{movie['id']}")])
    if not buttons:
        callback_query.answer("No Web Series available.", show_alert=True)
        return
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_main")])
    callback_query.message.edit_text("Select a Web Series:", parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("hollywood"))
def hollywood_handler(client, callback_query):
    callback_query.answer("Hollywood - Coming Soon!", show_alert=True)

@app.on_callback_query(filters.regex("devotional"))
def devotional_handler(client, callback_query):
    callback_query.answer("Devotional - Coming Soon!", show_alert=True)

@app.on_callback_query(filters.regex("poll"))
def poll_handler(client, callback_query):
    callback_query.answer("Vote: Favorite Movies - Coming Soon!", show_alert=True)

@app.on_callback_query(filters.regex("theme"))
def theme_handler(client, callback_query):
    callback_query.answer("Theme toggle - Coming Soon!", show_alert=True)

# === Trending Movies Handler ===
@app.on_callback_query(filters.regex("^trending$"))
def trending_handler(client, callback_query):
    try:
        messages = client.get_history(CHANNEL_USERNAME, limit=3)
        if not messages:
            callback_query.answer("No trending movies found.", show_alert=True)
            return
        text = "🎥 <b>Latest Trending Movies</b>:\n\n"
        for msg in messages:
            text += f"- <a href='https://t.me/{CHANNEL_USERNAME}/{msg.message_id}'>Movie Link</a>\n"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]])
        callback_query.message.edit_text(text, disable_web_page_preview=True, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    except Exception as e:
        callback_query.answer("Error fetching trending movies.", show_alert=True)
        print("Trending error:", e)

@app.on_callback_query(filters.regex("^surprise$"))
def surprise_handler(client, callback_query):
    if movies_data:
        movie = random.choice(movies_data)
        callback_query.answer("Surprise Movie!", show_alert=True)
        send_movie_details(client, callback_query.message.chat.id, movie)
    else:
        callback_query.answer("No movies available for surprise.", show_alert=True)

@app.on_callback_query(filters.regex("^search$"))
def search_instruction_handler(client, callback_query):
    callback_query.answer("Search Movies", show_alert=True)
    callback_query.message.reply_text(
        "Use the command:\n\n/searchmovie <movie name>\n\nExample: /searchmovie Inception",
        parse_mode=ParseMode.HTML
    )

@app.on_message(filters.command("searchmovie"))
def search_movie(client, message):
    if len(message.command) < 2:
        message.reply_text("Usage: /searchmovie <movie name>", parse_mode=ParseMode.MARKDOWN)
        return
    query = " ".join(message.command[1:]).lower()
    print(f"Search query: {query}")
    results = [movie for movie in movies_data if query in movie.get("title", "").lower()]
    if not results:
        message.reply_text("No movies found matching your query.", parse_mode=ParseMode.MARKDOWN)
        return
    buttons = []
    for movie in results:
        buttons.append([InlineKeyboardButton(movie["title"], callback_data=f"movie_{movie['id']}")])
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_main")])
    message.reply_text("Search Results:", parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(buttons))

# === Education Section Handlers ===

@app.on_callback_query(filters.regex("^education$"))
def education_handler(client, callback_query):
    buttons = []
    for i in range(1, 13):
        buttons.append([InlineKeyboardButton(f"Class {i}", callback_data=f"education_{i}")])
    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_main")])
    callback_query.message.edit_text("Select your Class for Education:", parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("^education_\\d+$"))
def education_class_handler(client, callback_query):
    class_num = callback_query.data.split("_")[1]
    buttons = [
        [InlineKeyboardButton("Sample Papers", callback_data=f"edu_{class_num}_sample")],
        [InlineKeyboardButton("Study Material", callback_data=f"edu_{class_num}_study")],
        [InlineKeyboardButton("🔙 Back", callback_data="education")],
        [InlineKeyboardButton("Contact Admin", url="https://t.me/NITINGURJAR800800")]
    ]
    callback_query.message.edit_text(f"Class {class_num} Education Resources:", parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("^edu_\\d+_(sample|study)$"))
def education_request_handler(client, callback_query):
    parts = callback_query.data.split("_")
    class_num = parts[1]
    req_type = parts[2]
    resource = "Sample Papers" if req_type == "sample" else "Study Material"
    callback_query.answer(f"This content is paid (Rs 500 per month).", show_alert=True)
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("Contact Admin", url="https://t.me/NITINGURJAR800800")],
        [InlineKeyboardButton("🔙 Back", callback_data="education")]
    ])
    callback_query.edit_message_reply_markup(reply_markup=kb)

# === Earn Money Online Section Handler ===

@app.on_callback_query(filters.regex("^earn_money$"))
def earn_money_handler(client, callback_query):
    callback_query.answer("Earn Money Online", show_alert=True)
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("Contact Admin", url="https://t.me/NITINGURJAR800800")]])
    callback_query.message.reply_text(
        "Please contact the admin for Earn Money Online opportunities.",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb
    )

@app.on_message(filters.command("earnmoney"))
def earnmoney(client, message):
    if len(message.command) < 2:
        message.reply_text("Usage: /earnmoney <your details> | <your email> | <your phone>", parse_mode=ParseMode.MARKDOWN)
        return
    full_text = message.text[len("/earnmoney "):].strip()
    parts = full_text.split("|")
    if len(parts) < 3:
        message.reply_text("Usage: /earnmoney <your details> | <your email> | <your phone>", parse_mode=ParseMode.MARKDOWN)
        return
    details = parts[0].strip()
    email = parts[1].strip()
    phone = parts[2].strip()
    admin_message = (
        f"Earn Money Online Request:\n"
        f"Details: {details}\n"
        f"Email: {email}\n"
        f"Phone: {phone}\n"
        f"User: {message.from_user.first_name} (@{message.from_user.username}) - ID: {message.from_user.id}"
    )
    try:
        client.send_message(ADMIN_USERNAME, admin_message, parse_mode=ParseMode.MARKDOWN)
        message.reply_text("Your Earn Money Online request has been sent!", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        message.reply_text("Error sending your request. Please try again later.", parse_mode=ParseMode.MARKDOWN)
        print("Earn money error:", e)

# === Back to Main Menu Handler ===
@app.on_callback_query(filters.regex("back_to_main"))
def back_to_main_handler(client, callback_query):
    callback_query.message.edit_text("Welcome back! Choose an option:", parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu_keyboard())

# === Movie Selection Handler ===
@app.on_callback_query(filters.regex("^movie_"))
def movie_selection_handler(client, callback_query):
    try:
        movie_id = int(callback_query.data.split("_")[1])
        movie = next((m for m in movies_data if m.get("id") == movie_id), None)
        if not movie:
            callback_query.answer("Movie not found.", show_alert=True)
            return
        callback_query.answer(f"Selected: {movie['title']}", show_alert=True)
        send_movie_details(client, callback_query.message.chat.id, movie)
    except Exception as e:
        callback_query.answer("Error processing movie selection.", show_alert=True)
        print("Movie selection error:", e)

# === Start the Bot ===
print("✅ Bot is running...")
app.run()