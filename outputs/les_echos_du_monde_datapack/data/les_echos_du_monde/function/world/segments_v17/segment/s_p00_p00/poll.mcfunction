scoreboard players add #wait edm_seg_ctl 2
execute if loaded 0 0 0 if loaded 0 0 16 if loaded 0 0 32 if loaded 16 0 0 if loaded 16 0 16 if loaded 16 0 32 if loaded 32 0 0 if loaded 32 0 16 if loaded 32 0 32 run function les_echos_du_monde:world/segments_v17/segment/s_p00_p00/place
execute if score #active edm_seg_ctl matches 112 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p00_p00/fail
