scoreboard players add #wait edm_seg_ctl 2
execute if loaded -192 0 -160 if loaded -192 0 -144 if loaded -192 0 -128 if loaded -176 0 -160 if loaded -176 0 -144 if loaded -176 0 -128 if loaded -160 0 -160 if loaded -160 0 -144 if loaded -160 0 -128 run function les_echos_du_monde:world/segments_v17/segment/s_m06_m05/place
execute if score #active edm_seg_ctl matches 19 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m06_m05/fail
