scoreboard players add #wait edm_seg_ctl 2
execute if loaded -160 0 -160 if loaded -160 0 -144 if loaded -160 0 -128 if loaded -144 0 -160 if loaded -144 0 -144 if loaded -144 0 -128 if loaded -128 0 -160 if loaded -128 0 -144 if loaded -128 0 -128 run function les_echos_du_monde:world/segments_v17/segment/s_m05_m05/place
execute if score #active edm_seg_ctl matches 31 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m05_m05/fail
