"""
    демонстрация кнопок внутри сообщений
"""
import os

from telethon import events, Button
import requests
from codecs import escape_decode  # type: ignore
import urllib.parse
import datetime
from bs4 import BeautifulSoup


def string_escape(s: str, encoding: str = "utf-8") -> str:
    """
    преобразование строки вида "SAMSUNG a50 64\\xd0\\xb3\\xd0\\xb1" в строку c кодировкой encoding
    """
    byte_s = bytes(s, encoding)
    res = escape_decode(byte_s)[0]
    res = res.decode(encoding)
    return res


def translate_rus2tat(word: str = ""):
    """
    перевод из русского на татарский
    """
    url_rus_to_tat = "https://translate.tatar/translate?lang=0&text="
    word: str = urllib.parse.quote(word)
    s = requests.Session()
    r = s.get(f"{url_rus_to_tat}{word}")
    return string_escape(str(r.content))


def translate_tat2rus(word: str = ""):
    """
    перевод из татарского на русский
    """
    url_rus_to_tat = "https://translate.tatar/translate?lang=1&text="
    word: str = urllib.parse.quote(word)
    s = requests.Session()
    r = s.get(f"{url_rus_to_tat}{word}")
    return string_escape(str(r.content))


@tlgbot.on(events.NewMessage(chats=tlgbot.settings.get_all_user_id(), pattern=''))
async def word_cmd_plugin(event):
    word = event.raw_text

    if word.find("/start") >= 0:
        return

    tek_date = datetime.datetime.now()
    sender_id = event.sender_id

    namefile_tmp = f"{tek_date}{sender_id}.txt"
    path = os.path.join("result", namefile_tmp)
    print("path = ", path)

    if not os.path.exists("result"):
        os.mkdir("result")

    with open(path, "w") as f:
        f.write(word)
        button_main_cmd = [
            [Button.inline("русский", data=f"tat2rus {path}"),
             Button.inline("татарский", data=f"rus2tat {path}")]]
        await event.respond(f"Выбери на какой язык перевести слово {word}", buttons=button_main_cmd)


def prettify_result(result):
    res = dict()

    index_res = result.find("<res>")
    if index_res == -1:
        return result[2:-1]

    soup = BeautifulSoup(result, "html.parser")

    tmp = soup.select_one("responseType")
    res["responseType"] = tmp.text if tmp else None

    tmp = soup.select_one("word")
    res["word"] = tmp.text if tmp else None

    tmp = soup.select_one("pos")
    res["pos"] = tmp.text if tmp else None

    tmp = soup.select("translation")
    tmp_list = []
    for val in tmp:
        tmp_list.append(val.text)

    res["translation"] = tmp_list

    tmp = soup.select("examples")
    tmp_list = []
    for val in tmp:
        tmp_list.append(val.text)
    res["examples"] = tmp_list

    tmp = soup.select_one("mt")
    res["mt"] = tmp.text if tmp else None

    return res


def format_result(text_dict):
    """
    {'responseType': '1',
    'word': 'дару',
    'pos': 'сущ',
    'translation': ['лекарство, медикамент // лекарственный', 'перен средство, способ'],
    'examples': [''],
    'mt': 'лекарство'}

    """
    trans = ""
    example = ""
    if type(text_dict) == str:
        return text_dict

    for val in text_dict['translation']:
        trans += "* " + val + "\n"

    for val in text_dict['examples']:
        if len(val.strip()):
            example += "* " + val + "\n"

    if len(example):

        result = f"""{text_dict['word']}  ->  {text_dict['mt']}

Сүзлек:
часть речи: {text_dict['pos']}
{trans}

Примеры:
{example}        
    """
    else:
        result = f"""{text_dict['word']}  ->  {text_dict['mt']}

Сүзлек:
часть речи: {text_dict['pos']}
{trans}
        """

    return result


@tlgbot.on(events.CallbackQuery)
async def translate_cmd(event):
    result = ""
    s = event.data.decode("utf-8").strip()
    print("s = ", s)
    data = s[:s.index(" ")].strip()
    path = s[s.index(" ") + 1:]
    print("event.data = ", data)
    if data == "tat2rus":
        with open(path, "r") as f:
            word = f.read()
            result = translate_tat2rus(word)
            await event.edit(
                f"{format_result(prettify_result(result))}")

    if data == "rus2tat":
        with open(path, "r") as f:
            word = f.read()
            result = translate_rus2tat(word)
            # result = prettify_result(result)
            await event.edit(
                f"{format_result(prettify_result(result))}")

    os.remove(path)
