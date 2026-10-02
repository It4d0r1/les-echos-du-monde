scoreboard players add #wait edm_seg_ctl 2
execute if loaded 160 0 -96 if loaded 160 0 -80 if loaded 160 0 -64 if loaded 176 0 -96 if loaded 176 0 -80 if loaded 176 0 -64 if loaded 192 0 -96 if loaded 192 0 -80 if loaded 192 0 -64 run function les_echos_du_monde:world/segments_v17/segment/s_p05_m03/place
execute if score #active edm_seg_ctl matches 182 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p05_m03/fail
