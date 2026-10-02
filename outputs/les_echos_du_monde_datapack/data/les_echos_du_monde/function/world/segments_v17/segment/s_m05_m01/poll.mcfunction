scoreboard players add #wait edm_seg_ctl 2
execute if loaded -160 0 -32 if loaded -160 0 -16 if loaded -160 0 0 if loaded -144 0 -32 if loaded -144 0 -16 if loaded -144 0 0 if loaded -128 0 -32 if loaded -128 0 -16 if loaded -128 0 0 run function les_echos_du_monde:world/segments_v17/segment/s_m05_m01/place
execute if score #active edm_seg_ctl matches 35 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m05_m01/fail
