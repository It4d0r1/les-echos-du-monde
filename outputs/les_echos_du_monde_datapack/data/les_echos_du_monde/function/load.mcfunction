# Initialise les règles et points par défaut une fois par sauvegarde.
execute unless data storage les_echos_du_monde:state initialized run function les_echos_du_monde:world/initialize
# Invalide le marqueur historique, qui était écrit même si le placement échouait.
execute unless data storage les_echos_du_monde:state platform_verified run function les_echos_du_monde:world/migrate_platform_marker
# Prépare un score technique pour lire le résultat réel de /place template.
execute unless data storage les_echos_du_monde:state platform_score_ready run function les_echos_du_monde:world/setup_platform_score
# Placement indépendant du marqueur d'initialisation : permet aussi de réparer
# une sauvegarde créée avant l'ajout de la structure Axiom.
execute unless data storage les_echos_du_monde:state platform_placed run function les_echos_du_monde:world/place_platform
