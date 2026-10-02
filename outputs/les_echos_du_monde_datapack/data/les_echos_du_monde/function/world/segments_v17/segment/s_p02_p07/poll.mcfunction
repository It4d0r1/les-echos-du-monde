scoreboard players add #wait edm_seg_ctl 2
execute if loaded 64 0 224 if loaded 64 0 240 if loaded 64 0 256 if loaded 80 0 224 if loaded 80 0 240 if loaded 80 0 256 if loaded 96 0 224 if loaded 96 0 240 if loaded 96 0 256 run function les_echos_du_monde:world/segments_v17/segment/s_p02_p07/place
execute if score #active edm_seg_ctl matches 148 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p02_p07/fail
