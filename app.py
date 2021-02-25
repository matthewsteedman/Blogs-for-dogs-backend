import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS


def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Database opened successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS owner_table('
                    'Ownerid INTEGER PRIMARY KEY AUTOINCREMENT,'
                    'Firstname TEXT,'
                    'Lastname TEXT,'
                    'Username TEXT,'
                    'age INTEGER,'
                    'Email TEXT,'
                    'Password TEXT )'
                 )
    print("owner_table table created successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS dog_table('
                    'dogid INTEGER PRIMARY KEY AUTOINCREMENT,'
                    'dogname TEXT, dogtype TEXT, dogage TEXT,'
                    'Ownerid INTEGER,'
                    'for_key TEXT,'
                    'weight TEXT,'
                    'imageurl TEXT,'
                    'description TEXT,'
                    'FOREIGN KEY(for_key) REFERENCES owner_table(Ownerid))')
    print("dog_table table created successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS daily_logs_table('
                    'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                    'username TEXT ,'
                    'sign_in_time TEXT,'
                    'sign_out_time TEXT,'
                    'date TEXT)')
    print("daily_logs_table table created successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS comment_table('
                    'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                    'username TEXT, comment TEXT)')
    print("comment_table table created successfully")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM owner_table")

    print(cursor.fetchall())

#    try:
#       conn.execute("INSERT INTO owner_table(Firstname, Lastname, Username, age, Email, Password) VALUES "
#                     "(?, ?, ?, ?, ?, ?)",  ('matthew', 'steedman', 'matta', 21, 'msteedman77@gmail.com', '12345'))
#       conn.commit()
#   except Exception as e:
#        print('Something wrong happend when inserting record to database: ' + str(e))
#   print('successfully')

#    conn.execute('SELECT * FROM owner_table')
#   table_2 = conn.cursor()
#    conn.commit()
#    print(table_2.fetchall())

    conn.close()

init_sqlite_db()


app = Flask(__name__)
CORS(app)
'''
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
'''
@app.route('/register-user/', methods=["POST"])
def register_user():
    msg = 'record successfully added'
    if request.method == 'POST':

        try:
            Firstname = request.form['Firstname']
            Lastname = request.form['Lastname']
            Username = request.form['Username']
            age = request.form['age']
            Email = request.form['email']
            Password = request.form['Password']

            with sqlite3.connect('database.db') as conn:
                '''
                conn.row_factory = dict_factory
                '''
                cur = conn.cursor()
                cur.execute("INSERT INTO owner_table(Firstname, Lastname, Username, age, Email, Password)VALUES "
                    "(?, ?, ?, ?, ?, ?)", (Firstname, Lastname, Username, age, Email, Password))
                conn.commit()
                return  jsonify(msg)

        except Exception as e:
            conn.rollback()

        finally:
            conn.close()
            return jsonify(msg)




