from flask import Flask, render_template, request, redirect , url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'aditya'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password1234'
app.config['MYSQL_DB'] = 'student_db'

mysql = MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('signin'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE email = %s AND password = %s", (email, password))
        students = cur.fetchone()
        cur.close()
        if students:
            session['email'] = email
            return redirect(url_for('profile'))
        else:
            return render_template('signin.html', error='Invalid username or password.')
    return render_template('signin.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        
        first_name = request.form['first']
        last_name = request.form['last']
        roll_no = request.form['roll_no']
        course = request.form['Course']
        score = request.form['score']
        dob = request.form['dob']
        gender = request.form['gender']
        email = request.form['email']
        contact_no = request.form['mobile']
        address = request.form['address']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE email = %s", (email,))
        existing_user = cur.fetchone()
        cur.close()

        if existing_user:
            return render_template('register.html', error_message="Email already registered")


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student (first_name,last_name, roll_no, dob, gender, email, contact_no, address,password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)",
                    (first_name, last_name, roll_no, dob, gender, email, contact_no, address,password))
        mysql.connection.commit()

        cur.execute("SELECT LAST_INSERT_ID()")
        student_id = cur.fetchone()[0]

        cur.execute("INSERT INTO courses (student_id, course, score) VALUES (%s, %s, %s)",
                    (student_id, course, score))
        mysql.connection.commit()


        cur.close()

        return redirect(url_for('registersuccess'))
    return render_template('register.html')


@app.route('/registersuccess')
def registersuccess():
    return render_template('registersuccess.html')

@app.route('/profile')
def profile():
    if 'email' in session:
        email = session['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT student.*, courses.course, courses.score 
            FROM student 
            LEFT JOIN courses ON student.id = courses.student_id 
            WHERE student.email = %s
        """, (email,))
        user = cur.fetchone()
        cur.close()
        return render_template('profile.html', user=user)
    return redirect(url_for('signin'))

@app.route('/students')
def students():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT student.*, courses.course, courses.score 
        FROM student 
        LEFT JOIN courses ON student.id = courses.student_id
    """)
    students = cur.fetchall()
    cur.close()
    return render_template('students.html', students=students)



@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)
