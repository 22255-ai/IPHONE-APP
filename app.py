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

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def home ():
    #home page 
    sql = """SELECT i.id, i.model,i.image_url, r.size AS ram_gb
            FROM iphone i 
            JOIN phone_ram pr ON i.id = pr.phone_id
            JOIN ram r ON pr.ram_id = r.id"""
 
    results = query_db(sql)
    print(results)
    return render_template("home.html",results=results)

@app.route('/iphone/<int:iphone_id>')
def iphone (iphone_id):
    #iphone details page
    sql =    """SELECT iphone.id, iphone.model, cpu.name, iphone.front_camera, iphone.rear_camera, iphone.image_url
                FROM iphone JOIN cpu ON cpu.id=iphone.cpu_id
                JOIN phone_ram ON phone_ram.phone_id=iphone.id
                JOIN ram ON ram.id=phone_ram.ram_id
                WHERE iphone.id = ?"""
    
    
    results = query_db(sql,[iphone_id],one=True)
    print(results)
    return render_template("iphone.html",results=results)

if __name__ == '__main__':
    app.run(debug=True)