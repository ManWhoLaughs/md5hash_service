# md5hash_service

Сервер будет работать только на Linux, с Windows слишком много танцев с бубном.

В работе использовались следующие ключевые модули и фреймворки:
* Flask - для самого сервера и обработки запросов
* RQ и Redis - для реализации очереди асинхронных заданий
* Sqlite3 - для хранения данных всех запросов 
* Flask-mail - для простой отправки сообщений

Чтобы всё работало, надо установить сервер Redis

> ***wget http://download.redis.io/redis-stable.tar.gz***
>
> ***tar xvzf redis-stable.tar.gz***
>
> ***cd redis-stable***
>
> ***make***
>
> ***sudo make install***

Оба модуля для Flask, RQ и Redis

> ***pip install flask***
>
> ***pip install flask-mail***
>
> ***pip install rq***
>
> ***pip install redis***

Всё остальное описано в requirements.txt

Запускается пока руками через три терминала так:

1. В первом терминале просто выполнить redis-server, чтобы создать сервер с очередью задач
2. Во втором терминале перейти в корневую директорию приложения, выполнить rq-worker, чтобы создать исполнителя. (Можно несколько, если не лень)
3. В третьем так же перейти в корневую директорию и запустить run.py с помощью python.

Все настройки портов, кроме почты, оставлены по умолчанию, поэтому вроде не должно быть никаких проблем.

API(назовём гордо):

Как и было сказано в задании, принимаются два типа запросов:
* curl -X POST на <server>/submit с параметром -d, в котором в кавычках находится url и опциональный email
* curl -X GET на <server>/check c аргументами в самом url-адресе в стандартном виде ..../check?id=something
  
Если в POST корректно указан email, то через специальный gmail-ящик на этот адрес отправится оповещение о статусе задачи.
