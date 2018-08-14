# Création d'une API REST pour une gestion immobilière

## Présentation du projet

#### Problématique:
Ce projet a pour but de créer un ensemble de microservices qui doivent permetre à un utilisateur d'intéragir avec une plateforme en assurant les fonctionnalités suivantes:

- Un utilisateur peut renseigner un bien immobilier avec les caractéristiques suivantes: (nom, description, type de bien, ville, pièces, caractéristiques des pièces, propriétaire). Cet utilisateur devient donc propriétaire de ce bien. Il peut aussi modifier les caractéristiques de son bien **mais** pas celles des autres biens dont il n'est pas propriétaire.

- Un utilisateur peut consulter les biens disponibles sur la plateforme **uniquement** pour une **ville particulière**.

- Un utilisateur peut renseigner / modifier ses informations personnelles sur la plateforme (nom, prénom, date de naissance). **En revanche**, il ne peut ni accéeder à ni modifier les informations des autres utilisateurs.

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
- **Git Bash** pour envoyer les requêtes vers le serveur
- **sqlite3**
- Et bien sûr l'**invite des commande**.

## Étapes de fonctionnement:

Le code python qui contient toutes les fonctions nécessaires au fonctionnement du programme s'appelle **app.py**.

-  Une fois que vous avez téléchargé tous les fichiers présents dans le repository(sauf le fichier images qui sert que pour le Readme), mettez les dans le même chemin. Ensuite, ouvrez l'invite des commande et assurez vous que vous travaillez dans le chemin qui contient vos fichiers téléchargés.

- Tapez les commandes suivantes:
```
  python
  from app import db
  db.create_all()
  exit()
```

Ceci permet de créer les deux tables présentes dans le code app.py; la table **Utilisateur** et la table **Bien_Immobilier**.

