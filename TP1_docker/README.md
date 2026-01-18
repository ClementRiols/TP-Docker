# TP Docker – Exercices 3 et 4

---

## Exercice 3 – Manipulation de base des conteneurs

### 1. Vérification de la version de Docker
Commande utilisée :  
`docker --version`  

Résultat obtenu :  
Docker version 29.1.3, build f52814d

La version affichée confirme que Docker est correctement opérationnel.

### 2. Liste des images Docker locales
Commande utilisée :  
`docker images`  

Résultat :  
IMAGE ID DISK USAGE CONTENT SIZE EXTRA

À ce stade, aucune image spécifique n’est encore utilisée.

### 3. Téléchargement d’une image depuis Docker Hub
Commande utilisée :  
`docker pull hello-world`  

Résultat :  
Using default tag: latest
latest: Pulling from library/hello-world
17eec7bbc9d7: Pull complete
ea52d2000f90: Download complete
Digest: sha256:d4aaab6242e0cace87e2ec17a2ed3d779d18fbfd03042ea58f2995626396a274
Status: Downloaded newer image for hello-world:latest
docker.io/library/hello-world:latest

L’image officielle `hello-world` est téléchargée depuis Docker Hub.

### 4. Exécution d’un conteneur à partir de l’image
Commande utilisée :  
`docker run hello-world`  

Résultat :  
Hello from Docker!
This message shows that your installation appears to be working correctly.
...

Le conteneur s’exécute bien puis s’arrête immédiatement après l’affichage du message montrant ainsi que tout fonctionne

### 5. Liste des conteneurs en cours d’exécution
Commande utilisée :  
`docker ps`  

Résultat :  
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES

Aucun conteneur n’apparaît car le conteneur `hello-world` s’est arrêté automatiquement après son exécution.

### 6. Liste de tous les conteneurs (actifs et arrêtés)
Commande utilisée :  
`docker ps -a`  

Résultat :  
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
460d27b37902 hello-world "/hello" 7 minutes ago Exited (0) 7 minutes ago jovial_dubinsky

Cette commande permet de voir l’historique des conteneurs, y compris ceux qui sont arrêtés.  
On constate cette fois-ci que le conteneur `hello-world` est bien présent, il s’est bien terminé sans erreur.

### 7. Suppression du conteneur
Commande utilisée :  
`docker rm 460d27b37902`  

Résultat :  
460d27b37902

Le conteneur est bien supprimé cela évite l’accumulation de conteneurs dont on ne sert plus.

### 8. Suppression de l’image Docker
Commande utilisée :  
`docker rmi hello-world`  

Résultat :  
Untagged: hello-world:latest
Deleted: sha256:d4aaab6242e0cace87e2ec17a2ed3d779d18fbfd03042ea58f2995626396a274

L’image est supprimée après utilisation permettant ainsi de libérer de l’espace disque 
---

## Exercice 4 – Création d’un serveur web avec Docker


### 1. Téléchargement de l’image officielle Nginx
Commande utilisée :  
`docker pull nginx`  

Résultat :  
Using default tag: latest
latest: Pulling from library/nginx
d6799cf0ce70: Pull complete
...
Status: Downloaded newer image for nginx:latest
docker.io/library/nginx:latest

L’image officielle `nginx` est bien téléchargée depuis Docker Hub.

### 2. Lancement du conteneur Nginx en arrière-plan
Commande utilisée :  
`docker run -d -p 8080:80 --name mon_nginx nginx`  

Résultat :  
94d70220f01317ce4e8ff3594fd6e36d987858307e1530415cd2d5f615e9a160

Explications plus détaillées :
- `-d` : exécute le conteneur en arrière-plan  
- `-p 8080:80` : mappe le port 80 du conteneur vers le port 8080 de la machine hôte  
- `--name mon_nginx` : donne un nom explicite au conteneur  

Le serveur web devient accessible en allant sur `http://localhost:8080`.

### 3. Vérification de l’état du conteneur
Commande utilisée :  
`docker ps`  

Résultat :  
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
94d70220f013 nginx "/docker-entrypoint.…" 2 minutes ago Up 2 minutes 0.0.0.0:8080->80/tcp, [::]:8080->80/tcp mon_nginx

