# TP Docker Optimisation

---

### Fichiers de configuration

`.gitignore` :
node_modules/
*.log
.env
.DS_Store
Thumbs.db


`.dockerignore` :
node_modules
.git
.env

---

## Étape 0 – Performance de base

Dockerfile initial :
FROM node:latest
WORKDIR /app
COPY node_modules ./node_modules
COPY . /app
RUN npm install
RUN apt-get update && apt-get install -y build-essential ca-certificates locales && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen
EXPOSE 3000 4000 5000
ENV NODE_ENV=development
RUN npm run build
USER root
CMD ["node", "server.js"]


Commandes :
docker build -t tp_optimisation:baseline .
docker images tp_optimisation:baseline


Résultat :
[+] Building 41.4s (12/12) FINISHED
tp_optimisation:baseline 2b9d1273e926 1.72GB 433MB


Problèmes identifiés :
- Image très lourde (1.72GB)
- `node_modules` copié manuellement alors qu’il aurait dû être ignoré
- Plusieurs `RUN` distincts entraînent la création de plusieurs couches inutiles
- ...

---

## Étape 1 – Application de .dockerignore

Dockerfile :
FROM node:latest
WORKDIR /app
COPY . /app
RUN npm install
RUN apt-get update && apt-get install -y build-essential ca-certificates locales && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen
EXPOSE 3000 4000 5000
ENV NODE_ENV=development
RUN npm run build
USER root
CMD ["node", "server.js"]

Suppression de `COPY node_modules ./node_modules` inutile grâce au `.dockerignore`

Commandes :
docker build -t tp_optimisation:1-dockerignore .
docker images tp_optimisation:1-dockerignore


Résultat :
[+] Building 13.1s (11/11) FINISHED
tp_optimisation:1-dockerignore 61e4555600e8 1.72GB 435MB

Gain de temps important mais l'’image de base reste très lourde

---

## Étape 2 – Utilisation d’une image plus légère

Dockerfile :
FROM node:25-alpine
WORKDIR /app
COPY . /app
RUN npm install
RUN apk add --no-cache build-base ca-certificates tzdata
EXPOSE 3000 4000 5000
ENV NODE_ENV=development
RUN npm run build
USER root
CMD ["node", "server.js"]

`node:25-alpine` est une image minimale, réduisant drastiquement la taille finale de notre image mais 

Commandes :
docker build -t tp_optimisation:2-image-modif .
docker images tp_optimisation:2-image-modif


Résultat :
[+] Building 24.2s (11/11) FINISHED
tp_optimisation:2-image-modif 60e076455d6f 643MB 162MB

Le temps de build à un peu réaugmenté à cause de changement de certains run pour pouvoir utiliser la nouvelle image mais la taille de l'image a été drastiquement réduite.

---

## Étape 3 – Fusion des RUN

Dockerfile :
FROM node:25-alpine
WORKDIR /app
COPY . /app
RUN apk add --no-cache build-base ca-certificates tzdata
&& npm install
&& npm run build
EXPOSE 3000 4000 5000
ENV NODE_ENV=development
USER root
CMD ["node", "server.js"]

Fusion des `RUN` en une seule couche pour réduire le nombre de couches Docker

Commandes :
docker build -t tp_optimisation:3-fusion-run .
docker images tp_optimisation:3-fusion-run


Résultat :
[+] Building 23.5s (9/9) FINISHED
tp_optimisation:3-fusion-run a06445686bf3 643MB 162MB

La taille est logiquement inchangé. Par contre, nous n'avons pas constater d'amélioration du temps de build

---

## Étape 4 – Optimisation des COPY

Dockerfile :
FROM node:25-alpine
WORKDIR /app
COPY package*.json ./
RUN apk add --no-cache build-base ca-certificates tzdata
&& npm install
&& npm run build
COPY . .
EXPOSE 3000 4000 5000
ENV NODE_ENV=development
USER root
CMD ["node", "server.js"]

Copie séparée de `package*.json` avant le reste du code pour une meilleure optimisation

Commandes :
docker build -t tp_optimisation:4-copy .
docker images tp_optimisation:4-copy


Résultat :
[+] Building 23.9s (10/10) FINISHED
tp_optimisation:4-copy cc16f5967f36 643MB 162MB

Réduction des temps de rebuild si jamais les dépendances ne changent pas

---

## Étape 5 – Multi-stage build et nettoyage final

Dockerfile :
FROM node:25-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN apk add --no-cache build-base ca-certificates tzdata
&& npm install
&& npm run build
COPY . .

FROM node:25-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
EXPOSE 3000
ENV NODE_ENV=production
USER root
CMD ["node", "dist/server.js"]

 `EXPOSE 3000` unique et `NODE_ENV=production` pour une configuration propre et minimale
Multi-stage build : la construction et les dépendances lourdes restent dans la phase `builder` et ne sont pas copiées dans l’image finale
En effet, seul le code compilé (`dist`) et les fichiers nécessaires (`package*.json`) sont inclus dans l’image finale

Commandes :
docker build -t tp_optimisation:5-MultiStage-netoyage .
docker images tp_optimisation:5-MultiStage-netoyage

Résultat :
[+] Building 4.3s (13/13) FINISHED
tp_optimisation:5-MultiStage-netoyage 8c87447e21fe 248MB 59.8MB

Résultat final :
La taille a été considérablement passant réduite de 248MB contre 1.72GB au début. Il en va de même pour le temps de buid qui n'est plus que 4.3s alors qu'initialement il duré 41.4s