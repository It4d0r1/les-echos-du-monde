scoreboard players add #wait edm_seg_ctl 2
execute if loaded -192 0 32 if loaded -192 0 48 if loaded -192 0 64 if loaded -176 0 32 if loaded -176 0 48 if loaded -176 0 64 if loaded -160 0 32 if loaded -160 0 48 if loaded -160 0 64 run function les_echos_du_monde:world/segments_v17/segment/s_m06_p01/place
execute if score #active edm_seg_ctl matches 25 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m06_p01/fail
