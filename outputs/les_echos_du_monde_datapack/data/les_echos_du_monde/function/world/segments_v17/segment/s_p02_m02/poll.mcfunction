scoreboard players add #wait edm_seg_ctl 2
execute if loaded 64 0 -64 if loaded 64 0 -48 if loaded 64 0 -32 if loaded 80 0 -64 if loaded 80 0 -48 if loaded 80 0 -32 if loaded 96 0 -64 if loaded 96 0 -48 if loaded 96 0 -32 run function les_echos_du_monde:world/segments_v17/segment/s_p02_m02/place
execute if score #active edm_seg_ctl matches 139 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p02_m02/fail
