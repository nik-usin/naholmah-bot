import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Настройки
BOT_TOKEN = "8781534240:AAHmbhPE2cKWTOSKuzMQNp19ZIfzk5dGKjc"
ADMIN_ID = 5585749093
SITE_URL = "https://t.me/naholmah_studio_bot"

logging.basicConfig(level=logging.INFO)

# Хранилище пользователей ожидающих ответа
waiting_reply = {}  # {admin_message_id: user_chat_id}

# Главное меню
def main_menu():
    keyboard = [
        ["🏠 Наши студии", "📅 Забронировать"],
        ["💬 Написать нам", "❓ Помощь"],
        ["🌐 Перейти на сайт"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"👋 Привет, {user.first_name}!\n\n"
        f"🏠 Добро пожаловать в студии *«На холмах»*\n\n"
        f"Мы предлагаем уютные студии для посуточной аренды в ЖК «Изумрудные холмы», Красногорск.\n\n"
        f"Выберите что вас интересует 👇"
    )
    await update.message.reply_text(text, reply_markup=main_menu(), parse_mode="Markdown")

# Студии
async def studios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛋 Студия 1 — Уютная", callback_data="studio_1")],
        [InlineKeyboardButton("🏙 Студия 2 — Современная", callback_data="studio_2")],
        [InlineKeyboardButton("💎 Студия 3 — Премиум", callback_data="studio_3")],
        [InlineKeyboardButton("📅 Забронировать", url=f"{SITE_URL}/studios")],
    ]
    await update.message.reply_text(
        "🏠 *Наши студии*\n\nВыберите студию для просмотра:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# Инфо о студиях
STUDIOS_INFO = {
    "studio_1": {
        "name": "Студия 1 — Уютная",
        "desc": (
            "📐 Площадь: 23 м²\n"
            "👥 До 3 гостей\n"
            "🏢 Этаж: 2 из 25\n\n"
            "✨ Удобства:\n"
            "🛋 Диван-кровать + раскладной пуфик\n"
            "📺 Wink TV\n"
            "🌐 Wi-Fi\n"
            "🍳 Варочная панель\n"
            "❄️ Холодильник\n"
            "👕 Стиральная машина\n"
            "🔑 Электронный замок\n\n"
            "💰 От 5 000 ₽/сутки"
        )
    },
    "studio_2": {
        "name": "Студия 2 — Современная",
        "desc": (
            "📐 Площадь: 20 м²\n"
            "👥 До 2 гостей\n"
            "🏢 Этаж: 2 из 25\n\n"
            "✨ Удобства:\n"
            "🛏 Откидная двуспальная кровать\n"
            "📺 Wink TV\n"
            "🌐 Wi-Fi\n"
            "🍳 Варочная панель\n"
            "❄️ Холодильник\n"
            "👕 Стиральная машина\n"
            "🔑 Электронный замок\n\n"
            "💰 От 6 500 ₽/сутки"
        )
    },
    "studio_3": {
        "name": "Студия 3 — Премиум",
        "desc": (
            "📐 Площадь: 26 м²\n"
            "👥 До 4 гостей\n"
            "🏢 Этаж: 2 из 25\n\n"
            "✨ Удобства:\n"
            "🛏 Двуспальная кровать + диван-кровать\n"
            "📺 Wink TV\n"
            "🌐 Wi-Fi\n"
            "🍳 Варочная панель\n"
            "❄️ Холодильник\n"
            "👕 Стиральная машина\n"
            "🔑 Электронный замок\n\n"
            "💰 От 9 000 ₽/сутки"
        )
    }
}

async def studio_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    studio = STUDIOS_INFO.get(query.data)
    if studio:
        keyboard = [[
            InlineKeyboardButton("📅 Забронировать", url=f"{SITE_URL}/studios"),
            InlineKeyboardButton("◀️ Назад", callback_data="back_studios")
        ]]
        await query.edit_message_text(
            f"🏠 *{studio['name']}*\n\n{studio['desc']}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

async def back_studios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🛋 Студия 1 — Уютная", callback_data="studio_1")],
        [InlineKeyboardButton("🏙 Студия 2 — Современная", callback_data="studio_2")],
        [InlineKeyboardButton("💎 Студия 3 — Премиум", callback_data="studio_3")],
        [InlineKeyboardButton("📅 Забронировать", url=f"{SITE_URL}/studios")],
    ]
    await query.edit_message_text(
        "🏠 *Наши студии*\n\nВыберите студию для просмотра:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# Написать нам
async def contact_us(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_message"] = True
    await update.message.reply_text(
        "💬 *Напишите ваше сообщение*\n\n"
        "Мы ответим вам в ближайшее время!\n"
        "Можете задать любой вопрос 👇",
        parse_mode="Markdown"
    )

# Помощь / FAQ
async def help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("❓ Как забронировать?", callback_data="faq_book")],
        [InlineKeyboardButton("💳 Как оплатить?", callback_data="faq_pay")],
        [InlineKeyboardButton("🔑 Как заселиться?", callback_data="faq_checkin")],
        [InlineKeyboardButton("📅 Минимальный срок?", callback_data="faq_mindays")],
        [InlineKeyboardButton("🐾 Можно с животными?", callback_data="faq_pets")],
        [InlineKeyboardButton("🚗 Есть парковка?", callback_data="faq_parking")],
        [InlineKeyboardButton("🌐 Перейти на сайт", url=SITE_URL)],
    ]
    await update.message.reply_text(
        "❓ *Часто задаваемые вопросы*\n\nВыберите вопрос:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

FAQ_ANSWERS = {
    "faq_book": "📅 *Как забронировать?*\n\n1. Зайдите на сайт\n2. Выберите студию\n3. Нажмите «Забронировать»\n4. Выберите даты (мин. 2 ночи)\n5. Заполните форму\n6. Дождитесь подтверждения",
    "faq_pay": "💳 *Как оплатить?*\n\nОплата после подтверждения брони:\n• СБП по номеру телефона\n• Перевод на карту\n\nРеквизиты на сайте в разделе «Оплата»",
    "faq_checkin": "🔑 *Как заселиться?*\n\nЗаезд с 14:00. На двери электронный замок — код пришлём после оплаты. Выезд до 12:00.",
    "faq_mindays": "📅 *Минимальный срок?*\n\nМинимальный срок бронирования — 2 ночи.",
    "faq_pets": "🐾 *Можно с животными?*\n\nПроживание с питомцами только по предварительному согласованию. Напишите нам заранее.",
    "faq_parking": "🚗 *Есть парковка?*\n\nДа! Бесплатные места на поверхности рядом с домом. Также есть подземный паркинг (платно).",
}

async def faq_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    answer = FAQ_ANSWERS.get(query.data, "Ответ не найден")
    keyboard = [[InlineKeyboardButton("◀️ Назад к вопросам", callback_data="back_faq")]]
    await query.edit_message_text(
        answer,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def back_faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("❓ Как забронировать?", callback_data="faq_book")],
        [InlineKeyboardButton("💳 Как оплатить?", callback_data="faq_pay")],
        [InlineKeyboardButton("🔑 Как заселиться?", callback_data="faq_checkin")],
        [InlineKeyboardButton("📅 Минимальный срок?", callback_data="faq_mindays")],
        [InlineKeyboardButton("🐾 Можно с животными?", callback_data="faq_pets")],
        [InlineKeyboardButton("🚗 Есть парковка?", callback_data="faq_parking")],
        [InlineKeyboardButton("🌐 Перейти на сайт", url=SITE_URL)],
    ]
    await query.edit_message_text(
        "❓ *Часто задаваемые вопросы*\n\nВыберите вопрос:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    # Кнопки меню
    if text == "🏠 Наши студии":
        await studios(update, context)
        return
    elif text == "📅 Забронировать":
        keyboard = [[InlineKeyboardButton("📅 Открыть сайт", url=f"{SITE_URL}/studios")]]
        await update.message.reply_text(
            "📅 *Бронирование*\n\nДля бронирования перейдите на наш сайт:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return
    elif text == "💬 Написать нам":
        await contact_us(update, context)
        return
    elif text == "❓ Помощь":
        await help_menu(update, context)
        return
    elif text == "🌐 Перейти на сайт":
        keyboard = [[InlineKeyboardButton("🌐 Открыть сайт", url=SITE_URL)]]
        await update.message.reply_text(
            f"🌐 Наш сайт: {SITE_URL}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # Если пользователь ждёт отправки сообщения
    if context.user_data.get("waiting_message"):
        context.user_data["waiting_message"] = False

        # Пересылаем сообщение админу
        admin_msg = await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"📨 *Новое сообщение от пользователя*\n\n"
                f"👤 Имя: {user.full_name}\n"
                f"🆔 ID: `{user.id}`\n"
                f"🔗 Username: @{user.username or 'нет'}\n\n"
                f"💬 Сообщение:\n{text}\n\n"
                f"_Ответьте на это сообщение чтобы отправить ответ пользователю_"
            ),
            parse_mode="Markdown"
        )
        waiting_reply[admin_msg.message_id] = user.id

        await update.message.reply_text(
            "✅ Сообщение отправлено! Мы ответим вам в ближайшее время.",
            reply_markup=main_menu()
        )
        return

    # Если это ответ админа на сообщение пользователя
    if user.id == ADMIN_ID and update.message.reply_to_message:
        replied_id = update.message.reply_to_message.message_id
        user_chat_id = waiting_reply.get(replied_id)
        if user_chat_id:
            await context.bot.send_message(
                chat_id=user_chat_id,
                text=f"💬 *Ответ от администратора:*\n\n{text}",
                parse_mode="Markdown",
                reply_markup=main_menu()
            )
            await update.message.reply_text("✅ Ответ отправлен пользователю!")
            return

    # Обычное сообщение
    await update.message.reply_text(
        "Выберите действие из меню 👇",
        reply_markup=main_menu()
    )

# Уведомление о новой брони (вызывается с сайта)
async def notify_new_booking(bot, booking_data: dict):
    text = (
        f"🔔 *Новая бронь!*\n\n"
        f"🏠 Студия: {booking_data.get('studio_name')}\n"
        f"👤 Гость: {booking_data.get('user_name')}\n"
        f"📞 Телефон: {booking_data.get('phone')}\n"
        f"📅 Заезд: {booking_data.get('check_in')}\n"
        f"📅 Выезд: {booking_data.get('check_out')}\n"
        f"👥 Гостей: {booking_data.get('guests')}\n"
        f"💰 Сумма: {booking_data.get('total_price')} ₽\n"
    )
    if booking_data.get('comment'):
        text += f"💬 Комментарий: {booking_data.get('comment')}\n"
    await bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(studio_callback, pattern="^studio_"))
    app.add_handler(CallbackQueryHandler(back_studios, pattern="^back_studios$"))
    app.add_handler(CallbackQueryHandler(faq_callback, pattern="^faq_"))
    app.add_handler(CallbackQueryHandler(back_faq, pattern="^back_faq$"))

    print("🤖 Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()