import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

PRODUCTS = {
    "iphone": {"name": "iPhone 15 Pro 256GB", "price": "1200$"},
    "samsung": {"name": "Samsung S24 Ultra", "price": "1100$"},
    "redmi": {"name": "Redmi Note 13 Pro", "price": "350$"}
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("📱 Махсулотлар", callback_data="products")],
        [InlineKeyboardButton("📞 Админ", callback_data="contact")]
    ]
    await update.message.reply_text("🛍️ Almaz Shop га хуш келибсиз!\n\nМахсулот танланг:", reply_markup=InlineKeyboardMarkup(kb))

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "products":
        kb = [[InlineKeyboardButton(f"{v['name']} - {v['price']}", callback_data=f"p_{k}")] for k,v in PRODUCTS.items()]
        kb.append([InlineKeyboardButton("⬅️ Оркага", callback_data="back")])
        await q.edit_message_text("📱 Махсулотлар:", reply_markup=InlineKeyboardMarkup(kb))
    elif q.data.startswith("p_"):
        k = q.data[2:]
        p = PRODUCTS[k]
        kb = [[InlineKeyboardButton("✅ Буюртма бериш", callback_data=f"buy_{k}")],[InlineKeyboardButton("⬅️ Оркага", callback_data="products")]]
        await q.edit_message_text(f"📱 {p['name']}\n💰 {p['price']}\n\nБуюртма берасизми?", reply_markup=InlineKeyboardMarkup(kb))
    elif q.data.startswith("buy_"):
        await q.edit_message_text("✅ Буюртма кабул килинди!\nТелефон номерингизни ёзинг, админ богланади!")
    elif q.data == "contact":
        await q.edit_message_text("📞 Админ: @almazshopaziz\nТез орада жавоб берамиз!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Оркага", callback_data="back")]]))
    elif q.data == "back":
        kb = [[InlineKeyboardButton("📱 Махсулотлар", callback_data="products")],[InlineKeyboardButton("📞 Админ", callback_data="contact")]]
        await q.edit_message_text("🛍️ Almaz Shop", reply_markup=InlineKeyboardMarkup(kb))

async def msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Рахмат! {update.message.text}\nАдминга юборилди!")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg))
    app.run_polling()

if __name__ == "__main__":
    main()
