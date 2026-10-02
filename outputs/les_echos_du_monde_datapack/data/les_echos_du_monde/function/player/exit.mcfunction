# Provisional destination. Change X/Y/Z here once the Garrik village location is fixed.
scoreboard players set #overworld_tp edm_internal 0
execute in minecraft:overworld store success score #overworld_tp edm_internal run tp @s 0.5 80 0.5
execute if score #overworld_tp edm_internal matches 1 run tag @s add edm_prologue_done
execute if score #overworld_tp edm_internal matches 1 run tag @s remove edm_prologue_waiting
