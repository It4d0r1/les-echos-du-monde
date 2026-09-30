# Envoie chaque joueur une seule fois dans le prologue. Le tag persiste dans ses données de joueur.
execute as @a[tag=!edm_prologue_done] at @s run function les_echos_du_monde:player/first_join

# Si Minecraft a refusé le modèle, avertit chaque joueur une seule fois.
execute as @a[tag=!edm_platform_error_reported] if data storage les_echos_du_monde:state platform_error run function les_echos_du_monde:player/report_platform_error

# Zone de sortie provisoire : ajuster cette boîte à la sortie réelle de la carte.
execute in les_echos_du_monde:prologue as @a[x=-1,y=-4,z=6,dx=2,dy=2,dz=2] run function les_echos_du_monde:player/exit
