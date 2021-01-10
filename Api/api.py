from flask import Flask, render_template, redirect,request,url_for
from flask_restful import reqparse, abort, Api, Resource
import pickle
import pandas as pd
import numpy as np 

app = Flask(__name__, template_folder="templates")
api = Api(app)

#arguments qui sont passés dans l'url de l'api
put_args = reqparse.RequestParser()
put_args.add_argument("apm", type=str, help="apm manquant", required = True)
put_args.add_argument("selectbyhotkeys", type=str, help="selectbyhotkeys manquant", required = True)
put_args.add_argument("assigntohotkeys", type=str, help="assigntohotkeys manquant", required = True)
put_args.add_argument("uniquehotkeys", type=str, help="uniquehotkeys manquant", required = True)
put_args.add_argument("minimapattacks", type=str, help="minimapattacks manquant", required = True)
put_args.add_argument("minimaprightclicks", type=str, help="minimaprightclicks manquant", required = True)
put_args.add_argument("numberofpacs", type=str, help="numberofpacs manquant", required = True)
put_args.add_argument("gapbetweenpacs", type=str, help="gapbetweenpacs manquant", required = True)
put_args.add_argument("actionlatency", type=str, help="actionlatency manquant", required = True)
put_args.add_argument("actionsinpac", type=str, help="actionsinpac manquant", required = True)
put_args.add_argument("totalmapexplored", type=str, help="totalmapexplored manquant", required = True)
put_args.add_argument("workersmade", type=str, help="workersmade manquant", required = True)



class API(Resource):
    def get(self):
        args = put_args.parse_args()
        X = [float(args.apm), float(args.selectbyhotkeys), float(args.assigntohotkeys), float(args.uniquehotkeys), float(args.minimapattacks),
            float(args.minimaprightclicks), float(args.numberofpacs), float(args.gapbetweenpacs), float(args.actionlatency), float(args.actionsinpac),
            float(args.totalmapexplored), float(args.workersmade)]
        RandomF = pickle.load( open( "randomF.p", "rb" ) ) 
        RandomF_pred = RandomF.predict([X]) #prediction du modele
        pred = int(RandomF_pred[0]) 
        if pred < 0:
            pred = 1
        if pred > 7:
            pred = 7
        Leagues = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Master','GrandMaster', 'Professional']
        return redirect( url_for('result', league = Leagues[pred])) 

api.add_resource(API, "/api/") 

@app.route('/')
def main(): #page principale
    return render_template("menu.html")

@app.route('/result') #page resultat de la league prédit
def result():
    resultat = request.args.get('league') 
    return render_template("sortie.html", league = resultat)


if __name__ == '__main__':
    app.run(debug=True)