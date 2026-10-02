scoreboard players add #wait edm_seg_ctl 2
execute if loaded -64 0 -256 if loaded -64 0 -240 if loaded -64 0 -224 if loaded -48 0 -256 if loaded -48 0 -240 if loaded -48 0 -224 if loaded -32 0 -256 if loaded -32 0 -240 if loaded -32 0 -224 run function les_echos_du_monde:world/segments_v17/segment/s_m02_m08/place
execute if score #active edm_seg_ctl matches 72 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m02_m08/fail
