# Coordonnees exactes, apres placement integral et verification hors jeu du sol.
execute unless data storage les_echos_du_monde:state platform_placed run return 0
scoreboard players set #prologue_tp edm_internal 0
execute in les_echos_du_monde:prologue store success score #prologue_tp edm_internal run tp @s 7 -3 1
execute if score #prologue_tp edm_internal matches 1 run tag @s add edm_prologue_done
execute if score #prologue_tp edm_internal matches 1 run tag @s remove edm_prologue_waiting
