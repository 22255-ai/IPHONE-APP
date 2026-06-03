import sqlite3

from flask import Flask,g, render_template

DATABASE = 'database.db'

#initialise app
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home ():
    #home page 
    db=get_db()
    cursor = db.cursor()
    sql = "SELECT * FROM iphone;"
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    return render_template("home.html",results=results)



if __name__ == '__main__':
    app.run(debug=True)