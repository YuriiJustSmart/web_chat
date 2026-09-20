1. Завантаж файли

Зайди на PythonAnywhere → Files.

Створи папку mysite і завантаж туди всі файли проєкту: .py, templates, static, SQLite-базу.

2. Відкрий Bash

У Consoles → Bash виконай:

cd ~/mysite
mkvirtualenv --python=/usr/bin/python3.13 compterra-venv
pip install flask

Якщо є requirements.txt:

pip install -r requirements.txt
3. Створи Web App

Web → Add a new web app → Manual configuration → Python 3.13.

Укажи:

Source code: /home/compterra/mysite
Virtualenv: /home/compterra/.virtualenvs/compterra-venv
4. Налаштуй WSGI

Відкрий WSGI configuration file і встав:

import sys

sys.path.insert(0, '/home/compterra/mysite')

from app import app as application

Якщо головний файл називається main.py, заміни app у рядку імпорту на main.

5. Запусти сайт

На вкладці Web натисни Reload, потім відкрий:

compterra.pythonanywhere.com

Якщо з'явиться помилка, відкрий Web → Error log.

Уточнення: як називається твій головний Python-файл — app.py, main.py чи інший?
