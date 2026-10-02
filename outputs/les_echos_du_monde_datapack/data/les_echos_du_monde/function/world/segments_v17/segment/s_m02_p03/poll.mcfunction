scoreboard players add #wait edm_seg_ctl 2
execute if loaded -64 0 96 if loaded -64 0 112 if loaded -64 0 128 if loaded -48 0 96 if loaded -48 0 112 if loaded -48 0 128 if loaded -32 0 96 if loaded -32 0 112 if loaded -32 0 128 run function les_echos_du_monde:world/segments_v17/segment/s_m02_p03/place
execute if score #active edm_seg_ctl matches 83 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m02_p03/fail
