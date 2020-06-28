from flask import Flask,request, Response
from flask_pymongo import PyMongo
from datetime import datetime
from bson import json_util
from bson.objectid import ObjectId
#from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/proyecto_V'

mongo = PyMongo(app)

@app.route('/api/user/add_pacient', methods = ['POST']) #Agregar un Paciente al sistema 
def create_patient():
    
    Nombre    = request.json['Nombre']
    Apellido  = request.json['Apellido']
    Cc        = request.json['Cc']
    Sexo      = request.json['Sexo']
    Edad      = request.json['Edad']
    Gafas     = request.json['Gafas']
    Dominante = request.json['Dominante']
    
    
    if  Nombre and Apellido and Cc and Sexo and Dominante and Edad and Gafas:

        integer = int(Cc)
        user = mongo.db.pacientes.find({'CC': integer})
        response = json_util.dumps(user)

        try:
            validator = response[2]
            print(validator)

            response = {
                'message':'El paciente ya se encuentra en el sistema '
            }

            return response
            
            
            
        
        except:

            now = datetime.now()
            Fecha = (now.strftime("%m/%d/%Y"))
            mongo.db.pacientes.insert(
            { 'Nombre': Nombre,'Apellido': Apellido,'CC': int(Cc),'Sexo': Sexo,'Edad': Edad,'Gafas': Gafas,'Dominante' : Dominante ,'Fecha': Fecha}
             )

            response = {
                'message':'Paciente agregado'
            }

            return response

    
    else:
        message ={

            'message':'Campos invalidos'
        }
        return message

@app.route('/api/user/list', methods = ['GET'])  #Poder ver todos los pacientes del sistema 
def get_all_patients():
   users = mongo.db.pacientes.find()
   response = json_util.dumps(users)
   return  Response(response ,mimetype='application/json')

@app.route('/api/user/list/one_user/<CC>', methods = ['GET']) # poder ver un unico Paciente del sistrema
def get_patient(CC):
    integer = int(CC)
    user = mongo.db.pacientes.find({'CC': integer})
    response = json_util.dumps(user)
    return Response(response ,mimetype='application/json')


@app.route('/api/user/add_user',methods =['POST']) # Agregar un usuario al sistema para hacer un login 
def create_user():

    Nombre      = request.json['Nombre']
    Usuario     = request.json['Usuario']
    Contrasena  = request.json['Contrasena']
    Contrasena2 = request.json['Contrasena2']

    if Nombre and Usuario and Contrasena:

        if ( str(Contrasena) == str(Contrasena2)):
            string = str(Usuario)
            user   = mongo.db.logins.find({'usuario':string})
            user_j = json_util.dumps(user) 


            try:
                validator = user_j[2]
                print(validator)
                response = {
                    'message':'Usuario ya exitente'
                }
        
            
                return(response)

            except:
                
                mongo.db.logins.insert(
                    {
                        'nombre'     : Nombre,
                        'usuario'    : Usuario,
                        'contrasena' : Contrasena             
                    }
                )
                response = {
                    'message':'Usuario agregado'
                }
        
            
                return(response)
        else:

            response = {
                'message':'Las contrasenas no son iguales '
            }
         
            return(response)
    else:
        response = {
            'message':'Datos invalidos '
        }
        
            
        return(response)


@app.route('/api/user/login_user',methods = ['GET']) #Ver si el usuario esta en el sistema "Hacer Login" 
def search_user():
    Usuario    = request.json['Usuario']
    Contrasena = request.json['Contrasena'] 
    

    if Usuario and Contrasena:


        user   = mongo.db.logins.find_one({'usuario':str(Usuario),'contrasena':str(Contrasena)})
        user_j = json_util.dumps(user) 

        try:
            validator = user_j[2]
            print(validator)

            response = {
                'message':'Logeado'

            }
            print("logeado")
            return Response(user_j  ,mimetype='application/json')

        except:

            response = {
                'message':'Usuario o Contrasena erroneo'

            }
            print("no logeado")
            return Response(user_j ,mimetype='application/json')
            
        
    else:
        response = {
            'message':'Datos invalidos '
        }
        
            
        return(response)


@app.route('/api/user/delete_user/<id>',methods = ['DELETE']) #Eliminar un usuario mediante el id asigando por mongo
def delete_user(id):

    ID = ObjectId(id)
    user = mongo.db.logins.find({'_id': ID})
    user_j = json_util.dumps(user) 

    try:
        validator = user_j[2]
        print validator
        mongo.db.logins.delete_one({'_id': ObjectId(id)})
        return "Usuario Eliminado"
    except:
        return "No hay usuario en el sistema"

@app.route('/api/user/delete_pacient/<cc>',methods = ['DELETE']) # Eliminar un paciente del sistema
def delete_pacient(cc):

    integer = int(cc)
    user = mongo.db.pacientes.find({'CC': integer})
    user_j = json_util.dumps(user)

    try:
        validator = user_j[2]
        print validator
        mongo.db.pacientes.delete_one({'CC': integer})
        return "Paciente eliminado "
    except:
        return "No se encontro usuario"


@app.route('/api/user/update_user_pass/<id>',methods = ['PATCH'])# cambiar la contrasena de usuario
def update_user(id):

    ID = ObjectId(id)
    user = mongo.db.logins.find({'_id': ID})
    user_j = json_util.dumps(user) 
    contra = request.json['Contrasena']
    try:
        validator = user_j[2]
        print validator
        mongo.db.logins.update_one({'_id':ObjectId(id)},{'$set':{'contrasena':contra}})  
        return "Contrasena modificada"

    except:
        return "No hay usuario en el sistema"
 
if __name__ == "__main__":
    app.run(debug=True)