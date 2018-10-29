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


