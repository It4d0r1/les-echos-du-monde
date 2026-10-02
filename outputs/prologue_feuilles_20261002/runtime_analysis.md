# Analyse du placement des feuilles signalées

Analyse en lecture seule. Aucun template, datapack installé ou monde n'a été modifié.

## Point signalé et segment

Le point **(-20, -1, 6)** appartient au segment `s_m01_p00`, placé à
**(-32, -26, 0)**. Ses coordonnées locales sont **(12, 25, 6)**.
Il n'est pas sur une couture de segment.

Dans le template installé, cette case contient `minecraft:oak_leaves` avec
`distance=1`, `persistent=false`, `waterlogged=false`.
Les cinq voisins latéraux/inférieur sont absents ; le voisin supérieur est une
autre feuille. La composante des feuilles connectées par les six faces contient
**neuf feuilles**, de **(-21, -1, 5)** à **(-19, 1, 7)**, toutes dans le même segment.
Elle ne touche aucun bloc de tronc.

La recherche a porté sur les neuf templates voisins couvrant X=-64..31 et
Z=-32..63. Le tronc le plus proche trouvé est à une distance Manhattan de 43.
Cette composante ne rejoint donc pas un tronc situé dans le segment voisin.

Les neuf templates voisins installés sont identiques par SHA-256 aux templates
préparés. Les fonctions de sélection, placement, attente, préparation d'arrivée
et déplacement examinées sont également identiques à la version préparée.

## Ce que fait le runtime

La commande est :

```text
place template les_echos_du_monde:platform_segments_v17/s_m01_p00 -32 -26 0
```

L'intégrité implicite est 1, la rotation et le miroir implicites sont désactivés.
Le runtime ne choisit pas une fraction des blocs du template. Il attend les neuf
chunks requis par la commande, puis enregistre la réussite du segment.

Le segment ciblé est préparé juste après le segment central pendant l'accueil.
L'arrivée normale attend neuf segments autour du spawn. Une attente d'un voisin
ne peut pas expliquer ce fragment une fois l'accueil terminé.

La génération ne réinitialise pas les segments terminés. Cette analyse ne
recommande pas de les replacer dans la sauvegarde du joueur.

## Feuilles et mises à jour vanilla

Le bytecode vanilla 1.21.1 de `LeavesBlock` montre que la décroissance aléatoire
requiert **persistent=false ET distance=7**. Une feuille sérialisée avec une
distance périmée de 1 ne disparaît pas nécessairement simplement en attendant.

`updateShape` programme une mise à jour de la distance, puis `updateDistance`
recalcule le minimum à partir des six voisins, avec une limite de 7.
`StructureTemplate.placeInWorld` effectue aussi des mises à jour des formes et
des voisins si les formes ne sont pas déjà déclarées connues. Le comportement
réel et les délais en jeu dépendent donc des mises à jour effectuées et du monde.
Cette analyse du code ne remplace pas une mesure de l'état de la case en jeu.

Ces éléments ont été lus dans le fichier vanilla local, sans modification d'un
fichier de mod, et archivés dans les fichiers `*_1.21.1_bytecode.txt` du dossier.

## Comment distinguer les causes

1. **Fragment déjà dans la source** : vérifier la case locale **(230,25,241)** du
   NBT complet. Si les mêmes neuf feuilles et l'absence de tronc sont présentes,
   le découpage a conservé ce fragment préexistant. L'analyse de la source doit
   confirmer ce point avant de conclure définitivement.
2. **Arbre temporairement incomplet** : la source contient un arbre relié à un
   tronc, mais le tronc ou la chaîne de feuilles traverse un bord de segment dont
   le score `edm_seg_done` n'est pas encore à 1. Ce cas ne correspond pas à la
   petite composante ciblée, entièrement intérieure à un segment.
3. **Erreur de découpage** : un bloc de tronc ou de feuille présent dans la source
   manque dans le template correspondant après conversion des coordonnées.
   La reconstruction intégrale des templates doit alors différer de la source
   préparée. Le générateur dispose déjà d'un contrôle de reconstruction exacte.
4. **Modification en jeu ou décroissance** : source et templates sont corrects,
   les segments concernés sont terminés, mais des blocs manquent dans le monde.
   Examiner alors les états de feuilles, les modifications du monde et les
   mises à jour. Rejouer tous les segments écraserait les constructions ultérieures.

Les grandes canopées traversant un bord de segment présentent théoriquement un
risque différent : des feuilles non persistantes peuvent recalculer leur
distance avant le placement du tronc voisin. Il faudrait observer cette situation
avant de l'attribuer au runtime. Ce risque ne démontre aucune erreur sur le
fragment précis signalé.

Les données exactes figurent dans `runtime_target_report.json` et peuvent être
reproduites avec `inspect_runtime_target.py`.
