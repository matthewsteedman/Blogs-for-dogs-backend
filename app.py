import sqlite3
from flask import Flask, request, render_template
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

#     conn.close()
#
#
init_sqlite_db()

app = Flask(__name__)
CORS(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/register/')
def register_test():
    return render_template('register_text.html')


@app.route('/register-user/', methods=["POST"])
def register_user():
    if request.method == 'POST':
        response = {'msg': None}

        try:
            firstname = request.form['Firstname']
            lastname = request.form['Lastname']
            username = request.form['Username']
            age = request.form['age']
            email = request.form['email']
            password = request.form['Password']

            with sqlite3.connect('database.db') as conn:

                conn.row_factory = dict_factory

                cur = conn.cursor()
                cur.execute("INSERT INTO owner_table(Firstname, Lastname, Username, age, Email, Password)VALUES "
                            "(?, ?, ?, ?, ?, ?)", (firstname, lastname, username, age, email, password))
                conn.commit()
                response['msg'] = "Record added succesfully."

        except Exception as e:
            conn.rollback()
            response['msg'] = "Something went wrong while inserting a record: " + str(e)
        finally:
            return response

@app.route('/test/')
def test():
    return render_template('test.html')

@app.route('/login-user/' , methods=["GET"])
def login_user():
    if request.method == 'GET':
        response = {}
        response['msg'] = None

        try:
            username = request.form['username']
            password = request.form['password']

            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                sql_stmnt = ('SELECT * FROM owner_table WHERE username = ? and password = ?')
                cur.execute(sql_stmnt, [(username), (password)])
                cur.fetchall()
                conn.commit()
                response['msg'] = "user logged in succesfully."

        except Exception as e:
            conn.rollback()
            response['msg'] = "Something went wrong while verifying a record: " + str(e)

        finally:
            return response