Le conteneur est bien en cours d’exécution et le port est correctement exposé.

### 4. Accès à l’application via un navigateur
Résultat affiché dans le navigateur :  
Welcome to nginx!
If you see this page, the nginx web server is successfully installed and working.

Cette page confirme que le conteneur fonctionne, le serveur Nginx est opérationnel et le mapping de ports est correct

### 5. Arrêt du conteneur
Commande utilisée :  
`docker stop mon_nginx`  

Résultat :  
mon_nginx

Le conteneur est arrêté proprement, sans suppression immédiate.

### 6. Suppression du conteneur
Commande utilisée :  
`docker rm mon_nginx`  

Résultat :  
mon_nginx

Le conteneur est supprimé afin de libérer les ressources et aussi pour pouvoir maintenir un environnement Docker propre.

## Exercice 5 – Déploiement d'une application Python Flask

### 1. Création de l’application Flask

Fichier `app.py` :

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

Cette application python expose une seule route qui renvoie le message "Hello, World!". De plus, l’option `host='0.0.0.0'` permet au conteneur d’être accessible depuis l’extérieur.

### 2. Écriture du Dockerfile

Dockerfile utilisé :

FROM python:3.13
WORKDIR /app
RUN pip install flask
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]

Explications :
- `FROM python:3.13` : image officielle Python 3.13 comme base.
- `WORKDIR /app` : définit le répertoire de travail dans le conteneur.
- `RUN pip install flask` : installe Flask dans le conteneur.
- `COPY app.py .` : copie le fichier Python dans le conteneur.
- `EXPOSE 5000` : expose le port 5000 pour accéder à l’application.
- `CMD ["python", "app.py"]` : commande de démarrage du conteneur.

### 3. Construction de l’image Docker

Commande utilisée :

docker build -t tp_docker_exo5 .

Résultat :

[+] Building 32.3s (9/9) FINISHED
...
Successfully built tp_docker_exo5:latest

L’image est créée et prête à être utilisée pour lancer un conteneur.

### 4. Test de l’application

Commande utilisée :

docker images

Résultat :

IMAGE ID        DISK USAGE    CONTENT SIZE
nginx:latest    228MB         62.6MB
tp_docker_exo5  1.62GB        418MB

Le conteneur fonctionne correctement et l’application Flask est accessible via le port 5000 (`http://localhost:5000`), elle affiche bien "Hello World !".

---

## Exercice 6 – Utilisation de Docker Compose

### 1. Modification de l’application Flask

Fichier `app.py` :

from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")
db = client.test_db

@app.route("/")
def hello_world():
    return "Hello World! Connexion à Mongo DB"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

On ajoute une connexion à une base MongoDB pour simuler une application multi-services.

### 2. Écriture du fichier Docker Compose

Fichier `docker-compose.yml` :

services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - mongo

  mongo:
    image: mongo
    ports:
      - "27017:27017"

Explications :
- `web` : conteneur de l’application Flask, construit à partir du Dockerfile local
- `mongo` : conteneur MongoDB
- `depends_on` : le serveur web dépends de MongoDB
- `ports` : mappe les ports du conteneur vers la machine hôte

### 3. Lancement avec Docker Compose

Commande utilisée :

docker compose up --build

Résultat :

[+] Building 38.8s (11/11) FINISHED
...
✔ tp1_docker-web Built 0.0s
✔ Network tp1_docker_default Created 0.1s
✔ Container tp1_docker-mongo-1 Created 0.2s
✔ Container tp1_docker-web-1 Created 0.2s
Attaching to mongo-1, web-1
...

> Le conteneur Flask (`web-1`) et MongoDB (`mongo-1`) sont démarrés correctement et reliés.

### 4. Vérification du fonctionnement

Commande pour lancer les conteneurs en arrière-plan :

docker compose up -d

Le site Flask est accessible via `http://localhost:5000` et renvoie :  
`Hello World! Connexion à Mongo DB`  
La connexion à MongoDB est effective et la communication entre les deux conteneurs fonctionne correctement.
