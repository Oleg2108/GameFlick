from telegram import Bot
from telegram.ext import Application, CommandHandler

TOKEN = '7614444281:AAFjFqQCdNGkS7FyRkePCsSZKeVXUuUrOts'  # Ваш токен
SUBSCRIBE_CHANNEL = '@game_flick'  # Канал для подписки
TECH_CHANNEL = '@game_flick2'     # Технический канал

# Словарь игр и ID постов в @game_flick2
GAMES = {
    'plancon': 20,       # Plancon: Space Conflict
    'extremecar': 21,    # Extreme Car Driving Simulator
    'coverfire': 22      # Cover Fire: Offline Shooting
    # Добавьте остальные игры с сайта
}

async def start(update, context):
    chat_id = update.message.chat_id
    game = context.args[0] if context.args else None

    try:
        member = await context.bot.get_chat_member(SUBSCRIBE_CHANNEL, chat_id)
        if member.status in ['member', 'administrator', 'creator']:
            if game and game.lower() in GAMES:
                post_id = GAMES[game.lower()]
                await context.bot.send_message(chat_id=chat_id, text=f"Вы подписаны! Вот ваша игра в {TECH_CHANNEL}: https://t.me/{TECH_CHANNEL[1:]}/{post_id}")
            else:
                await context.bot.send_message(chat_id=chat_id, text="Выберите игру на сайте: https://gameflick.netlify.app")
        else:
            await context.bot.send_message(chat_id=chat_id, text=f"Подпишитесь на {SUBSCRIBE_CHANNEL}, чтобы скачать игру!\nПосле подписки нажмите /start {game} снова.")
    except telegram.error.BadRequest:
        await context.bot.send_message(chat_id=chat_id, text=f"Подпишитесь на {SUBSCRIBE_CHANNEL}, чтобы скачать игру!\nПосле подписки нажмите /start {game} снова.")

def main():
    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()