# 🚀 Розгортання Flask-додатку на PythonAnywhere

Покрокова інструкція для деплою твого проєкту на сервер PythonAnywhere.
### Замість "mysite" встав назву своєї папки, "YuraJustSmart" - свій нік)
---

### 1. Завантаж файли
- Зайди на PythonAnywhere → вкладка Files.
- Створи папку mysite (або свою назву) і завантаж туди всі файли проєкту: .py, templates, static, SQLite-базу.

### 2. Відкрий Bash
У розділі Consoles → Bash виконай команди:
```bash
cd ~/mysite
mkvirtualenv --python=/usr/bin/python3.13 mysite-venv
pip install flask
```

### 3. Створи Web App
- Перейди у Web → Add a new web app → Manual configuration → Python 3.13.
- Укажи шляхи:
  - Source code: /home/YuraJustSmart/mysite
  - Virtualenv: /home/YuraJustSmart/.virtualenvs/mysite-venv

### 4. Налаштуй Static Files
У розділі Static files укажи параметри:
- URL: /static/
- Directory: /home/YuraJustSmart/mysite/static/

### 5. Налаштуй WSGI
Відкрий WSGI configuration file і встав код:
```python
import sys
sys.path.insert(0, '/home/YuraJustSmart/mysite')
from app import app as application
```
*(Якщо головний файл називається main.py, заміни app у рядку імпорту на main).*

### 6. Запусти сайт
- На вкладці Web натисни кнопку Reload.
- Відкрий свій сайт: compterra.pythonanywhere.com
- Якщо з'явиться помилка, перевір Web → Error log.
