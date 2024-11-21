from flask import Flask, render_template, redirect, g
import pymysql.cursors
app = Flask(__name__)

host = ""
user = ""
password = ""
database = ""

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host=host,                 # à modifier
            user=user,                     # à modifier
            password=password,                # à modifier
            database=database,        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_layout():
    return render_template('layout.html')

# ---------------------------------------------------------------------#

@app.route('/benne/show')
def show_benne():
    return render_template('benne/benne_show.html')

@app.route('/benne/add')
def add_benne():
    return render_template('benne/benne_add.html')

@app.route('/benne/edit')
def edit_benne():
    return render_template('benne/benne_edit.html')

@app.route('/benne/delete')
def delete_benne():
    return redirect('benne/show')

@app.route('/benne/etat')
def etat_benne():
    return render_template('benne/benne_etat.html')

# ---------------------------------------------------------------------#

@app.route('/passage/show')
def show_passage():
    return render_template('passage/passage_show.html')

@app.route('/passage/add')
def add_passage():
    return render_template('passage/passage_add.html')

@app.route('/passage/edit')
def edit_passage():
    return render_template('passage/passage_edit.html')

@app.route('/passage/delete')
def delete_passage():
    return redirect('passage/show')

@app.route('/passage/etat')
def etat_passage():
    return render_template('passage/passage_etat.html')

# ---------------------------------------------------------------------#

@app.route('/decharge/show')
def show_decharge():
    return render_template('decharge/decharge_show.html')

@app.route('/decharge/add')
def add_decharge():
    return render_template('decharge/decharge_add.html')

@app.route('/decharge/edit')
def edit_decharge():
    return render_template('decharge/decharge_edit.html')

@app.route('/decharge/delete')
def delete_decharge():
    return redirect('decharge/show')

@app.route('/decharge/etat')
def etat_decharge():
    return render_template('decharge/decharge_etat.html')

# ---------------------------------------------------------------------#

@app.route('/vehicule/show')
def show_vehicule():
    return render_template('vehicule/vehicule_show.html')

@app.route('/vehicule/add')
def add_vehicule():
    return render_template('vehicule/vehicule_add.html')

@app.route('/vehicule/edit')
def edit_vehicule():
    return render_template('vehicule/vehicule_edit.html')

@app.route('/vehicule/delete')
def delete_vehicule():
    return redirect('vehicule/show')

@app.route('/vehicule/etat')
def etat_vehicule():
    return render_template('vehicule/vehicule_etat.html')

# ---------------------------------------------------------------------#

if __name__ == '__main__':
    app.run()
