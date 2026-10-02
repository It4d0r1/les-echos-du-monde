scoreboard players add #wait edm_seg_ctl 2
execute if loaded -192 0 160 if loaded -192 0 176 if loaded -192 0 192 if loaded -176 0 160 if loaded -176 0 176 if loaded -176 0 192 if loaded -160 0 160 if loaded -160 0 176 if loaded -160 0 192 run function les_echos_du_monde:world/segments_v17/segment/s_m06_p05/place
execute if score #active edm_seg_ctl matches 29 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m06_p05/fail
