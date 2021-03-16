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
                 'weight TEXT,'
                 'imageurl TEXT,'
                 'description TEXT,'
                 'FOREIGN KEY(Ownerid) REFERENCES owner_table(Ownerid))')
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

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dog_table")

    print(cursor.fetchall())

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
        msg = None
        try:
            post_data = request.get_json()
            firstname = post_data['Firstname']
            lastname = post_data['Lastname']
            username = post_data['Username']
            age = post_data['age']
            email = post_data['email']
            password = post_data['Password']
            with sqlite3.connect('database.db') as conn:

                conn.row_factory = dict_factory

                cur = conn.cursor()
                cur.execute("INSERT INTO owner_table(Firstname, Lastname, Username, age, Email, Password)VALUES "
                            "(?, ?, ?, ?, ?, ?)", (firstname, lastname, username, age, email, password))
                conn.commit()
                msg = "Record added succesfully."

        except Exception as e:
            return {'error': str(e)}
        finally:
            conn.close()
            return {'msg': msg}

@app.route('/test/')
def test():
    return render_template('test.html')

@app.route('/login-user/' , methods=["GET"])
def login_user():
    if request.method == 'GET':
        response = {}
        response['msg'] = None
        response['body'] = []

        try:
            # get_data = request.get_json()
            # username = get_data['username']
            # password = get_data['password']

            with sqlite3.connect('database.db') as conn:
                conn.row_factory = dict_factory
                cur = conn.cursor()
                sql_stmnt = ('SELECT * FROM owner_table')
                cur.execute(sql_stmnt)
                admins = cur.fetchall()
                conn.commit()
                response['body'] = admins
                response['msg'] = "user logged in succesfully."

        except Exception as e:
            conn.rollback()
            response['msg'] = "Something went wrong while verifying a record: " + str(e)

        finally:
            return response

@app.route('/create-blog/', methods=["POST"])
def create_blog():
    if request.method == 'POST':
        msg = None
        try:
            post_data = request.get_json()
            dog_name = post_data['dogname']
            dog_type = post_data['dogtype']
            dog_age = post_data['dogage']
            dog_weight = post_data['weight']
            image_url = post_data['imageurl']
            description = post_data['description']
            with sqlite3.connect('database.db') as conn:

                conn.row_factory = dict_factory

                cur = conn.cursor()
                cur.execute("INSERT INTO dog_table(dogname, dogtype, dogage, weight , imageurl, description)VALUES "
                            "(?, ?, ?, ?, ?, ?)", (dog_name, dog_type, dog_age, dog_weight, image_url, description))
                conn.commit()
                msg = "blog added succesfully."

        except Exception as e:
            return {'error': str(e)}
        finally:
            conn.close()
            return {'msg': msg}

@app.route('/display-content/' , methods=["GET"])
def display_rec():
    if request.method == 'GET':
        response = {}
        response['msg'] = None
        response['body'] = []

        try:
            # get_data = request.get_json()
            # username = get_data['username']
            # password = get_data['password']

            with sqlite3.connect('database.db') as conn:
                conn.row_factory = dict_factory
                cur = conn.cursor()
                sql_stmnt = ('SELECT * FROM dog_table')
                cur.execute(sql_stmnt)
                admins = cur.fetchall()
                conn.commit()
                response['body'] = admins
                response['msg'] = "records on display"

        except Exception as e:
            conn.rollback()
            response['msg'] = "Something went wrong while displaying a record: " + str(e)

        finally:
            return response


@app.route('/delete_records/<int:Ownerid>/', methods=["DELETE"])
def delete_records(Ownerid):

    msg = None
    try:
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM owner_table WHERE id=" + str(Ownerid))
            conn.commit()
            msg = "record deleted successfully deleted"
    except Exception as e:
        conn.rollback()
        msg = "Error occured when attempting to delete a record"
    finally:
        conn.close()
        return str("record deleted successfully deleted")