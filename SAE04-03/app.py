from datetime import datetime

from flask import Flask, render_template, redirect, g, request
import pymysql.cursors
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'une cle(token) : grain de sel(any random string)'

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host="localhost", # à modifier
            user="root", # à modifier
            password="root", # à modifier
            database="db_usine", # à modifier
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
    return render_template('index.html')

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
    mycursor = get_db().cursor()
    sql = '''   SELECT *
        FROM decharge
        INNER JOIN usine ON decharge.num_usine = usine.num_usine
        INNER JOIN vehicule ON decharge.num_vehicule = vehicule.num_vehicule
        INNER JOIN  produit ON decharge.num_produit = produit.num_produit
        ORDER BY JMA DESC;
             '''
    mycursor.execute(sql)
    liste_decharge = mycursor.fetchall()
    return render_template('decharge/decharge_show.html', decharges=liste_decharge)

@app.route('/decharge/add', methods=['GET'])
def add_decharge():
    form_data = getFormDechargeList(None, None)
    return render_template('decharge/decharge_add.html', form_init=form_data)

@app.route('/decharge/add', methods=['POST'])
def save_decharge():
    form_data = {
        "num_usine": request.form['num_usine'],
        "num_produit": request.form['num_produit'],
        "num_vehicule": request.form['num_vehicule'],
        "quantite": request.form['quantite'],
    }
    error_list = checkFormDecharge(form_data)
    if error_list:
        formInfos = getFormDechargeList(form_data, error_list)
        return render_template('decharge/decharge_add.html', form_init=formInfos)
    mycursor = get_db().cursor()
    sql = '''  INSERT INTO decharge(num_produit, num_usine, num_vehicule, quantite, JMA)
            VALUES (%s,%s,%s,%s,%s)
                 '''
    turple_insert = (
        form_data['num_produit'],
        form_data['num_usine'],
        form_data['num_vehicule'],
        form_data['quantite'],
        datetime.today(),
    )
    mycursor.execute(sql, turple_insert)
    get_db().commit()
    return redirect('/decharge/show')

@app.route('/decharge/edit')
def edit_decharge():
    return render_template('decharge/decharge_edit.html')

@app.route('/decharge/delete')
def delete_decharge():
    mycursor = get_db().cursor()
    sql = '''   DELETE FROM décharge
     WHERE num=%s;
             '''
    turple_insert = (id)
    mycursor.execute(sql, turple_insert)

    get_db().commit()
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

def checkFormDecharge(formData):
    erroList = []
    # check produit
    mycursor = get_db().cursor()
    sql = '''   SELECT num_produit
            FROM produit
            WHERE num_produit=%s;
                 '''
    mycursor.execute(sql, (formData['num_produit']))
    if mycursor.rowcount == 0 :
        erroList.append("Erreur:  Produit invalide !")

    #check usine
    mycursor = get_db().cursor()
    sql = '''   SELECT num_usine
               FROM usine
               WHERE num_usine=%s;
                    '''
    mycursor.execute(sql, (formData['num_usine']))
    if mycursor.rowcount == 0:
        erroList.append("Erreur:  Usine inexistante !")

    #check vehicule
    mycursor = get_db().cursor()
    sql = '''   SELECT num_vehicule
               FROM vehicule
               WHERE num_vehicule=%s;
                    '''
    mycursor.execute(sql, (formData['num_vehicule']))
    if mycursor.rowcount == 0:
        erroList.append("Erreur:  Vehicule introuvable !")

    return erroList

def getFormDechargeList(previousData, errorList):
    mycursor = get_db().cursor()
    sql = '''   SELECT *
                FROM usine
                ORDER BY nom_usine;
                     '''
    mycursor.execute(sql)
    usines = mycursor.fetchall()

    sql = '''   SELECT *
                    FROM produit
                    ORDER BY libelle_produit;
                         '''
    mycursor.execute(sql)
    produits = mycursor.fetchall()
    sql = '''   SELECT *
                        FROM vehicule
                        ORDER BY poid_max;
                             '''
    mycursor.execute(sql)
    vehicules = mycursor.fetchall()
    return {
        "usines": usines,
        "produits": produits,
        "vehicules": vehicules,
        "errorList": errorList,
        "previousData": previousData
    }


if __name__ == '__main__':
    app.run(debug=True, port=5000)
