# Импортируем необходимые модули из Flask и стандартной библиотеки
from flask import Flask, jsonify, g, abort, request  # Flask — основной класс приложения, jsonify — для возврата JSON, g — глобальный объект для хранения данных запроса, abort — для обработки ошибок, request — для получения данных из POST
import sqlite3  # Модуль для работы с SQLite базой данных
from flask_cors import CORS

# Создаём экземпляр Flask-приложения
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}}, supports_credentials=True)
# Имя файла базы данных
DATABASE = 'users.db'

# Функция для получения соединения с базой данных для текущего запроса
# Соединение сохраняется в объекте g, чтобы использовать одно соединение на запрос
# Если соединения ещё нет, оно создаётся и сохраняется в g._database
# row_factory позволяет получать строки как словари (dict)
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# Функция, которая вызывается после завершения обработки запроса
# Закрывает соединение с базой данных, если оно было открыто
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Функция инициализации базы данных
# Создаёт таблицу users, если она не существует
# Добавляет тестовых пользователей, если таблица пуста
# Выполняется только при запуске приложения напрямую
# Использует контекст приложения Flask
# (иначе get_db() не будет работать)
def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )''')  # Создаём таблицу users, если её нет
        db.commit()
        # Проверяем, пуста ли таблица
        cur = db.execute('SELECT COUNT(*) as cnt FROM users')
        if cur.fetchone()['cnt'] == 0:
            # Если пуста — добавляем тестовых пользователей
            db.executemany('INSERT INTO users (name, email) VALUES (?, ?)', [
                ('Alice', 'alice@example.com'),
                ('Bob', 'bob@example.com'),
                ('Charlie', 'charlie@example.com'),
            ])
            db.commit()

# Маршрут для получения списка всех пользователей
# Метод: GET /users
@app.route('/users', methods=['GET'])
def get_users():
    db = get_db()  # Получаем соединение с БД
    users = db.execute('SELECT * FROM users').fetchall()  # Получаем всех пользователей
    # Преобразуем результат в список словарей и возвращаем как JSON
    return jsonify([dict(u) for u in users])

# Маршрут для получения одного пользователя по id
# Метод: GET /users/<user_id>
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = get_db()  # Получаем соединение с БД
    # Получаем пользователя по id
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user is None:
        # Если пользователь не найден — возвращаем ошибку 404
        return jsonify({'error': 'User not found'}), 404
    # Если найден — возвращаем его данные как JSON
    return jsonify(dict(user))

# Маршрут для добавления нового пользователя
# Метод: POST /users
@app.route('/users', methods=['POST'])
def add_user():
    db = get_db()
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400
    try:
        db.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        db.commit()
        return jsonify({'message': 'User added successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'User with this email already exists'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Маршрут для обработки OPTIONS-запросов для /users
@app.route('/users', methods=['OPTIONS'])
def users_options():
    return '', 204

# Маршрут для удаления пользователя по id
# Метод: DELETE /users/<user_id>
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.commit()
    return jsonify({'message': 'User deleted successfully'})

# Точка входа при запуске файла напрямую
if __name__ == '__main__':
    init_db()  # Инициализируем базу данных (создаём таблицу и тестовые данные)
    app.run(debug=True)  # Запускаем Flask-приложение в режиме отладки 