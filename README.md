# md5hash_service

Сервер будет работать только на Linux, с Windows слишком много танцев с бубном.

В работе использовались следующие ключевые модули и фреймворки:
1.Flask - для самого сервера и обработки запросов
2.RQ и Redis - для реализации очереди асинхронных заданий
3.Sqlite3 - для хранения данных всех запросов 
4.Flask-mail - для простой отправки сообщений

Чтобы всё работало, надо установить сервер Redis

'''bash
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
sudo make install
'''
Оба модуля для Flask, RQ и Redis
'''bash
pip install flask
pip install flask-mail
pip install rq
pip install redis
'''

Всё остальное описано в requirements.txt


