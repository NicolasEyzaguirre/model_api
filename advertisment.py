
from flask import Flask, request, jsonify
import os
import pickle
from sklearn.model_selection import cross_val_score
import pandas as pd
import sqlite3



os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido a mi API del modelo advertising"


# 1. Ofrezca la predicción de ventas a partir de todos los valores de gastos en publicidad. (/v2/predict)

@app.route('/v2/predict', methods=['GET'])
def predict():
    model = pickle.load(open('data/advertising_model','rb'))

    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)

    if tv is None or radio is None or newspaper is None:
        return "Missing args, the input values are needed to predict"
    else:
        prediction = model.predict([[tv,radio,newspaper]])
        return "The prediction of sales investing that amount of money in TV, radio and newspaper is: " + str(round(prediction[0],2)) + 'k €'

# 2. Un endpoint para almacenar nuevos registros en la base de datos que deberá estar previamente creada.(/v2/ingest_data)

@app.route('/api/v2/ingest_data', methods=['GET'])
def get_all():
    connection = sqlite3.connect('campaña.db')
    cursor = connection.cursor()
    if 'title' not in request.args and 'published' not in request.args and 'author' not in request.args:
        return "Filters missing"
    else:
        tv = request.args.get('tv', None)
        radio = request.args.get('radio', None)
        newspaper = request.args.get('newspaper', None)

        add_to_campaña = '''
        INSERT INTO campaña (TV) VALUES ('''+tv+''')
        INSERT INTO campaña (radio) VALUES ('''+radio+''')
        INSERT INTO campaña (newspaper) VALUES ('''+newspaper+''')'''

        result = cursor.execute(add_to_campaña).fetchall()
        connection.close()
        return jsonify(result)



# 3. Posibilidad de reentrenar de nuevo el modelo con los posibles nuevos registros que se recojan. (/v2/retrain)

