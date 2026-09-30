# Synchroniser le projet entre le PC et Android

Le dépôt GitHub privé prévu, `drague036-afk/les-echos-du-monde`, servira de point de partage entre les appareils.

## Sur le PC

Dans le dossier du projet :

1. Avant de commencer, récupérer les changements du téléphone avec `git pull`.
2. Modifier les fichiers.
3. Enregistrer les changements avec `git add -A`, puis `git commit -m "Description des changements"`.
4. Envoyer les changements sur GitHub avec `git push`.

## Sur Android

Dans une application Git compatible avec GitHub :

1. Cloner `https://github.com/drague036-afk/les-echos-du-monde.git` une seule fois.
2. Avant de modifier des fichiers, faire `pull` pour récupérer les changements du PC.
3. Après les modifications, créer un commit puis faire `push`.

La synchronisation est manuelle : `pull` récupère les changements et `push` envoie les tiens. Éviter de modifier le même fichier sur le PC et le téléphone avant d’avoir synchronisé, pour limiter les conflits.

## Contenu synchronisé

La sélection prévue comprend les documents du projet, les idées, les ressources, le datapack exporté et les sources MCreator. Le fichier `.gitignore` écarte les sauvegardes complètes, les caches de compilation et les réglages locaux de MCreator.

Le profil CurseForge et ses mondes Minecraft ne sont pas inclus : ce dossier de projet ne les contient pas.

