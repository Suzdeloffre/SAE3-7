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
    form_value = request.args.get('form_value', '0')
    mycursor = get_db().cursor()
    sql = '''   SELECT *
            FROM benne
            INNER JOIN centre ON benne.num_centre = centre.num_centre
            INNER JOIN produit ON benne.num_produit = produit.num_produit;
                 '''
    mycursor.execute(sql)
    liste_benne = mycursor.fetchall()
    return render_template(
        'benne/benne_show.html',
        bennes={
            'liste_benne': liste_benne,
            'form_value': form_value
        }
    )

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
    form_value = request.args.get('form_value', '0')
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
    return render_template(
        'decharge/decharge_show.html',
        decharges={
            'liste_decharge': liste_decharge,
            'form_value': form_value
        }
    )

@app.route('/decharge/add', methods=['GET'])
def add_decharge():
    form_data = getFormDechargeList(None)
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
        form_infos = getFormDechargeList(form_data)
        return render_template('decharge/decharge_add.html', form_init=form_infos)
    mycursor = get_db().cursor()
    sql = '''  INSERT INTO decharge(num_produit, num_usine, num_vehicule, quantite, JMA)
            VALUES (%s,%s,%s,%s,%s)
                 '''
    turple_insert = (
        form_data['num_produit'],
        form_data['num_usine'],
        form_data['num_vehicule'],
        form_data['quantite'] + 'kg',
        datetime.today(),
    )
    mycursor.execute(sql, turple_insert)
    get_db().commit()
    return redirect('/decharge/show?form_value=1')

@app.route('/decharge/edit', methods=['GET'])
def edit_decharge():
    id = request.args.get('id')
    idSplited = id.split("*")
    form_data = {
        "num_usine": idSplited[1],
        "num_produit": idSplited[2],
        "num_vehicule": idSplited[0],
        "JMA": idSplited[3],
    }
    if id != None :
        mycursor = get_db().cursor()
        sql = '''   SELECT *
            FROM decharge
            WHERE num_vehicule = %s AND num_usine = %s AND num_produit = %s AND JMA = %s;
                 '''
        turple_edit = (
            form_data['num_vehicule'],
            form_data['num_usine'],
            form_data['num_produit'],
            form_data['JMA'],
        )
        mycursor.execute(sql, turple_edit)
        decharge = mycursor.fetchone()
    else:
        decharge = None
    form_data = getFormDechargeList(decharge)
    print(form_data)
    return render_template('decharge/decharge_edit.html', form_init=form_data)

@app.route('/decharge/edit', methods=['POST'])
def update_decharge():
    form_data = {
        "num_usine": request.form['num_usine'],
        "num_produit": request.form['num_produit'],
        "num_vehicule": request.form['num_vehicule'],
        "quantite": request.form['quantite'],
        "id": request.form['id'],
    }
    idSplited = form_data['id'].split("*")
    error_list = checkFormDecharge(form_data)
    if error_list:
        form_infos = getFormDechargeList(form_data)
        return render_template('decharge/decharge_add.html', form_init=form_infos)
    mycursor = get_db().cursor()
    sql = '''  UPDATE decharge
                SET num_produit=%s, num_usine=%s, num_vehicule=%s, quantite=%s, JMA=%s
                WHERE num_vehicule = %s AND num_usine = %s AND num_produit = %s AND JMA = %s
                 '''
    turple_update = (
        form_data['num_produit'],
        form_data['num_usine'],
        form_data['num_vehicule'],
        form_data['quantite'] + 'kg',
        datetime.today(),
        idSplited[0],
        idSplited[1],
        idSplited[2],
        idSplited[3]
    )
    mycursor.execute(sql, turple_update)
    get_db().commit()
    return redirect('/decharge/show?form_value=1')

@app.route('/decharge/delete')
def delete_decharge():
    id = request.args.get('id', '')
    idSplited = id.split("*")
    form_data = {
        "num_usine": idSplited[1],
        "num_produit": idSplited[2],
        "num_vehicule": idSplited[0],
        "JMA": idSplited[3],
    }
    mycursor = get_db().cursor()
    sql = '''   DELETE FROM decharge
            WHERE num_vehicule = %s AND num_usine = %s AND num_produit = %s AND JMA = %s
        '''
    turple_delete = (
        form_data['num_vehicule'],
        form_data['num_usine'],
        form_data['num_produit'],
        form_data['JMA'],
    )
    mycursor.execute(sql, turple_delete)
    get_db().commit()
    return redirect('/decharge/show?form_value=1')

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

def getFormDechargeList(previousData):
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
    if previousData:
        print(previousData)
        previousData['quantite'] = int(previousData['quantite'].replace("kg", "").strip())
    return {
        "usines": usines,
        "produits": produits,
        "vehicules": vehicules,
        "previous_data": previousData
    }


if __name__ == '__main__':
    app.run(debug=True, port=5000)
