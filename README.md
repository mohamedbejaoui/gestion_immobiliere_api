# Création d'une API REST pour une gestion immobilière

## Présentation du projet

#### Problématique:
Ce projet a pour but de créer un ensemble de microservices qui doivent permetre à un utilisateur d'intéragir avec une plateforme en assurant les fonctionnalités suivantes:

- Un utilisateur peut renseigner un bien immobilier avec les caractéristiques suivantes: (nom, description, type de bien, ville, pièces, caractéristiques des pièces, propriétaire). Cet utilisateur devient donc propriétaire de ce bien. Il peut aussi modifier les caractéristiques de son bien **mais** pas celles des autres biens dont il n'est pas propriétaire.

- Un utilisateur peut consulter les biens disponibles sur la plateforme **uniquement** pour une **ville particulière**.

- Un utilisateur peut renseigner / modifier ses informations personnelles sur la plateforme (nom, prénom, date de naissance). **En revanche**, il ne peut ni accéeder ni modifier les informations des autres utilisateurs.

#### Objectif:
Créer un microservice avec une API REST qui permet aux utilisateurs de réaliser toutes les fonctionnalités citées ci-dessus. Je ne vais pas développer une interface pour ce projet.

#### Choix technologiques:
- Language: Python
- Framework: Flask
- Base de données: **relationnelle** en utilisant le module **SQLAlchemy** de Python

## Conditions préalables:
Pour pouvoir faire fonctionner le programme localement, On va utiliser les logiciels suivants: (Vous devez donc installer ce que vous manque )

- **Python** (avec les modules: flask, flask_sqlalchemy, jwt, datetime et functools)
- **curl** qui set pour la syntaxe des requêtes à envoyer au serveur
- **Git Bash** sui sert à envoyer les requêtes vers le serveur
- **sqlite3**
- Et bien sûr l'**invite des commande**.

## Étapes de fonctionnement:

Le code python qui contient toutes les fonctions nécessaires au fonctionnement du programme s'appelle **app.py**.

-  Une fois que vous avez téléchargé tous les fichiers présents dans le repository(sauf le fichier images qui sert que pour le Readme) en dessus de Readme, mettez les dans le même chemin. Ensuite, ouvrez l'invite des commande et assurez vous que vous travaillez dans le chemin qui contient vos fichiers téléchargés.

- Tapez les commandes suivantes:
'''
python
from app import db
db.create_all()
exit()
'''
Ceci permet de créer les deux tables présentes dans le code app.py; la table **Utilisateur** et la table **Bien_Immobilier**.

