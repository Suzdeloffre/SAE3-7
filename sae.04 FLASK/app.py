from flask import Flask, render_template, redirect, g, request
import pymysql.cursors
app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host="localhost", # à modifier
            user="alexis", # à modifier
            password="Samsung21C!", # à modifier
            database="BDD_alexis", # à modifier
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
    mycursor = get_db().cursor()
    sql = '''   SELECT benne.id_benne, centre.nom_centre, benne.volume, benne.nb_benne, produit.libelle_produit
            FROM benne
            INNER JOIN centre ON benne.num_centre = centre.num_centre
            INNER JOIN produit ON benne.num_produit = produit.num_produit
            ORDER BY centre.nom_centre ASC;
                 '''
    mycursor.execute(sql)
    bennes = mycursor.fetchall()
    return render_template('benne/benne_show.html', bennes= bennes)

@app.route('/benne/add', methods=['GET'])
def add_benne():
    mycursor = get_db().cursor()
    sql = '''
        SELECT centre.num_centre AS id, centre.nom_centre AS nom, centre.adresse_centre AS adresse
        FROM centre;
        '''
    mycursor.execute(sql)
    centres = mycursor.fetchall()

    sql = '''
        SELECT produit.num_produit AS id, produit.libelle_produit AS nom
        FROM produit;
        '''
    mycursor.execute(sql)
    produits = mycursor.fetchall()
    return render_template('benne/benne_add.html', centres=centres, produits=produits)

@app.route('/benne/add', methods=['POST'])
def valid_add_benne():
    nbBenne = request.form.get('nbBenne')
    volume = request.form.get('volume')
    centre = request.form.get('centre')
    produit = request.form.get('produit')
    print(nbBenne, volume, centre, produit)
    mycursor = get_db().cursor()
    sql='''
    INSERT INTO benne(id_benne, nb_benne, volume, num_centre, num_produit) VALUES (NULL, %s, %s, %s, %s);
    '''
    tuple_insert=(nbBenne, volume, centre, produit)
    mycursor.execute(sql, tuple_insert)

    get_db().commit()
    return redirect('/benne/show')

@app.route('/benne/edit', methods=['GET'])
def edit_benne():
    id=request.args.get('id')
    if id != None and id.isnumeric():
        indice = int(id)
        mycursor = get_db().cursor()
        sql = '''
                SELECT id_benne, nb_benne, volume, num_centre, num_produit 
                FROM benne
                WHERE id_benne=%s;
                '''
        mycursor.execute(sql, indice)
        benne = mycursor.fetchone()

        sql = '''
                SELECT centre.num_centre AS id, centre.nom_centre AS nom, centre.adresse_centre AS adresse
                FROM centre;
                '''
        mycursor.execute(sql)
        centres = mycursor.fetchall()

        sql = '''
                SELECT produit.num_produit AS id, produit.libelle_produit AS nom
                FROM produit;
                '''
        mycursor.execute(sql)
        produits = mycursor.fetchall()

        get_db().commit()
    else:
        benne=[]
    return render_template('benne/benne_edit.html', benne=benne, centres=centres, produits=produits)

@app.route('/benne/edit', methods=['POST'])
def valid_edit_benne():
    id = request.form.get('id')
    nbBenne = request.form.get('nbBenne')
    volume = request.form.get('volume')
    centre = request.form.get('centre')
    produit = request.form.get('produit')

    mycursor = get_db().cursor()
    sql = '''
        UPDATE benne 
        SET nb_benne = %s, volume = %s, num_centre = %s, num_produit = %s
        WHERE id_benne = %s;
    '''
    tuple_insert=(nbBenne, volume, centre, produit, id)
    mycursor.execute(sql, tuple_insert)
    get_db().commit()

    return redirect('/benne/show')

@app.route('/benne/delete')
def delete_benne():
    id = request.args.get('id', '')
    mycursor = get_db().cursor()
    sql = '''   DELETE FROM benne WHERE id_benne=%s;    '''
    turple_insert = (id)
    mycursor.execute(sql, turple_insert)
    get_db().commit()
    return redirect('/benne/show')

# ---------------------------------------------------------------------#

