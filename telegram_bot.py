import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import asyncio
import time

# Токен вашего бота
TOKEN = '7614444281:AAFjFqQCdNGkS7FyRkePCsSZKeVXUuUrOts'
# Числовой ID канала @game_flick
CHANNEL_ID = '-1001881210308'
TECH_CHANNEL = '@game_flick2'

# Словарь игр: ключ — параметр из ссылки, значение — ID поста в @game_flick2
GAMES = {
    'plancon': 32,
    'extremecar': 24,
    'coverfire': 25,
    'brightmemory': 26,
    'lineage2m': 27,
    'rocketleague': 28,
    'arenabreakout': 29,
    'doorkickers': 30,
    'asphalt8': 31,
    'sfg3': 33,
    'darkanddarker': 34,
    'cozytown': 35,
    'demolitionderby2': 36,
    'simcitybuildit': 37,
    'stuntbikeextreme': 38,
    'zakz': 39,
    'warsmash': 40,
    'stormhillmystery': 41
}

# Создаём приложение бота
application = Application.builder().token(TOKEN).build()

# Функция обработки команды /start
async def start(update, context):
    chat_id = update.message.chat_id
    game = context.args[0] if context.args else None
    if game:
        context.user_data['game'] = game.lower()
    await send_subscribe_button(update, context)

# Функция проверки подписки на канал
async def check_subscription(context, user_id):
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except telegram.error.BadRequest:
        return False

# Функция отправки сообщения с кнопкой подписки
async def send_subscribe_button(update, context):
    keyboard = [
        [InlineKeyboardButton("Подписаться", url="https://t.me/game_flick")],
        [InlineKeyboardButton("Проверить подписку", callback_data="check")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_photo(
        chat_id=update.message.chat_id,
        photo='https://t.me/game_flick2/23',
        caption="Чтобы скачать игру, подпишись на канал @game_flick!",
        reply_markup=reply_markup
    )

# Функция отправки ссылки на скачивание
async def send_download_button(update, context):
    game = context.user_data.get('game')
    chat_id = update.effective_chat.id if update.message is None else update.message.chat_id
    if game and game in GAMES:
        post_id = GAMES[game]
        url = f"https://t.me/{TECH_CHANNEL[1:]}/{post_id}"
        keyboard = [[InlineKeyboardButton("Скачать игру", url=url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Спасибо за подписку! Вот твоя ссылка на скачивание ({game}):",
            reply_markup=reply_markup
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Игра не найдена. Выбери игру на сайте: https://gameflick.netlify.app"
        )

# Обработка нажатий на кнопки
async def button_handler(update, context):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if query.data == "check":
        if await check_subscription(context, user_id):
            await send_download_button(update, context)
        else:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="Ты ещё не подписан на @game_flick. Подпишись и попробуй снова!"
            )

# Добавляем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_handler))

# Основной цикл запуска с перезапуском
def run_bot():
    while True:
        try:
            print("Бот запущен!")
            application.run_polling(allowed_updates=telegram.Update.ALL_TYPES)
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(60)  # Ждём 1 минуту перед перезапуском

if __name__ == '__main__':
    run_bot()  # Запускаем бот с перезапуском