![](https://github.com/mohamedbejaoui/gestion_immobiliere_api/blob/master/images/image1.PNG)

Pour tester que vous avez bien créer les deux tables, tapez les commandes suivantes:
'''
sqlite3 test.db
.tables
.exit
'''
En fait, les deux tables crées sont stockés dans test.db qui se trouve maintenant dans votre
chemin de travail.

IMAGE2 !!!

- Maintenant, on doit lancer notre serveur. Pour cela, tapez la commande suivante toujours dans l'invite des commandes:
'''
python app.py
'''

IMAGE3 !!!

- Le serveur étant lancé, nous pouvons maintenant commencer à envoyer les requêtes. Pour cela, ouvrez **Git Bash**.

- Commençons par créer un utilisateur avec les caractéristiques suivantes par exemple:
  - *nom:* Durand
  - *prénom:* Benoit
  - *date de naissance:* 22-05-1994
  Pour respecter certains critères de la problématique, j'ai ajouté deux autres colonnes à la table Utilisateur:
  - *pseudo:* benoitdurand
  - *password:* 12345

  Pour envoyer la requête, taper le code suivant dans Git Bash. D'ailleurs, toutes les requêtes qu'on va envoyer au serveur vont être tapées dans Git Bash. Ca s'appliquera donc pour tous les codes qui vont suivre.
  '''
  curl -i -H "Content-Type: application/json" -X POST -d '{"nom":"Durand","prenom":"Benoit","date_naissance":"22-05-1994","pseudo":"benoitdurand","password":"12345"}' http://127.0.0.1:5000/user
  '''
  Vous devez avoir le message suivant:

  IMAGE4!!!

  L'utilisateur est donc crée. Vous pouvez retenir son id pour une utilisation ultérieure.

- Créons un autre utilisateur. Ca va être utile pour tester les contraintes.
  Par exemple, on va choisir comme informations personnelles:
  - *nom:* Martin
  - *prénom:* Thomas
  - *date de naissance:* 14-06-1991
  - *pseudo:* thomasmartin
  - *password:* azerty   
  Tapez le code suivant:
  '''
  curl -i -H "Content-Type: application/json" -X POST -d '{"nom":"Martin","prenom":"Thomas","date_naissance":"14-06-1991","pseudo":"thomasmartin","password":"azerty"}' http://127.0.0.1:5000/user
  '''
  Vous devez avoir le message suivant:

  IMAGE5!!!

- Avant de passer à la création de biens, un utilisateur doit d'abord se connecter au serveur avec son pseudo et son mot de passe. Pour cela, si M.Durand essaye de se connecter, il doit taper ce code:
'''
curl -u benoitdurand:12345 -i http://127.0.0.1:5000/login
'''
Vous recevez donc un token comme suit:

IMAGE 6 !!!

Ce token va gérer les contraintes citées dans la problématique comme on va voir plus tard. Il va permettre à M.Durand de rester connecté pendant **30 minutes**. Au delà de cette période, il va **expirer**.

- Maintenant qu'on est connecté en tant que M.Durand à l'aide du token qu'on a reçu, essayons de créer le premier bien que M.Durand va donc devenir propriétaire.
On va choisir par exemple les caractéristiques suivantes:
  - *nom:* Appartement 36mcarre Paris 15eme
  - *description:* A louer charmant appartement meuble de 36mcarre a proximite immediate de la gare Montparnasse
  - *type_bien:* appartement
  - *ville:* Paris
  - *pieces:* 2
  - *Carac_piece:* un salon et une chambre
Tapez donc le code suivant:
'''
curl -i -H "Content-Type: application/json" -X POST -d '{"nom":"Appartement 36mcarre Paris 15eme","description":"A louer charmant appartement meuble de 36mcarre a proximite immediate de la gare Montparnasse","type_bien":"appartement","ville":"Paris","pieces":2,"carac_pieces":"un salon et une chambre"}' http://127.0.0.1:5000/bien_immobilier --header "x-access-token:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTM0MTkxNjk5fQ.EOxCREIhYMlduhKJ40sW6oEtXgae83u4PYbobR4obwQ""
'''
Mettez le token que vous avez reçu au lieu de celui que j'ai mis dans le code.
Vous devez avoir le message suivant:

IMAGE7!!!

Le bien est donc crée. Son id est 1.

- Essayons de consulter ce bien. N'importe quel utilisateur peut consulter les biens; on n'a donc pas besoin de token. En revanche, on doit indiquer le nom de la ville. Dans notre cas, on n'a encore qu'un seul bien se trouvant à Paris.
Tapez le code suivant:
'''
curl -i http://127.0.0.1:5000/bien_immobilier/"Paris"
'''
Vous devez voir le message suivant:

IMAGE 8!!!

- Essayons maintenant de cahnger par exemple *type_bien* de appartement à maison. On est connecté en tant que M.Durand qui est propriétaire du bien 1. On sera donc capable de le faire. Voici le code:
'''
curl -i -H "Content-Type: application/json" -X PUT -d '{"type_bien":"maison"}' http://127.0.0.1:5000/bien_immobilier/1 --header "x-access-token:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTM0MTkxNjk5fQ.EOxCREIhYMlduhKJ40sW6oEtXgae83u4PYbobR4obwQ""
'''

Voud devez voir le message suivant:

IMAGE 9!!!

On a donc modifié les caractéristiques du bien. Vous pouvez le vérifier en consultant à nouveau la liste des biens à Paris.

- Maintenant, on va se connecter en tant que M.Martin. On va essayer de modifier le bien de M.Durand pour vérifier que ça ne va pas fonctionner.
Pour se connecter:
'''
curl -u thomasmartin:azerty -i http://127.0.0.1:5000/login
'''
Retenez le token et utilisez le dans la requête suivante:(On va essayer de changer *pieces* de 2 à 2)
'''
curl -i -H "Content-Type: application/json" -X PUT -d '{"pieces":3}' http://127.0.0.1:5000/bien_immobilier/1 --header "x-access-token:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZXhwIjoxNTM0MTkzMTYyfQ.WMN8YUHmnN1fWuQS4pBFJSX15Fta4yIn8AiRV9qtZSI""
'''
Voici le message renvoyé:

IMAGE 10 !!!

On voit bien que la modification n'est pas autorisée car M.Martin n'est pas propriétaire du bien 1.

- Il nous reste donc de voir comment modifier les informations personnelles d'un utilisateur.
M.Martin va essayer de changer sa date de naissance comme suit:
'''
curl -i -H "Content-Type: application/json" -X PUT -d '{"date_naissance":"21-07-1995"}' http://127.0.0.1:5000/user/2 --header "x-access-token:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZXhwIjoxNTM0MTkzMTYyfQ.WMN8YUHmnN1fWuQS4pBFJSX15Fta4yIn8AiRV9qtZSI""
'''
Message renvoyé:

IMAGE11!!!

Les modifications sont donc apportées car l'id dans le requête correspond à l'id de M.Martin(2).

Maintenant, M.Martin va essayer de changer les informations de M.Durand. IL suffit de changer l'id dans la requête comme suit:
'''
curl -i -H "Content-Type: application/json" -X PUT -d '{"date_naissance":"21-07-1995"}' http://127.0.0.1:5000/user/1 --header "x-access-token:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZXhwIjoxNTM0MTkzMTYyfQ.WMN8YUHmnN1fWuQS4pBFJSX15Fta4yIn8AiRV9qtZSI""
'''
Vous recevez donc ce message:

IMAGE12!!!

Comme prévu, les modifications sont interdites car M.Martin ne peut modifier que ses informations personnelles.

- Vous pouvez tester encore les contraintes en ajoutant des utilisateurs et des biens et en envoyant des requêtes semblables à celles au dessus en modifiants quelque renseignements. Normalement, Vous disposer de tout ce que vous avez besoin pour faire tous les tests que vous souhaitez faire pour cette base de données.

## Auteurs
**Mohamed Bejaoui**

### Merci pour votre attention!
