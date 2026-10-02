scoreboard players add #wait edm_seg_ctl 2
execute if loaded 0 0 160 if loaded 0 0 176 if loaded 0 0 192 if loaded 16 0 160 if loaded 16 0 176 if loaded 16 0 192 if loaded 32 0 160 if loaded 32 0 176 if loaded 32 0 192 run function les_echos_du_monde:world/segments_v17/segment/s_p00_p05/place
execute if score #active edm_seg_ctl matches 117 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p00_p05/fail
