import telegram
from telegram.ext import Application, CommandHandler

# Токен вашего бота
TOKEN = "5893751467:AAF74HJ9JET_I14pkkQSr8toE6zkVTRiDhk"

async def start(update, context):
    print("Команда /start получена от пользователя:", update.message.from_user.id)
    await update.message.reply_text("Бот работает! Введите /test для проверки.")
    print("Ответ отправлен пользователю:", update.message.from_user.id)

async def test_command(update, context):
    print("Команда /test получена от пользователя:", update.message.from_user.id)
    await update.message.reply_text("Тест успешен!")
    print("Ответ отправлен пользователю:", update.message.from_user.id)

def main():
    print("Бот запускается с токеном:", TOKEN)
    try:
        application = Application.builder().token(TOKEN).build()
        print("Application успешно создан")
    except telegram.error.InvalidToken:
        print("Ошибка: Неверный токен")
        return
    except Exception as e:
        print(f"Ошибка при создании Application: {e}")
        return
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("test", test_command))
    print("Бот успешно инициализирован, ожидание команд...")
    application.run_polling()

if __name__ == "__main__":
    main()
