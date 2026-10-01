data modify storage les_echos_du_monde:state platform_placed set value 1b
data remove storage les_echos_du_monde:state platform_building
execute as @a[tag=edm_prologue_waiting] run title @s actionbar {"text":"Le prologue est prêt.","color":"green"}
