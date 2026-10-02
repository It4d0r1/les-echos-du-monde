execute unless data storage les_echos_du_monde:state {platform_layout:"segments_v17"} run tellraw @s {"text":"Ce monde utilise une ancienne plateforme. La nouvelle génération reste bloquée pour protéger les constructions.","color":"red"}
execute unless data storage les_echos_du_monde:state {platform_layout:"segments_v17"} run return 0
data remove storage les_echos_du_monde:state prologue_automation_paused
function les_echos_du_monde:world/segments_v17/enable
