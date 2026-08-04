from flask import Flask, render_template, request, redirect, session
import sqlite3
import bcrypt
import difflib

app = Flask(__name__)
app.secret_key = 'your_secret_key_social_net'

DB_NAME = "users.db"

def fuzzy_interest_match(db_interests, search_term):
    if not db_interests or not search_term:
        return False
    search_term = str(search_term).lower().strip()
    db_interests_list = [i.strip().lower() for i in str(db_interests).split(',')]
    
    for item in db_interests_list:
        if search_term in item:
            return True
        similarity = difflib.SequenceMatcher(None, item, search_term).ratio()
        if similarity >= 0.7:
            return True
    return False

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                country TEXT,
                interests TEXT,
                avatar TEXT,
                bio TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                FOREIGN KEY (sender_id) REFERENCES users_new (id),
                FOREIGN KEY (receiver_id) REFERENCES users_new (id)
            )
        """)
        conn.commit()

init_db()

@app.route('/', methods=['GET'])
def home():
    if 'user_id' in session:
        current_user_id = session['user_id']
        
        username_query = request.args.get('username_search', '').strip()
        interest_query = request.args.get('interest_search', '').strip()
        age_min = request.args.get('age_min', '').strip()
        age_max = request.args.get('age_max', '').strip()
        country_query = request.args.get('country', '').strip()
        gender_query = request.args.get('gender', '').strip()
        
        try:
            with sqlite3.connect(DB_NAME) as conn:
                conn.create_function("FUZZY_MATCH", 2, fuzzy_interest_match)
                
                cursor = conn.cursor()
                cursor.execute("SELECT username FROM users_new WHERE id = ?", (current_user_id,))
                res = cursor.fetchone()
                if not res:
                    session.pop('user_id', None)
                    return render_template('index.html', logged_in=False)
                current_username = res[0]
                
                query = "SELECT * FROM users_new WHERE 1=1"
                params = []
                
                if username_query:
                    query += " AND username LIKE ?"
                    params.append(f"%{username_query}%")
                if interest_query:
                    query += " AND FUZZY_MATCH(interests, ?)"
                    params.append(interest_query)
                if age_min.isdigit():
                    query += " AND age >= ?"
                    params.append(int(age_min))
                if age_max.isdigit():
                    query += " AND age <= ?"
                    params.append(int(age_max))
                if country_query:
                    query += " AND country LIKE ?"
                    params.append(f"%{country_query}%")
                if gender_query:
                    query += " AND gender = ?"
                    params.append(gender_query)
                
                cursor.execute(query, params)
                users = cursor.fetchall()
                
                cursor.execute("SELECT id, username, avatar FROM users_new")
                all_users_info = {row[0]: {'username': row[1], 'avatar': row[2]} for row in cursor.fetchall()}
                
                cursor.execute("""
                    SELECT sender_id, receiver_id, message 
                    FROM messages 
                    WHERE sender_id = ? OR receiver_id = ?
                    ORDER BY id ASC
                """, (current_user_id, current_user_id))
                all_messages = cursor.fetchall()
                
                grouped_chats = {}
                for sender_id, receiver_id, message_text in all_messages:
                    partner_id = receiver_id if sender_id == current_user_id else sender_id
                    
                    if partner_id not in grouped_chats:
                        partner_info = all_users_info.get(partner_id, {'username': "Невідомий", 'avatar': None})
                        grouped_chats[partner_id] = {
                            'partner_name': partner_info['username'],
                            'partner_avatar': partner_info['avatar'],
                            'messages': []
                        }
                    
                    sender_info = all_users_info.get(sender_id, {'username': "Невідомий", 'avatar': None})
                    grouped_chats[partner_id]['messages'].append((
                        sender_info['username'], 
                        message_text, 
                        sender_info['avatar']
                    ))
                
            return render_template(
                'index.html', 
                logged_in=True,
                users=users, 
                current_username=current_username, 
                grouped_chats=grouped_chats
            )
        except Exception as e:
            return f"<p>Помилка бази даних: {str(e)}</p>"
            
    return render_template('index.html', logged_in=False)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users_new WHERE username = ?", (username,))
            user = cursor.fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]
            return redirect("/")
        else:
            return "<p>Невірний логін або пароль! <a href='/'>Спробувати знову</a></p>"
    except Exception as e:
        return f"<p>Помилка при перевірці: {str(e)}</p>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        raw_password = request.form['password']
        
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt(rounds=10)).decode('utf-8')
        
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users_new (username, email, password) VALUES (?, ?, ?)", 
                               (username, email, hashed_password))
                conn.commit()
                
                cursor.execute("SELECT id FROM users_new WHERE username = ?", (username,))
                new_user = cursor.fetchone()
                if new_user:
                    session['user_id'] = new_user[0]
                    
            return redirect("/profile_setup")
        except sqlite3.IntegrityError:
            return "<p>Помилка: Користувач з таким ім'ям вже існує! <a href='/'>На головну</a></p>"
        except Exception as e:
            return f"<p>Помилка реєстрації: {str(e)}</p>"
            
    return redirect("/")

@app.route('/profile_setup', methods=['GET', 'POST'])
def profile_setup():
    if 'user_id' not in session:
        return redirect("/")
        
    user_id = session['user_id']
    
    if request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        country = request.form.get('country')
        interests = request.form.get('interests')
        avatar = request.form.get('avatar')
        bio = request.form.get('bio')
        
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users_new 
                    SET age = ?, gender = ?, country = ?, interests = ?, avatar = ?, bio = ? 
                    WHERE id = ?
                """, (age if age else None, gender, country, interests, avatar, bio, user_id))
                conn.commit()
            return redirect("/")
        except Exception as e:
            return f"<p>Помилка збереження профілю: {str(e)}</p>"
            
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users_new WHERE id = ?", (user_id,))
            user = cursor.fetchone()
    except Exception as e:
        return f"<p>Помилка бази даних: {str(e)}</p>"
        
    return render_template('profile.html', user=user)

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect("/")
        
    sender_id = session['user_id']
    receiver_id = request.form['receiver_id']
    message = request.form['message']
    
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO messages (sender_id, receiver_id, message) VALUES (?, ?, ?)",
                           (sender_id, receiver_id, message))
            conn.commit()
        return redirect("/")
    except Exception as e:
        return f"<p>Помилка надсилання повідомлення: {str(e)}</p>"

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True, port=5002)