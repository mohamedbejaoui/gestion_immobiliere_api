# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from flask import Flask, request, jsonify, make_response
#request pour avoir le data de la request, jsonify pour retourner de l'information à l'utilisateur
from flask_sqlalchemy import SQLAlchemy #choix de la base de donnée
import jwt #création du token
import datetime #expiration du token (j'ai choisi un temps d'expiration de 30 minutes pour chaque utilisateur connecté)
from functools import wraps #va servir pour le token decorator


app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Mohamed/Documents/api rest/test.db'

db=SQLAlchemy(app)

class Utilisateur(db.Model): #table utilisateur(j'ai ajouté un pseudo et un mot de passe pour pouvoir gérer les autorisations)
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nom = db.Column(db.String(25)) 
    prenom = db.Column(db.String(25))
    date_naissance = db.Column(db.String(10))
    pseudo = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    
class Bien_Immobilier(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nom = db.Column(db.String(50))
    description = db.Column(db.String(1000))
    type_bien = db.Column(db.String(30))
    ville = db.Column(db.String(25))
    pieces = db.Column(db.Integer)
    carac_pieces = db.Column(db.String(250))
    proprietaire_id = db.Column(db.Integer) #correspond à l'id de l'utilisateur qui va créer ce bien
    
#token decorator
########################
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs): #inner decoration
        token = None #empty token

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Utilisateur.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        #pass user object to the route
        return f(current_user, *args, **kwargs)
        
    return decorated
#########################

#créer un nouvel utilisateur (pas besoin d'autorisation)
@app.route('/user', methods=['POST'])
def creer_utilisateur():
    data = request.get_json() 
    nouvel_util = Utilisateur(nom=data['nom'], prenom=data['prenom'], date_naissance=data['date_naissance'], pseudo=data['pseudo'], password=data['password'])
    db.session.add(nouvel_util)
    db.session.commit()
    
    return jsonify({'message' : 'Nouvel utilisateur cree!', 'Voici votre id' : nouvel_util.id})

#renseigner un bien par un utilisateur qui devient donc propriétaire
@app.route('/bien_immobilier', methods=['POST'])
@token_required
def renseigner_bien(current_user):
    data = request.get_json()
    nouveau_bien = Bien_Immobilier(nom=data['nom'],description=data['description'],type_bien=data['type_bien'],ville=data['ville'],pieces=data['pieces'],carac_pieces=data['carac_pieces'],proprietaire_id=current_user.id)
    
    db.session.add(nouveau_bien)
    db.session.commit()
    
    return jsonify({'message': 'Nouveau bien cree!', 'Voici l''id de votre bien' : nouveau_bien.id})

#consulter les biens par un utilisateur en indiquant une ville (pas besoin d'autorisation) 
@app.route('/bien_immobilier/<ville>', methods=['GET'])
def consulter_bien(ville):
    biens = Bien_Immobilier.query.filter_by(ville=ville).all()
    
    if not biens:
        return jsonify({'message' : 'Aucun bien trouve dans cette ville!'})
    
    output = [] #puisqu'on ne peut pas entrer une requête sqlalchemy dans un object json directement
    
    for bien in biens:
        bien_data = {}
        bien_data['id'] = bien.id
        bien_data['nom'] = bien.nom
        bien_data['description'] = bien.description
        bien_data['type_bien'] = bien.type_bien
        bien_data['ville'] = bien.ville
        bien_data['pieces'] = bien.pieces
        bien_data['carac_pieces'] = bien.carac_pieces
        bien_data['proprietaire_id'] = bien.proprietaire_id
        output.append(bien_data)
        
    return jsonify({'biens' : output})

#modifier les caractéristiques d'un bien par le propriétaire seulement(autorisation requise)
@app.route('/bien_immobilier/<int:bien_id>', methods=['PUT'])
@token_required
def modifier_bien(current_user, bien_id):
    
    bien = Bien_Immobilier.query.filter_by(id=bien_id).first()   
    
    if not bien:
        return jsonify({'message' : 'Le bien que vous voulez modifier n''existe pas!'})    
    
    if current_user.id != bien.proprietaire_id:
        return jsonify({'message' : 'Modification non autorisee!, Vous n''etes pas le proprietaire de ce bien'})
    
    data = request.get_json()
    if 'nom' in data.keys():
        bien.nom = data['nom'] 
    if 'description' in data.keys():
        bien.nom = data['description'] 
    if 'type_bien' in data.keys():
        bien.nom = data['type_bien'] 
    if 'ville' in data.keys():
        bien.nom = data['ville'] 
    if 'pieces' in data.keys():
        bien.nom = data['pieces'] 
    if 'carac_pieces' in data.keys():
        bien.nom = data['carac_pieces'] 
    
    db.session.commit()
    
    return jsonify({'message': 'Caracteristiques du bien modifiees!'})

#modifier les coordonnées personnels d'un utilisateur par lui même seulement
@app.route('/user/<int:user_id>', methods=['PUT'])
@token_required
def modifier_utilisateur(current_user, user_id):
    if current_user.id != user_id:
        return jsonify({'message' : 'Modification non autorisee!, Vous ne pouvez pas modifier les informations d''un autre utilisateur'})
    
    utilisateur = Utilisateur.query.filter_by(id=user_id).first()
    
    if not utilisateur:
       return jsonify({'message' : 'Utilisateur non trouve!'})
    
    data = request.get_json()
    if 'nom' in data.keys():
        utilisateur.nom = data['nom'] 
    if 'prenom' in data.keys():    
        utilisateur.prenom = data['prenom'] 
    if 'date_naissance' in data.keys():
        utilisateur.date_naissance = data['date_naissance'] 
    db.session.commit()
    
    return jsonify({'message': 'Informations modifiees!'})
    
#chaque utilisateur doit se connecter pour pouvoir exécuter des fonctions qui demandent une autorisation
@app.route('/login')
def login():
    auth = request.authorization
    #Si aucune authentification n'est faite
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic real="Login required!"'})   
    
    utilisateur = Utilisateur.query.filter_by(password=auth.password).first()
    
    #Si l'utilisateur est introuvable
    if not utilisateur:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic real="Login required!"'})
    
    if utilisateur.password == auth.password:
        token = jwt.encode({'id':utilisateur.id, 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})
    
    #Si le mot de passe n'est pas correct
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic real="Login required!"'}) 

if __name__ == '__main__':
    app.run(debug=True)

