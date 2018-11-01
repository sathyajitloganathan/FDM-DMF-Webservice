import time
import flask
import requests
import logging
from flask import request, jsonify
import ModelBuilding as mb
import numpy as np
import pandas as pd
# from flask_cors import CORS

# logging.getLogger('flask_cors').level = logging.DEBUG
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app=flask.Flask(__name__)
# CORS(app)

clf = mb.import_model()

@app.route('/', methods = ['GET'])
def home():
    return """Hello, FDM!!!"""

@app.route('/welcome', methods = ['GET'])
def welcome():
    return """Welcome to this Web Service. Utilizable for  Direct Mail Fundraising Donor identification prediction based on the input features you send."""

@app.route('/prediction/single', methods = ['POST'])
def prediction_single():
    data = request.get_json(force = True)
    #return {'value':data['w']}
    try:
        if "singleRecord" in data:
            if data['singleRecord']=="True":
                singRec = []
                for key,value in data["attributes"].items():
                    singRec.append(value)

                formRec = np.array(singRec).reshape(1,-1)
                pred = clf.predict(formRec)
                print(pred)
                #return ('Prediction Completed',200)
                return jsonify({"isDonor":int(pred),
                                "Profit":13-0.68,
                                "Expense":0.68,})
    except Exception as e:
        print(e)
        return "Exception: " + str(e)

@app.route('/prediction/file', methods = ['POST'])
def bulk_prediction():
    #return(data['withHeader'])
    try:
        if request.form['filetype'] == 'csv':
            if request.form['withHeader'] == 'True':
                fileobject = request.files.get('file')
                X = pd.read_csv(fileobject,header=0)
            elif request.form['withHeader'] == 'False':
                fileobject = request.files.get('file')
                X = pd.read_csv(fileobject)
            print(X)
            X = X.drop(['TARGET_B','Row Id','Row Id.','TARGET_D'],axis=1)
            predictions = clf.predict(X)

            donorCount = int(sum(predictions))
            nonDonorCount = int(len(X)-sum(predictions))

            return jsonify({
                "DonorCount":donorCount,
                "NonDonorCount":nonDonorCount,
                "Profit": float(donorCount*13) - float(nonDonorCount*0.68),
                "Expense": float(len(X)*0.68)
            })
        elif request.form['filetype'] == 'excel':
            if request.form['withHeader'] == 'True':
                fileobject = request.files.get('file')
                X = pd.read_excel(fileobject,sheetname=0)
            elif request.form['withHeader'] == 'False':
                fileobject = request.files.get('file')
                X = pd.read_csv(fileobject)
            print(X)
            X = X.drop(['TARGET_B','Row Id','Row Id.','TARGET_D'],axis=1)
            predictions = clf.predict(X)

            donorCount = int(sum(predictions))
            nonDonorCount = int(len(X)-sum(predictions))

            return jsonify({
                "DonorCount":donorCount,
                "NonDonorCount":nonDonorCount,
                "Profit": float(donorCount*13) - float(nonDonorCount*0.68),
                "Expense": float(len(X)*0.68)
            })

    except Exception as e:
        print(e)
        return "Exception: " + str(e)


if __name__ == '__main__':
    print("Excited")
    # clf = mb.import_model()
    # app.run(host='0.0.0.0',port=800,debug=True, threaded=True, use_reloader=False)
    app.run(host='0.0.0.0',port=800,debug=True)
