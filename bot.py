import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

PRODUCTS = {
    "iphone": {"name": "iPhone 15 Pro 256GB", "price": "15 000 000 so'm"},
    "samsung": {"name": "Samsung S24 Ultra", "price": "13 000 000 so'm"},
    "redmi": {"name": "Redmi Note 13 Pro", "price": "3 500 000 so'm"}
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("📱 Махсулотлар", callback_data="products")],
        [InlineKeyboardButton("📞 Админ", callback_data="admin")]
    ]
    await update.message.reply_text("🛍 Almaz Shop ga xush kelibsiz!", reply_markup=InlineKeyboardMarkup(kb))

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "products":
        kb = []
        for k, v in PRODUCTS.items():
            kb.append([InlineKeyboardButton(f"{v['name']} - {v['price']}", callback_data=f"p_{k}")])
        kb.append([InlineKeyboardButton("⬅️ Оркага", callback_data="back")])
        await q.edit_message_text("📱 Махсулотлар:", reply_markup=InlineKeyboardMarkup(kb))
    elif q.data.startswith("p_"):
        k = q.data[2:]
        p = PRODUCTS[k]
        kb = [[InlineKeyboardButton("⬅️ Оркага", callback_data="products")]]
        await q.edit_message_text(f"📦 {p['name']}\n💰 {p['price']}\n\nБуюртма учун @almazshop_admin га ёзинг!", reply_markup=InlineKeyboardMarkup(kb))
    elif q.data == "admin":
        kb = [[InlineKeyboardButton("⬅️ Оркага", callback_data="back")]]
        await q.edit_message_text("📞 Админ: @almazshop_admin\nТел: +998901234567", reply_markup=InlineKeyboardMarkup(kb))
    elif q.data == "back":
        kb = [
            [InlineKeyboardButton("📱 Махсулотлар", callback_data="products")],
            [InlineKeyboardButton("📞 Админ", callback_data="admin")]
        ]
        await q.edit_message_text("🛍 Almaz Shop ga xush kelibsiz!", reply_markup=InlineKeyboardMarkup(kb))

def main():
    if not TOKEN:
        print("TOKEN yo'q!")
        return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
