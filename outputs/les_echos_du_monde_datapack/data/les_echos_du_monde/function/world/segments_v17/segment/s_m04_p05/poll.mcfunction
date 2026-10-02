scoreboard players add #wait edm_seg_ctl 2
execute if loaded -128 0 160 if loaded -128 0 176 if loaded -128 0 192 if loaded -112 0 160 if loaded -112 0 176 if loaded -112 0 192 if loaded -96 0 160 if loaded -96 0 176 if loaded -96 0 192 run function les_echos_du_monde:world/segments_v17/segment/s_m04_p05/place
execute if score #active edm_seg_ctl matches 55 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m04_p05/fail
