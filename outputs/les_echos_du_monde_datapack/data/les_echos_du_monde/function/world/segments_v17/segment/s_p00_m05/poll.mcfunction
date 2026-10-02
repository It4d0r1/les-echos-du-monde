scoreboard players add #wait edm_seg_ctl 2
execute if loaded 0 0 -160 if loaded 0 0 -144 if loaded 0 0 -128 if loaded 16 0 -160 if loaded 16 0 -144 if loaded 16 0 -128 if loaded 32 0 -160 if loaded 32 0 -144 if loaded 32 0 -128 run function les_echos_du_monde:world/segments_v17/segment/s_p00_m05/place
execute if score #active edm_seg_ctl matches 107 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p00_m05/fail
