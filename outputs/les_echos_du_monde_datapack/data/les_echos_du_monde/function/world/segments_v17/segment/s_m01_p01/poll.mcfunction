scoreboard players add #wait edm_seg_ctl 2
execute if loaded -32 0 32 if loaded -32 0 48 if loaded -32 0 64 if loaded -16 0 32 if loaded -16 0 48 if loaded -16 0 64 if loaded 0 0 32 if loaded 0 0 48 if loaded 0 0 64 run function les_echos_du_monde:world/segments_v17/segment/s_m01_p01/place
execute if score #active edm_seg_ctl matches 97 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m01_p01/fail
