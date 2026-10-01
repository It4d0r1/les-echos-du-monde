# Essai en jeu — à effectuer

Les vérifications faites jusqu'ici portent sur les fichiers. Elles ne confirment pas le fonctionnement réel dans Minecraft.

1. Fermer complètement Minecraft, relancer **Pixelmon Les Échos du Monde**, puis créer un nouveau monde de test.
2. Vérifier le message de préparation dans l'Overworld et la progression des **933 morceaux**. La durée dépend des performances du modpack; aucun délai réel n'a été mesuré.
3. Attendre la téléportation automatique dans `les_echos_du_monde:prologue`. Vérifier avec F3 la position d'arrivée initiale **7, -3, 1**, avant de se déplacer.
4. Vérifier la végétation, les chemins, les six réserves et les limites de Garrik. Le modèle doit utiliser l'origine **-235, -30, -250**.
5. Tester la reconnexion : l'arrivée ne doit pas être rejouée pour un joueur ayant déjà reçu le tag `edm_prologue_done`.

En cas d'arrêt de la préparation, conserver `logs/latest.log`. Avec les commandes autorisées, consulter :

```mcfunction
/data get storage les_echos_du_monde:state
```

`platform_placed:1b` indique que tous les morceaux ont réussi leur placement. `platform_error_tile` indique l'indice du morceau arrêté. Ne se téléporter manuellement vers la plateforme que lorsque son placement est terminé.

La sortie et le spawn Overworld restent provisoires; leur sécurité dans le terrain réel de l'Overworld n'a pas été testée.
