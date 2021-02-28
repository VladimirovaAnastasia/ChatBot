# Чат-бот для отправки уведомления о проверке работ 

Бот, который присылает уведомление об успешном/неуспешном результате проверки работы на [dvmn.org](https://dvmn.org/modules/).
![Telegram](https://dvmn.org/media/reviews.jpg)

## Как запустить
 Устанавливаем необходимые библиотеки
 ```
 pip install requirements.txt
```
 
Для корректной работы скрипта в корневой папке проекта необходимо создать файл с именем `.env`. Открыв его с помощью любого текстового редактора, необходимо указать данные в следующем формате (без кавычек):
 ```
DEVMAN_API_TOKEN=your_devman_api_token
TG_CHAT_ID = your_tg_chat_id
TG_TOKEN=your_tg_token
HTTP_PROXY=your_http_proxy
```

Как получить данные параметры: 

`DEVMAN_API_TOKEN` - находится [здесь](https://dvmn.org/api/docs/), если вы авторизованы.

`TG_TOKEN` - [инструкция](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/), 

`TG_CHAT_ID` - необходимо написать в Telegram специальному боту: @userinfobot, предварительно не забыв отправить сообщение своему боту,

`HTTP_PROXY` - любое работающее прокси.


 Запускаем скрипт командой 
 ```
 python script.py runserver
 ```

 
## Цель проекта
 Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/modules/) 
