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
    return render_template('layout.html')

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
    mycursor = get_db().cursor()
    sql = '''   SELECT vehicule.num_vehicule, vehicule.num_type, vehicule.num_marque,
                vehicule.poid_max, vehicule.date_achat
            FROM vehicule
            INNER JOIN type_vehicule ON vehicule.num_type = type_vehicule.num_type
            INNER JOIN marque ON vehicule.num_marque = marque.num_marque
            ORDER BY type_vehicule.libelle_type ASC;
                 '''
    mycursor.execute(sql)
    vehicule = mycursor.fetchall()
    return render_template('vehicule/vehicule_show.html', vehicule=vehicule)

@app.route('/vehicule/add', methods=['GET'])
def add_vehicule():
    mycursor = get_db().cursor()
    sql = '''
        SELECT type_vehicule.num_type AS id, type_vehicule.libelle_type AS libelle
        FROM type_vehicule;
        '''
    mycursor.execute(sql)
    type_vehicule = mycursor.fetchall()

    sql = '''
        SELECT marque.num_marque AS id, marque.libelle_marque AS libelle
        FROM marque;
        '''
    mycursor.execute(sql)
    marque = mycursor.fetchall()
    return render_template('vehicule/vehicule_add.html', type_vehicule=type_vehicule, marque=marque)

@app.route('/vehicule/add', methods=['POST'])
def valid_add_vehicule():
    num_type = request.form.get('type_vehicule')
    num_marque = request.form.get('marque')
    poid_max = request.form.get('poid_max')
    date_achat = request.form.get('date_achat')
    print(num_type, num_marque, poid_max, date_achat)
    mycursor = get_db().cursor()
    sql='''
    INSERT INTO vehicule(num_vehicule, num_type, num_marque, poid_max, date_achat)
     VALUES (NULL, %s, %s, %s, %s);
    '''
    tuple_insert=(num_type, num_marque, poid_max, date_achat)
    mycursor.execute(sql, tuple_insert)

    get_db().commit()
    return redirect('/vehicule/show')

@app.route('/vehicule/edit', methods=['GET'])
def edit_vehicule():
    id=request.args.get('id')
    if id != None and id.isnumeric():
        indice = int(id)
        mycursor = get_db().cursor()
        sql = '''
                SELECT num_vehicule, num_type, num_marque, poid_max, date_achat 
                FROM vehicule
                WHERE num_vehicule=%s;
                '''
        mycursor.execute(sql, indice)
        vehicule = mycursor.fetchone()

        sql = '''
                SELECT type_vehicule.num_type AS id, type_vehicule.libelle_type AS libelle,
                FROM type_vehicule;
                '''
        mycursor.execute(sql)
        type_vehicule = mycursor.fetchall()

        sql = '''
                SELECT marque.num_marque AS id, marque.libelle_marque AS libelle
                FROM marque;
                '''
        mycursor.execute(sql)
        marque = mycursor.fetchall()

        get_db().commit()
    else:
        vehicule=[]
    return render_template('vehicule/vehicule_edit.html', vehicule=vehicule, type_vehicule=type_vehicule, marque=marque)

@app.route('/vehicule/edit', methods=['POST'])
def valid_edit_vehicule():
    id = request.form.get('id')
    num_type = request.form.get('type_vehicule')
    num_marque = request.form.get('marque')
    poid_max = request.form.get('poid_max')
    date_achat = request.form.get('date_achat')

    mycursor = get_db().cursor()
    sql = '''
        UPDATE vehicule
        SET num_type = %s, num_marque = %s, poid_max = %s, date_achat = %s
        WHERE num_vehicule = %s;
    '''
    tuple_insert=(num_type, num_marque, poid_max, date_achat, id)
    mycursor.execute(sql, tuple_insert)
    get_db().commit()

    return redirect('/vehicule/show')

@app.route('/vehicule/delete')
def delete_vehicule():
    id = request.args.get('id', '')
    mycursor = get_db().cursor()
    sql = '''   DELETE FROM vehicule WHERE num_vehicule=%s;    '''
    turple_insert = (id)
    mycursor.execute(sql, turple_insert)
    get_db().commit()
    return redirect('/vehicule/show')

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
