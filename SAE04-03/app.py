from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/benne')
def benne():
    return render_template('benne.html')

@app.route('/passage')
def passage():
    return render_template('passage.html')

@app.route('/decharge')
def decharge():
    return render_template('decharge.html')

@app.route('/vehicule')
def vehicule():
    return render_template('vehicule.html')

if __name__ == '__main__':
    app.run()
