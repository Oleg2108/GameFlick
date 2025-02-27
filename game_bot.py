import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
from bs4 import BeautifulSoup
import subprocess
import os

# Токен вашего бота
TOKEN = "5893751467:AAF74HJ9JET_I14pkkQSr8toE6zkVTRiDhk"

# Состояния разговора для добавления
ADD_PAGE, ADD_TITLE, ADD_DESC, ADD_LINK, ADD_IMAGE, ADD_GENRE, ADD_CONFIRM = range(7)
# Состояния разговора для замены
REP_PAGE, REP_OLD, REP_TITLE, REP_DESC, REP_LINK, REP_IMAGE, REP_GENRE, REP_CONFIRM = range(8)

async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Добавить игру на сайт", callback_data="add")],
        [InlineKeyboardButton("Заменить игру на сайте", callback_data="replace")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)
    return ConversationHandler.END

async def button_handler(update, context):
    query = update.callback_query
    await query.answer()
    
    if query.data == "add":
        await query.edit_message_text("На какую страницу добавить игру? (например, index, page2, page3):")
        return ADD_PAGE
    elif query.data == "replace":
        await query.edit_message_text("На какой странице заменить игру? (например, index, page2, page3):")
        return REP_PAGE
    return ConversationHandler.END

# Добавление игры
async def add_page(update, context):
    context.user_data["page"] = update.message.text.lower()
    await update.message.reply_text("Введите название игры:")
    return ADD_TITLE

async def add_title(update, context):
    context.user_data["title"] = update.message.text
    await update.message.reply_text("Введите описание игры (до 400 символов):")
    return ADD_DESC

async def add_desc(update, context):
    desc = update.message.text
    if len(desc) > 400:
        await update.message.reply_text("Описание слишком длинное (более 400 символов). Введите короче:")
        return ADD_DESC
    context.user_data["description"] = desc
    await update.message.reply_text("Введите ссылку на скачивание:")
    return ADD_LINK

async def add_link(update, context):
    context.user_data["link"] = update.message.text
    await update.message.reply_text("Введите ссылку на изображение (или 'пропустить' для стандартного):")
    return ADD_IMAGE

async def add_image(update, context):
    image = update.message.text
    if image.lower() == "пропустить":
        context.user_data["image"] = "https://via.placeholder.com/300"
    else:
        context.user_data["image"] = image
    await update.message.reply_text("Введите жанр игры (или 'пропустить' для 'Неизвестно'):")
    return ADD_GENRE

async def add_genre(update, context):
    genre = update.message.text
    if genre.lower() == "пропустить":
        context.user_data["genre"] = "Неизвестно"
    else:
        context.user_data["genre"] = genre
    
    game = context.user_data
    await update.message.reply_text(
        f"Проверьте данные:\n"
        f"Страница: {game['page']}\n"
        f"Название: {game['title']}\n"
        f"Описание: {game['description']}\n"
        f"Ссылка: {game['link']}\n"
        f"Изображение: {game['image']}\n"
        f"Жанр: {game['genre']}\n"
        f"Всё верно? (да/нет)"
    )
    return ADD_CONFIRM

async def add_confirm(update, context):
    if update.message.text.lower() == "да":
        game = context.user_data
        add_game_to_page(game["page"], game)
        update_site()
        await update.message.reply_text(f"Игра '{game['title']}' добавлена на {game['page']}.html и опубликована на сайте!")
    else:
        await update.message.reply_text("Добавление отменено. Начните заново с /start.")
    return ConversationHandler.END

# Замена игры
async def rep_page(update, context):
    context.user_data["page"] = update.message.text.lower()
    await update.message.reply_text("Введите название или номер игры, которую хотите заменить:")
    return REP_OLD

async def rep_old(update, context):
    context.user_data["old_game"] = update.message.text
    await update.message.reply_text("Введите новое название игры:")
    return REP_TITLE

async def rep_title(update, context):
    context.user_data["title"] = update.message.text
    await update.message.reply_text("Введите новое описание игры (до 400 символов):")
    return REP_DESC

async def rep_desc(update, context):
    desc = update.message.text
    if len(desc) > 400:
        await update.message.reply_text("Описание слишком длинное (более 400 символов). Введите короче:")
        return REP_DESC
    context.user_data["description"] = desc
    await update.message.reply_text("Введите новую ссылку на скачивание:")
    return REP_LINK

async def rep_link(update, context):
    context.user_data["link"] = update.message.text
    await update.message.reply_text("Введите новую ссылку на изображение (или 'пропустить' для стандартного):")
    return REP_IMAGE

async def rep_image(update, context):
    image = update.message.text
    if image.lower() == "пропустить":
        context.user_data["image"] = "https://via.placeholder.com/300"
    else:
        context.user_data["image"] = image
    await update.message.reply_text("Введите новый жанр игры (или 'пропустить' для 'Неизвестно'):")
    return REP_GENRE

