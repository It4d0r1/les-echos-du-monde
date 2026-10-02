scoreboard players add #wait edm_seg_ctl 2
execute if loaded -64 0 32 if loaded -64 0 48 if loaded -64 0 64 if loaded -48 0 32 if loaded -48 0 48 if loaded -48 0 64 if loaded -32 0 32 if loaded -32 0 48 if loaded -32 0 64 run function les_echos_du_monde:world/segments_v17/segment/s_m02_p01/place
execute if score #active edm_seg_ctl matches 81 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m02_p01/fail
