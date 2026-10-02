scoreboard players add #wait edm_seg_ctl 2
execute if loaded 0 0 96 if loaded 0 0 112 if loaded 0 0 128 if loaded 16 0 96 if loaded 16 0 112 if loaded 16 0 128 if loaded 32 0 96 if loaded 32 0 112 if loaded 32 0 128 run function les_echos_du_monde:world/segments_v17/segment/s_p00_p03/place
execute if score #active edm_seg_ctl matches 115 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p00_p03/fail
