scoreboard players add #wait edm_seg_ctl 2
execute if loaded 160 0 -128 if loaded 160 0 -112 if loaded 160 0 -96 if loaded 176 0 -128 if loaded 176 0 -112 if loaded 176 0 -96 if loaded 192 0 -128 if loaded 192 0 -112 if loaded 192 0 -96 run function les_echos_du_monde:world/segments_v17/segment/s_p05_m04/place
execute if score #active edm_seg_ctl matches 181 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p05_m04/fail
