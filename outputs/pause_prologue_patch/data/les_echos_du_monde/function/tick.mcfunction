# Envoie chaque joueur une seule fois dans le prologue.
execute unless data storage les_echos_du_monde:state {prologue_automation_paused:1b} as @a[tag=!edm_prologue_done] at @s run function les_echos_du_monde:player/first_join
# Apres l'arrivee, construit le modele chunk par chunk autour du joueur.
execute unless data storage les_echos_du_monde:state {prologue_automation_paused:1b} in les_echos_du_monde:prologue as @a[tag=edm_prologue_done] unless data storage les_echos_du_monde:state platform_placed unless data storage les_echos_du_monde:state platform_building unless data storage les_echos_du_monde:state platform_error run function les_echos_du_monde:world/place_platform
# Si Minecraft refuse un morceau, avertit chaque joueur une seule fois.
execute unless data storage les_echos_du_monde:state {prologue_automation_paused:1b} as @a[tag=!edm_platform_error_reported] if data storage les_echos_du_monde:state platform_error run function les_echos_du_monde:player/report_platform_error
# Zone de sortie provisoire.
execute unless data storage les_echos_du_monde:state {prologue_automation_paused:1b} in les_echos_du_monde:prologue as @a[x=-1,y=-4,z=6,dx=2,dy=2,dz=2] run function les_echos_du_monde:player/exit