![](https://github.com/mohamedbejaoui/gestion_immobiliere_api/blob/master/images/image1.PNG)

Pour tester que vous avez bien créer les deux tables, tapez les commandes suivantes:
```
sqlite3 test.db
.tables
.exit
```
En fait, les deux tables crées sont stockés dans test.db qui se trouve maintenant dans votre
chemin de travail. On voit que les deux tables sont bien crées.

![](https://github.com/mohamedbejaoui/gestion_immobiliere_api/blob/master/images/image2.PNG)

- Maintenant, on doit **lancer notre serveur**. Pour cela, tapez la commande suivante toujours dans l'invite des commandes:
```
python app.py
```

![](https://github.com/mohamedbejaoui/gestion_immobiliere_api/blob/master/images/image3.PNG)

- Le serveur étant lancé, nous pouvons maintenant commencer à envoyer les requêtes. Pour cela, ouvrez **Git Bash**.

- Commençons par créer un utilisateur avec les caractéristiques suivantes par exemple:
  - *nom:* Durand
  - *prénom:* Benoit
  - *date de naissance:* 22-05-1994

  Pour assurer toutes les contraintes mentionnées dans la problématique, j'ai ajouté deux autres colonnes à la table Utilisateur:
  - ***pseudo:*** benoitdurand
  - ***password:*** 12345

  Ces deux colonnes vont permettre à un utilisateur de se connecter au serveur. On va voir ça plus tard.

Pour envoyer la requête, le code a pour sytaxe:
```
curl -i -H "Content-Type: application/json" -X POST -d '{informations personnelles}' http://127.0.0.1:5000/user
```
Dans notre cas, tapez le code qui suit. (d'ailleurs, toutes les requêtes qu'on va envoyer au serveur vont être tapées dans Git Bash. **Tous les codes à suivre seront donc tapés dans Git Bash**)
```
  curl -i -H "Content-Type: application/json" -X POST -d '{"nom":"Durand","prenom":"Benoit","date_naissance":"22-05-1994","pseudo":"benoitdurand","password":"12345"}' http://127.0.0.1:5000/user
```
Vous devez avoir le message suivant:

![](https://github.com/mohamedbejaoui/gestion_immobiliere_api/blob/master/images/image4.PNG)

L'utilisateur est donc crée. Vous devez retenir son id pour une utilisation ultérieure.

- Créons un autre utilisateur. Ca va être utile pour tester nos fonctionnalités.

  Par exemple, on va choisir comme informations personnelles:
  - *nom:* Martin
  - *prénom:* Thomas
  - *date de naissance:* 14-06-1991
  - ***pseudo:*** thomasmartin
  - ***password:*** azerty   

Tapez donc le code suivant:
```
  curl -i -H "Content-Type: application/json" -X POST -d '{"nom":"Martin","prenom":"Thomas","date_naissance":"14-06-1991","pseudo":"thomasmartin","password":"azerty"}' http://127.0.0.1:5000/user
```
Ce message s'affichera:

![](https://github.com/mohamedbejaoui/gestion_immobiliere_api/blob/master/images/image5.PNG)


- Avant de passer à la création de biens, un utilisateur doit d'abord se connecter au serveur avec son pseudo et son mot de passe. Pour cela, si M.Durand essaye de se connecter, il doit taper ce code:
```
curl -u benoitdurand:12345 -i http://127.0.0.1:5000/login
```
D'une manière générale, la syntaxe du code est:
```
curl -u pseudo:password -i http://127.0.0.1:5000/login
```

Vous recevez donc un **token** comme suit:

![](https://github.com/mohamedbejaoui/gestion_immobiliere_api/blob/master/images/image6.PNG)

Ce token va gérer l'accés à certaines fonctions du programme qui nécessitent une autorisation.

Il va permettre à M.Durand de rester connecté pendant **30 minutes**. Au delà de cette période, il va **expirer**.

Vous devez donc le retenir car vous allez l'utiliser dans les requêtes qui vont suivre.


- Maintenant qu'on est connecté en tant que M.Durand, essayons de créer le premier bien que M.Durand va donc devenir propriétaire.

On va choisir par exemple les caractéristiques suivantes:
  - *nom:* Appartement 36mcarre Paris 15eme
  - *description:* A louer charmant appartement meuble de 36mcarre a proximite immediate de la gare Montparnasse
  - *type_bien:* appartement
  - *ville:* Paris
  - *pieces:* 2
  - *Carac_piece:* un salon et une chambre

Tapez donc le code suivant:
```
curl -i -H "Content-Type: application/json" -X POST -d '{"nom":"Appartement 36mcarre Paris 15eme","description":"A louer charmant appartement meuble de 36mcarre a proximite immediate de la gare Montparnasse","type_bien":"appartement","ville":"Paris","pieces":2,"carac_pieces":"un salon et une chambre"}' http://127.0.0.1:5000/bien_immobilier --header "x-access-token:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTM0MTkxNjk5fQ.EOxCREIhYMlduhKJ40sW6oEtXgae83u4PYbobR4obwQ""
```
Vous voyez bien que la syntaxe générale qui permet de renseigner un bien est:
```
curl -i -H "Content-Type: application/json" -X POST -d '{caractéristiques du bien}' http://127.0.0.1:5000/bien_immobilier --header "x-access-token:votre token"
```
Vous devez avoir le message suivant:

![](https://github.com/mohamedbejaoui/gestion_immobiliere_api/blob/master/images/image7.PNG)

Le bien est donc crée. Son id est 1.


- Essayons de consulter ce bien. N'importe quel utilisateur peut consulter les biens; on n'a donc pas besoin d'insérer le token dans la requête.

En revanche, on doit indiquer le nom de la ville. Dans notre cas, on n'a encore qu'un seul bien se trouvant à Paris.

Pour consulter les biens d'une ville, la requête est:
```
curl -i http://127.0.0.1:5000/bien_immobilier/"ville"
```

Dans notre cas, tapez donc le code suivant:
```
curl -i http://127.0.0.1:5000/bien_immobilier/"Paris"
```

Vous devez voir le message suivant:

![](https://github.com/mohamedbejaoui/gestion_immobiliere_api/blob/master/images/image8.PNG)


- Essayons maintenant de changer par exemple *type_bien* de **appartement** à **maison**. On est connecté en tant que M.Durand qui est propriétaire du bien 1. On sera donc capable de le faire.

Pour modifier les caractéristiques d'un bien, voici la requête à envoyer:
```
curl -i -H "Content-Type: application/json" -X PUT -d '{modifications à apporter}' http://127.0.0.1:5000/bien_immobilier/id_bien --header "x-access-token:votre token"
```

Dans notre cas, ça sera donc:

```
curl -i -H "Content-Type: application/json" -X PUT -d '{"type_bien":"maison"}' http://127.0.0.1:5000/bien_immobilier/1 --header "x-access-token:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTM0MTkxNjk5fQ.EOxCREIhYMlduhKJ40sW6oEtXgae83u4PYbobR4obwQ""
```
Et si on veut changer aussi le nombre de pièces, on remplacera ``` -d '{"type_bien":"maison"}' ``` par ``` -d '{"type_bien":"maison", "pieces"=3}' ```

Voud devez voir le message suivant:

![](https://github.com/mohamedbejaoui/gestion_immobiliere_api/blob/master/images/image9.PNG)

On a donc modifié les caractéristiques du bien. Vous pouvez le vérifier en consultant à nouveau la liste des biens à Paris.


- Maintenant, on va se connecter en tant que M.Martin. On va essayer de modifier le bien de M.Durand pour vérifier que ça ne va pas fonctionner.

Pour se connecter en tant que M.Martin, tapez:
```
curl -u thomasmartin:azerty -i http://127.0.0.1:5000/login
```
Retenez le token et utilisez le dans la requête suivante:(On va essayer de changer *pieces* de 2 à 3)
```
curl -i -H "Content-Type: application/json" -X PUT -d '{"pieces":3}' http://127.0.0.1:5000/bien_immobilier/1 --header "x-access-token:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZXhwIjoxNTM0MTkzMTYyfQ.WMN8YUHmnN1fWuQS4pBFJSX15Fta4yIn8AiRV9qtZSI""
```
Voici le message renvoyé:

![](https://github.com/mohamedbejaoui/gestion_immobiliere_api/blob/master/images/image10.PNG)

On voit bien que la modification n'est pas autorisée car M.Martin n'est pas propriétaire du bien 1.


- Il nous reste donc de voir comment modifier les informations personnelles d'un utilisateur.

Pour faire cette requête, le code est:
```
curl -i -H "Content-Type: application/json" -X PUT -d '{modifications à apporter}' http://127.0.0.1:5000/user/user_id --header "x-access-token:votre token"
```

M.Martin va essayer de changer sa date de naissance. Pour cela tapez:
```
curl -i -H "Content-Type: application/json" -X PUT -d '{"date_naissance":"21-07-1995"}' http://127.0.0.1:5000/user/2 --header "x-access-token:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZXhwIjoxNTM0MTkzMTYyfQ.WMN8YUHmnN1fWuQS4pBFJSX15Fta4yIn8AiRV9qtZSI""
```
Message renvoyé:

![](https://github.com/mohamedbejaoui/gestion_immobiliere_api/blob/master/images/image11.PNG)

Les modifications sont donc apportées car l'id dans le requête correspond à l'id de M.Martin qui est 2 (il était affiché lors de la création de l'utilisateur).

Maintenant, M.Martin va essayer de changer les informations de M.Durand. IL suffit de changer l'id à la fin du lien de la requête comme suit:
```
curl -i -H "Content-Type: application/json" -X PUT -d '{"date_naissance":"21-07-1995"}' http://127.0.0.1:5000/user/1 --header "x-access-token:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZXhwIjoxNTM0MTkzMTYyfQ.WMN8YUHmnN1fWuQS4pBFJSX15Fta4yIn8AiRV9qtZSI""
```
Vous recevez donc ce message:

![](https://github.com/mohamedbejaoui/gestion_immobiliere_api/blob/master/images/image12.PNG)

Comme prévu, les modifications sont interdites car M.Martin ne peut modifier que ses informations personnelles.



- Vous pouvez tester encore les contraintes en ajoutant des utilisateurs et des biens et en envoyant des requêtes semblables à celles au dessus. Normalement, Vous disposer de tout ce que vous avez besoin pour faire tous les tests que vous souhaitez faire pour cette base de données.

### Merci pour votre attention!

## Auteurs
**Mohamed Bejaoui**
