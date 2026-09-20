🚀 Розгортання Flask-додатку на PythonAnywhereПокрокова інструкція для деплою твого проєкту на сервер PythonAnywhere.1. Завантаж файли проєктуПерейди на PythonAnywhere $\rightarrow$ вкладка Files.Створи папки за таким шляхом: /home/YuraJustSmart/my_messenger/.Завантаж туди всі файли твого проєкту: головний файл (app.py), папки з шаблонами (templates), статичними файлами (static) та SQLite-базу (якщо використовується).2. Налаштуй середовище в BashВідкрий вкладку Consoles $\rightarrow$ Bash та виконай команди для створення віртуального середовища й встановлення залежностей:Bashcd ~/my_messenger
mkvirtualenv --python=/usr/bin/python3.13 compterra-venv
pip install flask
💡 Якщо у проєкті є файл із залежностями, встановіть їх однією командою:Bashpip install -r requirements.txt
3. Створи Web AppПерейди на вкладку Web $\rightarrow$ натисни Add a new web app.Обери Manual configuration $\rightarrow$ вибери Python 3.13.Заповни шляхи до проєкту та віртуального середовища:Source code: /home/YuraJustSmart/my_messengerVirtualenv: /home/YuraJustSmart/.virtualenvs/compterra-venv4. Налаштуй Static Files (Статичні файли)Щоб стилі CSS, скрипти JavaScript та інші статичні ресурси завантажувалися коректно й швидко, налаштуй їх у панелі керування:Перейди на вкладку Web і знайди розділ Static files.Додай нове правило мапінгу:URL: /static/Directory: /home/YuraJustSmart/my_messenger/static/5. Налаштуй WSGI-файлУ розділі Code на вкладці Web клікни на посилання на WSGI configuration file (наприклад, /var/www/yurajustsmart_pythonanywhere_com_wsgi.py).Заміни його вміст на такий код:Pythonimport sys

# Шлях до папки з твоїм проєктом
sys.path.insert(0, '/home/YuraJustSmart/my_messenger')

# Імпорт Flask-додатку (головний файл називається app.py)
from app import app as application
6. Запусти та перевір сайтПовернись на вкладку Web і натисни зелену кнопку Reload.Перейди за посиланням твого сайту: YuraJustSmart.pythonanywhere.com⚠️ Якщо на сайті з'явиться помилка (наприклад, 500 Internal Server Error), перевір деталі у розділі Web $\rightarrow$ Error log.
