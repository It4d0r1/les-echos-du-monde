# Lire les commandes WorldEdit sur Android

## Fichier à ouvrir

Dans le dépôt `les-echos-du-monde`, ouvrir :

`04_TECHNIQUE/BRUSHES_CHEMINS_PLACE_VILLAGE.md`

Ce guide contient les commandes pour les chemins, la place, la flore, les arbres et l'annulation des opérations WorldEdit. Les commandes sont à saisir dans Minecraft avec les permissions nécessaires.

## Récupérer les documents avec Gitling

Adresse du dépôt configuré sur le PC :

```text
https://github.com/It4d0r1/les-echos-du-monde.git
```

1. Dans Gitling, connecter un compte GitHub autorisé à accéder au dépôt.
2. Pour la première récupération, utiliser `+`, saisir cette URL et le nom local `les-echos-du-monde`, puis lancer `Clone`.
3. Attendre la fin du clonage. `remote: Enumerating objects` indique que le serveur prépare les éléments à transmettre ; ce message seul ne confirme pas que le téléchargement est terminé.
4. Pour récupérer les modifications publiées ensuite, utiliser `Pull` dans le dépôt existant. Enregistrer les éventuelles modifications locales avant cette opération.
5. Ouvrir le dossier `04_TECHNIQUE`, puis le fichier indiqué ci-dessus.

## Lire avec une application Android

[Markor](https://github.com/gsantner/markor) prend en charge Markdown et son aperçu, et permet de lire les fichiers locaux hors connexion.

1. Installer Markor depuis les liens de téléchargement proposés par son projet officiel.
2. Depuis Gitling, utiliser l'ouverture du fichier dans un éditeur externe et choisir Markor si Android le propose.
3. Dans Markor, utiliser le mode aperçu ou lecture pour afficher les titres, les tableaux et les blocs de commandes.
4. Si l'ouverture externe ne fonctionne pas, enregistrer ou exporter une copie du fichier dans un dossier accessible, par exemple `Documents`, puis ouvrir cette copie avec Markor.

Les intitulés des boutons peuvent varier selon les versions. L'ouverture Gitling → Markor n'a pas été testée sur le téléphone de Bastien. Markor lit la copie locale ; Gitling assure la récupération depuis GitHub.

## Lire dans le navigateur

1. Ouvrir [le dépôt GitHub](https://github.com/It4d0r1/les-echos-du-monde) et se connecter si nécessaire.
2. Ouvrir `04_TECHNIQUE/BRUSHES_CHEMINS_PLACE_VILLAGE.md`.
3. Choisir `Preview / Aperçu` pour afficher la mise en page Markdown.

## Emplacement des copies

| Copie | Emplacement et rôle |
| --- | --- |
| PC | `C:\Users\Bastien\Desktop\Les Echo du monde\04_TECHNIQUE` : documentation du projet. |
| GitHub | Même chemin relatif dans le dépôt, après commit et push réussis. |
| Android | Copie récupérée par Gitling avec Clone ou Pull. |
| Modpack actif | Les fonctions du datapack sont dans `global_packs/required_data/les_echos_du_monde`. Ces guides Android et WorldEdit sont des documents du projet ; ils n'ont pas de copie d'installation nécessaire dans ce dossier. |

Un lien absolu commençant par `C:\` désigne le PC. Sur Android, utiliser les chemins relatifs du dépôt ou les liens GitHub.

## Sources

- [Gitling : clonage et éditeur externe](https://github.com/maneeshacooray/Gitling#quick-start).
- [Markor : formats pris en charge et aperçu](https://github.com/gsantner/markor#features).
- [GitHub : afficher l'aperçu des fichiers Markdown](https://docs.github.com/en/repositories/working-with-files/using-files/viewing-and-understanding-files).

Voir aussi le guide général [Synchronisation PC et Android](../SYNCHRONISATION_PC_ANDROID.md).
