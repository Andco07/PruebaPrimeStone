from functools import update_wrapper
from re import I
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy as aldb
import json

from sqlalchemy.orm import session

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:andcoy07@localhost:5432/pruebadev'
db = aldb(app)

class persona(db.Model):
    __tablename__ = "personas"
    id_persona = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(), nullable = False)

    def __init__(self, id_persona, nombre):
        self.id_persona = id_persona
        self.nombre = nombre

class Estatura:
    def __init__(self,name,height):

        self.name = name
        self.height = height

@app.route('/api/get-prime-numbers', methods = ['GET'])
def numberprimos():
    num = int(request.args.get("number"))
    primoslist = []
    for i in range(2, num + 1):
        primos = True
        for j in range(2,11):
            if i == j:
                break
            elif i%j == 0:
                primos = False
            else:
                continue
        if primos == True:
            primoslist.append(i)
    return jsonify(primoslist)

@app.route('/api/convert-height', methods = ['POST'])
def convert_height():
    datos = request.get_json()
    estatura = datos["height"]
    numbers = [int(temp)for temp in estatura.split() if temp.isdigit()]
    estatura_metros =  str(round(float(numbers[0]/39.37),2))
    Est =  Estatura(name=datos["name"], height= estatura_metros)
    result = json.dumps(Est.__dict__)
    return (result)
    
@app.route('/api/set-data', methods = ['PUT'])
def editperson():
    datos = request.get_json()
    id_per = int(datos["id_persona"])
    person = db.session.query(persona)
    person = person.filter(persona.id_persona == id_per)
    record = person.one()
    record.nombre = request.json['nombre']
    record.id_persona = id_per
    db.session.merge(record)
    db.session.commit()
    return jsonify(datos)

if __name__ == '__main__':
    app.run(port = 3000, debug = True) 
