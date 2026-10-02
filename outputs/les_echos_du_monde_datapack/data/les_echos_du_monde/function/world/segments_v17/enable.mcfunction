execute unless data storage les_echos_du_monde:state {platform_layout:"segments_v17"} run tellraw @s {"text":"Ce monde utilise une autre plateforme. Créez un nouveau monde pour la version 17.","color":"red"}
execute unless data storage les_echos_du_monde:state {platform_layout:"segments_v17"} run return 0
execute if data storage les_echos_du_monde:state {prologue_automation_paused:1b} run tellraw @s {"text":"L'automatisation globale du prologue est en pause. Réactivez-la d'abord.","color":"red"}
execute if data storage les_echos_du_monde:state {prologue_automation_paused:1b} run return 0
scoreboard players set #enabled edm_seg_ctl 1
data modify storage les_echos_du_monde:segments_v17 enabled set value 1b
tellraw @s {"text":"Génération de plateforme activée.","color":"green"}