async def rep_genre(update, context):
    genre = update.message.text
    if genre.lower() == "пропустить":
        context.user_data["genre"] = "Неизвестно"
    else:
        context.user_data["genre"] = genre
    
    game = context.user_data
    await update.message.reply_text(
        f"Проверьте данные для замены:\n"
        f"Страница: {game['page']}\n"
        f"Заменяемая игра: {game['old_game']}\n"
        f"Новое название: {game['title']}\n"
        f"Новое описание: {game['description']}\n"
        f"Новая ссылка: {game['link']}\n"
        f"Новое изображение: {game['image']}\n"
        f"Новый жанр: {game['genre']}\n"
        f"Всё верно? (да/нет)"
    )
    return REP_CONFIRM

async def rep_confirm(update, context):
    if update.message.text.lower() == "да":
        game = context.user_data
        replace_game_on_page(game["page"], game["old_game"], game)
        update_site()
        await update.message.reply_text(f"Игра '{game['old_game']}' заменена на '{game['title']}' на {game['page']}.html и опубликована на сайте!")
    else:
        await update.message.reply_text("Замена отменена. Начните заново с /start.")
    return ConversationHandler.END

def add_game_to_page(page, game):
    with open(f"{page}.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, "html.parser")
    container = soup.select_one(".games-container")
    current_games = len(container.find_all("article"))
    new_id = current_games + 1
    
    game_div = soup.new_tag("article", **{"class": "game"})
    img = soup.new_tag("img", src=game["image"], alt=f"Скриншот игры {game['title']}", **{"loading": "lazy"})
    h3 = soup.new_tag("h3")
    h3.string = f"{new_id}. {game['title']}"
    p_genre = soup.new_tag("p", **{"class": "genre"})
    p_genre.string = f"Жанр: {game['genre']}"
    p_desc = soup.new_tag("p")
    p_desc.string = game["description"]
    div_rating = soup.new_tag("div", **{"class": "rating"})
    div_rating.string = "★★★★☆ (4.0/5)"
    a = soup.new_tag("a", href=game["link"], target="_blank", **{"data-game": game["title"]})
    a.string = "Скачать"
    
    game_div.append(img)
    game_div.append(h3)
    game_div.append(p_genre)
    game_div.append(p_desc)
    game_div.append(div_rating)
    game_div.append(a)
    container.append(game_div)
    
    with open(f"{page}.html", "w", encoding="utf-8") as file:
        file.write(str(soup))

def replace_game_on_page(page, old_game, new_game):
    with open(f"{page}.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, "html.parser")
    games = soup.select(".game")
    
    for game_div in games:
        h3 = game_div.find("h3").text
        if old_game in h3 or old_game == h3.split(".")[0].strip():
            game_div.clear()
            img = soup.new_tag("img", src=new_game["image"], alt=f"Скриншот игры {new_game['title']}", **{"loading": "lazy"})
            h3_tag = soup.new_tag("h3")
            h3_tag.string = h3  # Сохраняем старый номер
            p_genre = soup.new_tag("p", **{"class": "genre"})
            p_genre.string = f"Жанр: {new_game['genre']}"
            p_desc = soup.new_tag("p")
            p_desc.string = new_game["description"]
            div_rating = soup.new_tag("div", **{"class": "rating"})
            div_rating.string = "★★★★☆ (4.0/5)"
            a = soup.new_tag("a", href=new_game["link"], target="_blank", **{"data-game": new_game["title"]})
            a.string = "Скачать"
            
            game_div.append(img)
            game_div.append(h3_tag)
            game_div.append(p_genre)
            game_div.append(p_desc)
            game_div.append(div_rating)
            game_div.append(a)
            break
    
    with open(f"{page}.html", "w", encoding="utf-8") as file:
        file.write(str(soup))

def update_site():
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Обновление игры через бота"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Сайт обновлён через Git!")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при обновлении сайта через Git: {e}")

def main():
    application = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CallbackQueryHandler(button_handler)],
        states={
            # Добавление
            ADD_PAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_page)],
            ADD_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_title)],
            ADD_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_desc)],
            ADD_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_link)],
            ADD_IMAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_image)],
            ADD_GENRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_genre)],
            ADD_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_confirm)],
            # Замена
            REP_PAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, rep_page)],
            REP_OLD: [MessageHandler(filters.TEXT & ~filters.COMMAND, rep_old)],
            REP_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, rep_title)],
            REP_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, rep_desc)],
            REP_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, rep_link)],
            REP_IMAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, rep_image)],
            REP_GENRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, rep_genre)],
            REP_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, rep_confirm)]
        },
        fallbacks=[]
    )
    
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()