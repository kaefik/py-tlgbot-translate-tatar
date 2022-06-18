О проекте

**py-tlgbot-translate-tatar** - телеграмм бот который реализует интерфейс к переводчику https://translate.tatar/ с татарского языка на русский и обратно.

## Настройка проекта для запуска

### Библиотеки:

```bash
pip install Telethon # для самого бота
pip3 install requests
pip3 install bs4
```

### Конфигурационные файлы проекта:

* **cfg/config_tlg.py** - за основу можно взять файл config_tlg_example.py

  ```
    # здесь указывается переменные для запуска телеграмм бота
    TLG_APP_NAME = "tlgbotappexample"  # APP NAME get from https://my.telegram.org
    TLG_APP_API_ID = 1258887  # APP API ID get from https://my.telegram.org
    TLG_APP_API_HASH = "sdsadsadasd45522665f"  # APP API HASH get from https://my.telegram.org
    I_BOT_TOKEN = "0000000000:sfdfdsfsdf5s5541sd2f1sd5"  # TOKEN Bot from BotFather
    TLG_ADMIN_ID_CLIENT = [1258889]  # admin clients for admin telegram bot
    # proxy for Telegram
    TLG_PROXY_SERVER = None  # address MTProxy Telegram
    TLG_PROXY_PORT = None  # port  MTProxy Telegram
    TLG_PROXY_KEY = None  # secret key  MTProxy Telegram
    # for save settings user
    # CSV - сохранение данных настроек для доступа к боту используя БД в формате CSV
    # SQLITE - сохранение данных настроек для доступа к боту используя БД в формате sqlite3
    TYPE_DB = "SQLITE"
  ```

Параметром **TYPE_DB** можно выбрать сохранять настройки с помощью sqlite3 или в файле csv (бывает полезно когда по
каким-то причинам на устройстве нет встроенной библиотеки slite3)

## Запуск бота как сервис

сохраним файл start-youtube-audio.service в папку /etc/systemd/system

```bash
[Unit]
Description=Youtube video to audio
After=network.target

[Service]
ExecStart=/bin/bash /home/scripts/youtube2mp3/start-youtube2mp3.sh

[Install]
WantedBy=default.target
```

## Запуск сервиса

```bash
systemctl enable start-youtube-audio.service
systemctl start start-youtube-audio.service
```

## Запуск проекта:

```bash
python start_tlgbotcore.py
```

### Запуск сервиса как docker контейнер

* создание образа контейнера

```buildoutcfg
docker build -t tlgtatartranslate .  
```

* запуск

```bash
docker run --rm   -v "/home/oilnur/prj/prj-py/py-tlgbot-translate-tatar/cfg/config_dairy.py:/home/app/cfg/config_dairy.py" -v "/home/oilnur/prj/prj-py/py-tlgbot-translate-tatar/cfg/config_tlg.py:/home/app/cfg/config_tlg.py" -v "/home/oilnur/prj/prj-py/py-tlgbot-translate-tatar/settings.db:/home/app/settings.db" tlgtatartranslate
```



