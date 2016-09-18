# gtudata
scrapy 
Проект сбора данных с сайта при помощи фреймворка scrapy

Автор: Цымай Дмитрий

email: dmitry-zy@yandex.ru

Подробнее здесь: https://habrahabr.ru/post/308660/ 

Требует установки python 2, scrapy, sqlalchemy, sqlite3

Руководство по установке scrapy:
https://scrapy.readthedocs.io/en/latest/intro/install.html

Руководство по установке sqlalchemy:
http://www.sqlalchemy.org/download.html

Чтобы запустить проект:
1. Установите все необходимое, 
2. Скачайте проект на локальную машину, 
3. Зайдите в каталог gtudata (там находится файл scrapy.cfg) 
    и запустите  команды из консоли:
        scrapy crawl speclist
        scrapy crawl abiturlist
Результат будет записан в базу данных sqlite: data_scraped


