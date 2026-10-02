scoreboard players add #wait edm_seg_ctl 2
execute if loaded 32 0 -96 if loaded 32 0 -80 if loaded 32 0 -64 if loaded 48 0 -96 if loaded 48 0 -80 if loaded 48 0 -64 if loaded 64 0 -96 if loaded 64 0 -80 if loaded 64 0 -64 run function les_echos_du_monde:world/segments_v17/segment/s_p01_m03/place
execute if score #active edm_seg_ctl matches 124 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p01_m03/fail
