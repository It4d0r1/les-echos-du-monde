scoreboard players add s_p01_p03 edm_seg_retry 1
data modify storage les_echos_du_monde:segments_v17 last_error.segment set value "s_p01_p03"
execute store result storage les_echos_du_monde:segments_v17 last_error.failures int 1 run scoreboard players get s_p01_p03 edm_seg_retry
execute if score s_p01_p03 edm_seg_retry matches 3 run tellraw @a {"text":"Plateforme : le segment s_p01_p03 a échoué 3 fois. Génération de ce segment suspendue ; consultez la documentation.","color":"red"}
function les_echos_du_monde:world/segments_v17/segment/s_p01_p03/cleanup