@app.route('/vehicule/show')
def show_vehicule():
    mycursor = get_db().cursor()
    sql = '''   SELECT *
            FROM vehicule
            INNER JOIN type_vehicule ON vehicule.num_type = type_vehicule.num_type
            INNER JOIN marque ON vehicule.num_marque = marque.num_marque
            ORDER BY type_vehicule.libelle_type ASC;
                 '''
    mycursor.execute(sql)
    vehicules = mycursor.fetchall()
    return render_template('vehicule/vehicule_show.html', vehicules=vehicules)

@app.route('/vehicule/add', methods=['GET'])
def add_vehicule():
    mycursor = get_db().cursor()
    sql = '''
        SELECT type_vehicule.num_type AS id, type_vehicule.libelle_type AS libelle
        FROM type_vehicule;
        '''
    mycursor.execute(sql)
    type_vehicules = mycursor.fetchall()

    sql = '''
        SELECT marque.num_marque AS id, marque.libelle_marque AS libelle
        FROM marque;
        '''
    mycursor.execute(sql)
    marques = mycursor.fetchall()
    return render_template('vehicule/vehicule_add.html', type_vehicules=type_vehicules, marques=marques)

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
                SELECT *
                FROM vehicule
                WHERE num_vehicule=%s;
                '''
        mycursor.execute(sql, indice)
        vehicule = mycursor.fetchone()

        sql = '''
                SELECT *
                FROM type_vehicule;
                '''
        mycursor.execute(sql)
        type_vehicules = mycursor.fetchall()

        sql = '''
                SELECT *
                FROM marque;
                '''
        mycursor.execute(sql)
        marques = mycursor.fetchall()

        get_db().commit()
    else:
        vehicule=[]
    return render_template('vehicule/vehicule_edit.html', vehicule=vehicule, type_vehicules=type_vehicules, marques=marques)

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

@app.route('/vehicule/delete', methods=['GET'])
def delete_vehicule():
    id = request.args.get('id', '')
    mycursor = get_db().cursor()
    sql = '''   SELECT *
                FROM passage
                INNER JOIN centre ON passage.num_centre = centre.num_centre
                WHERE num_vehicule = %s
                ORDER BY passage.num_vehicule, passage.JMA, passage.ordre;
                     '''
    tuple_insert=(id)
    mycursor.execute(sql, tuple_insert)
    passagesV = mycursor.fetchall()

    sql = '''   SELECT *
                FROM decharge
                INNER JOIN produit ON decharge.num_produit = produit.num_produit
                INNER JOIN usine ON decharge.num_usine = usine.num_usine
                WHERE num_vehicule = %s
                ORDER BY decharge.JMA, usine.nom_usine;
                     '''
    tuple_insert = (id)
    mycursor.execute(sql, tuple_insert)
    dechargesV = mycursor.fetchall()

    if passagesV == () and dechargesV == ():
        sql = '''   DELETE FROM vehicule WHERE num_vehicule=%s;    '''
        turple_insert = (id)
        mycursor.execute(sql, turple_insert)
        get_db().commit()
        return redirect('/vehicule/show')
    else:
        return render_template('vehicule/vehicule_delete.html', id=id, passages=passagesV, decharges=dechargesV)

@app.route('/vehicule/delete/passage')
def valid_delete_passage():
    id = request.args.get('id')
    idV = request.args.get('idV')
    mycursor = get_db().cursor()
    sql = '''   DELETE FROM passage WHERE id_passage=%s;    '''
    mycursor.execute(sql, id)
    get_db().commit()
    return redirect('/vehicule/delete?id='+idV)

@app.route('/vehicule/delete/decharge')
def valid_delete_decharge():
    id = request.args.get('id', '')
    idV = request.args.get('idV')
    mycursor = get_db().cursor()
    sql = '''   DELETE FROM decharge WHERE id_decharge=%s;    '''
    turple_insert = (id)
    mycursor.execute(sql, turple_insert)
    get_db().commit()
    return redirect('/vehicule/delete?id='+idV)

@app.route('/vehicule/etat', methods=['GET'])
def etat_vehicule():
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
    return render_template('vehicule/vehicule_etat.html', vehicule=vehicule, type_vehicule=type_vehicule, marque=marque)

@app.route('/vehicule/edit', methods=['POST'])
def valid_etat_vehicule():
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

    return redirect('/vehicule/etat')


# ---------------------------------------------------------------------#

@app.route('/passage/show')
def show_passage():
    mycursor = get_db().cursor()
    sql = '''   SELECT *
            FROM passage
            INNER JOIN centre ON passage.num_centre = centre.num_centre
            INNER JOIN vehicule ON passage.num_vehicule = vehicule.num_vehicule
            ORDER BY passage.num_vehicule, passage.JMA, passage.ordre;
                 '''
    mycursor.execute(sql)
    passages = mycursor.fetchall()
    return render_template('passage/passage_show.html', passages=passages)

@app.route('/passage/add', methods=['GET'])
def add_passage():
    mycursor = get_db().cursor()
    sql = '''
        SELECT vehicule.num_vehicule AS id
        FROM vehicule
        ORDER BY id;
        '''
    mycursor.execute(sql)
    vehicules = mycursor.fetchall()

    sql = '''
        SELECT centre.num_centre AS id, centre.nom_centre AS nom, centre.adresse_centre
        FROM centre;
        '''
    mycursor.execute(sql)
    centres = mycursor.fetchall()
    return render_template('passage/passage_add.html', vehicules=vehicules, centres=centres)

@app.route('/passage/add', methods=['POST'])
def valid_add_passage():
    centre = request.form.get('centre')
    vehicule = request.form.get('vehicule')
    ordre = request.form.get('ordre')
    date_passage = request.form.get('date_passage')
    mycursor = get_db().cursor()
    sql='''
    INSERT INTO passage(id_passage, num_centre, num_vehicule, JMA, ordre)
     VALUES (NULL, %s, %s, %s, %s);
    '''
    tuple_insert=(centre, vehicule, date_passage, ordre)
    mycursor.execute(sql, tuple_insert)

    get_db().commit()
    return redirect('/passage/show')

@app.route('/passage/edit', methods=['GET'])
def edit_passage():
    id=request.args.get('id')
    if id != None and id.isnumeric():
        indice = int(id)
        mycursor = get_db().cursor()
        sql = '''
                SELECT *
                FROM passage
                WHERE id_passage=%s;
                '''
        mycursor.execute(sql, indice)
        passage = mycursor.fetchone()

        sql = '''
                SELECT vehicule.num_vehicule AS id
                FROM vehicule
                ORDER BY id;
                '''
        mycursor.execute(sql)
        vehicules = mycursor.fetchall()

        sql = '''
                SELECT centre.num_centre AS id, centre.nom_centre AS nom, centre.adresse_centre
                FROM centre;
                '''
        mycursor.execute(sql)
        centres = mycursor.fetchall()

        get_db().commit()
    else:
        vehicule=[]
    return render_template('passage/passage_edit.html', vehicules=vehicules, passage=passage, centres=centres)

@app.route('/passage/edit', methods=['POST'])
def valid_edit_passage():
    id = request.form.get('id')
    centre = request.form.get('centre')
    vehicule = request.form.get('vehicule')
    ordre = request.form.get('ordre')
    date_passage = request.form.get('date_passage')

    mycursor = get_db().cursor()
    sql = '''
        UPDATE passage
        SET num_vehicule = %s, JMA = %s, ordre = %s, num_centre = %s
        WHERE id_passage = %s;
    '''
    tuple_insert=(vehicule, date_passage, ordre, centre, id)
    mycursor.execute(sql, tuple_insert)
    get_db().commit()

    return redirect('/passage/show')

@app.route('/passage/delete')
def delete_passage():
    id = request.args.get('id', '')
    mycursor = get_db().cursor()
    sql = '''   DELETE FROM passage WHERE id_passage=%s;    '''
    turple_insert = (id)
    mycursor.execute(sql, turple_insert)
    get_db().commit()
    return redirect('/passage/show')

# ---------------------------------------------------------------------#

@app.route('/decharge/show')
def show_decharge():
    mycursor = get_db().cursor()
    sql = '''   SELECT *
            FROM decharge
            INNER JOIN produit ON decharge.num_produit = produit.num_produit
            INNER JOIN vehicule ON decharge.num_vehicule = vehicule.num_vehicule
            INNER JOIN usine ON decharge.num_usine = usine.num_usine
            ORDER BY decharge.JMA, usine.nom_usine;
                 '''
    mycursor.execute(sql)
    decharges = mycursor.fetchall()
    return render_template('decharge/decharge_show.html', decharges=decharges)

@app.route('/decharge/add', methods=['GET'])
def add_decharge():
    mycursor = get_db().cursor()
    sql = '''
        SELECT vehicule.num_vehicule AS id
        FROM vehicule
        ORDER BY id;
        '''
    mycursor.execute(sql)
    vehicules = mycursor.fetchall()

    sql = '''
        SELECT produit.num_produit AS id, produit.libelle_produit AS nom
        FROM produit;
        '''
    mycursor.execute(sql)
    produits = mycursor.fetchall()

    sql = '''
            SELECT usine.num_usine AS id, usine.nom_usine AS nom, usine.adresse_usine AS adresse
            FROM usine;
            '''
    mycursor.execute(sql)
    usines = mycursor.fetchall()
    return render_template('decharge/decharge_add.html', vehicules=vehicules, produits=produits, usines=usines)

@app.route('/decharge/add', methods=['POST'])
def valid_add_decharge():
    usine = request.form.get('usine')
    vehicule = request.form.get('vehicule')
    quantite = request.form.get('quantite')
    date_decharge = request.form.get('date_decharge')
    produit = request.form.get('produit')
    mycursor = get_db().cursor()
    sql='''
    INSERT INTO decharge(id_decharge, num_usine, num_vehicule, num_produit, JMA, quantite)
     VALUES (NULL, %s, %s, %s, %s, %s);
    '''
    tuple_insert=(usine, vehicule, produit, date_decharge, quantite)
    mycursor.execute(sql, tuple_insert)

    get_db().commit()
    return redirect('/decharge/show')

@app.route('/decharge/edit', methods=['GET'])
def edit_decharge():
    id=request.args.get('id')
    if id != None and id.isnumeric():
        indice = int(id)
        mycursor = get_db().cursor()
        sql = '''
                SELECT *
                FROM decharge
                WHERE id_decharge=%s;
                '''
        mycursor.execute(sql, indice)
        decharge = mycursor.fetchone()

        sql = '''
                SELECT vehicule.num_vehicule AS id
                FROM vehicule
                ORDER BY id;
                '''
        mycursor.execute(sql)
        vehicules = mycursor.fetchall()

        sql = '''
                SELECT produit.num_produit AS id, produit.libelle_produit AS nom
                FROM produit;
                '''
        mycursor.execute(sql)
        produits = mycursor.fetchall()

        sql = '''
                    SELECT usine.num_usine AS id, usine.nom_usine AS nom, usine.adresse_usine AS adresse
                    FROM usine;
                    '''
        mycursor.execute(sql)
        usines = mycursor.fetchall()

        get_db().commit()
    else:
        vehicule=[]
    return render_template('decharge/decharge_edit.html', decharge=decharge, vehicules=vehicules, produits=produits, usines=usines)

@app.route('/decharge/edit', methods=['POST'])
def valid_edit_decharge():
    id = request.form.get('id')
    usine = request.form.get('usine')
    vehicule = request.form.get('vehicule')
    quantite = request.form.get('quantite')
    date_decharge = request.form.get('date_decharge')
    produit = request.form.get('produit')

    mycursor = get_db().cursor()
    sql = '''
        UPDATE decharge
        SET num_vehicule = %s, JMA = %s, quantite = %s, num_usine = %s, num_produit=%s
        WHERE id_decharge = %s;
    '''
    tuple_insert=(vehicule, date_decharge, quantite, usine, produit, id)
    mycursor.execute(sql, tuple_insert)
    get_db().commit()

    return redirect('/decharge/show')

@app.route('/decharge/delete')
def delete_decharge():
    id = request.args.get('id', '')
    mycursor = get_db().cursor()
    sql = '''   DELETE FROM decharge WHERE id_decharge=%s;    '''
    turple_insert = (id)
    mycursor.execute(sql, turple_insert)
    get_db().commit()
    return redirect('/decharge/show')

# ---------------------------------------------------------------------#

if __name__ == '__main__':
    app.run()
