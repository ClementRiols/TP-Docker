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
