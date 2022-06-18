"""
обработка команды /start
"""

from telethon import events


@tlgbot.on(events.NewMessage(chats=tlgbot.settings.get_all_user_id(), pattern='/start'))
async def start_cmd_plugin(event):
    await event.respond(
        "Сәлам!\nБу телеграмм ботында сүзне татар теленнән рус теленә тәрҗемә итәргә ярдәм итәчәк һәм киресенчә.\nСүз "
        "генә кертегез һәм нинди телгә тәрҗемә итәргә кирәклеген сайлагыз.\n\n")
    await event.respond(
        "Привет!\nЭтот телеграмм бот который поможет перевести слово с татарского языка на русский язык и "
        "наоборот.\nВведите слово и выберите на какой язык нужно перевести.\n\n")
