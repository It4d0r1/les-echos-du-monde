# Synchroniser le projet entre le PC et Android

## Dépôt prêt

Le dépôt GitHub privé [drague036-afk/les-echos-du-monde](https://github.com/drague036-afk/les-echos-du-monde) est créé. La copie du PC a été envoyée sur la branche `main`. Le téléphone Android doit maintenant cloner le dépôt une première fois.

## Sur Android

1. Installer [Gitling depuis F-Droid](https://f-droid.org/packages/com.maneeshacooray.gitling/). Gitling permet de cloner, récupérer et envoyer des changements sur GitHub.
2. Dans Gitling, connecter le compte GitHub avec la connexion sécurisée proposée par l’application.
3. Appuyer sur `+`, saisir l’adresse `https://github.com/drague036-afk/les-echos-du-monde.git`, choisir un nom local, puis appuyer sur `Clone`.
4. Installer aussi une application d’édition de texte compatible avec Android pour modifier les fichiers Markdown. Gitling ouvre les fichiers dans un éditeur externe.
5. Avant de modifier des fichiers, faire `Pull` dans Gitling.
6. Après les modifications, ouvrir la liste des changements, sélectionner les fichiers, créer un commit avec un court message, puis faire `Push`.

## Sur le PC

Dans le dossier du projet :

1. Avant de commencer, récupérer les changements du téléphone avec `git pull`.
2. Modifier les fichiers.
3. Enregistrer les changements avec `git add -A`, puis `git commit -m "Description des changements"`.
4. Envoyer les changements sur GitHub avec `git push`.

La synchronisation est manuelle : `pull` récupère les changements et `push` envoie les tiens. Faire un `pull` avant de modifier les fichiers et un `push` après le commit. Éviter de modifier le même fichier sur le PC et le téléphone avant la synchronisation pour limiter les conflits.

## Contenu synchronisé

Le dépôt contient les documents du projet, les idées, les ressources, le datapack exporté et les sources MCreator. Le fichier `.gitignore` écarte les sauvegardes complètes, les caches de compilation et les réglages locaux de MCreator.

Le profil CurseForge et les mondes Minecraft ne sont pas inclus : ils se trouvent dans un autre dossier.
