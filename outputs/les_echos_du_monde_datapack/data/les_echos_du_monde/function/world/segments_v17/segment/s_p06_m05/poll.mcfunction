scoreboard players add #wait edm_seg_ctl 2
execute if loaded 192 0 -160 if loaded 192 0 -144 if loaded 192 0 -128 if loaded 208 0 -160 if loaded 208 0 -144 if loaded 208 0 -128 if loaded 224 0 -160 if loaded 224 0 -144 if loaded 224 0 -128 run function les_echos_du_monde:world/segments_v17/segment/s_p06_m05/place
execute if score #active edm_seg_ctl matches 193 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p06_m05/fail
