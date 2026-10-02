scoreboard players add #wait edm_seg_ctl 2
execute if loaded -160 0 64 if loaded -160 0 80 if loaded -160 0 96 if loaded -144 0 64 if loaded -144 0 80 if loaded -144 0 96 if loaded -128 0 64 if loaded -128 0 80 if loaded -128 0 96 run function les_echos_du_monde:world/segments_v17/segment/s_m05_p02/place
execute if score #active edm_seg_ctl matches 38 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m05_p02/fail
