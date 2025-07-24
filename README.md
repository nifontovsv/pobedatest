# Flask Users App

Это простое приложение на Flask для управления пользователями с веб-интерфейсом (HTML+JS) и backend на Python/Flask/SQLite.

## Быстрый старт

### 1. Клонируйте репозиторий
```bash
git clone <ссылка_на_репозиторий>
cd <имя_папки_проекта>
```

### 2. (Рекомендуется) Создайте и активируйте виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate
```
На Windows:
```bash
venv\Scripts\activate
```

### 3. Установите зависимости
Если есть файл requirements.txt:
```bash
pip install -r requirements.txt
```
Если файла нет, установите вручную:
```bash
pip install flask flask-cors
```

### 4. Запустите backend (Flask)
```bash
python3 pobedatest/flask_users_app.py
```

- Сервер будет доступен по адресу: http://127.0.0.1:5000

### 5. Откройте frontend
- Откройте файл `pobedatest/users_frontend.html` в браузере (двойной клик или через Live Server/расширение VS Code).
- Веб-интерфейс будет работать с backend автоматически.

---

## Структура проекта
- `pobedatest/flask_users_app.py` — backend (Flask + SQLite)
- `pobedatest/users_frontend.html` — frontend (HTML + JS)

---

## Примечания
- При первом запуске база данных создаётся автоматически, добавляются тестовые пользователи.
- Для сброса базы (id снова будут 1, 2, 3) — просто перезапустите backend.
- Для работы нужен Python 3.6+.

---

## Возможные проблемы
- Если не установлен Python или pip — скачайте с https://python.org
- Если порт 5000 занят — измените его в файле flask_users_app.py (`app.run(debug=True, port=5001)`)
- Если не работает CORS — убедитесь, что открываете frontend по адресу http://127.0.0.1:5500 и backend по http://127.0.0.1:5000


