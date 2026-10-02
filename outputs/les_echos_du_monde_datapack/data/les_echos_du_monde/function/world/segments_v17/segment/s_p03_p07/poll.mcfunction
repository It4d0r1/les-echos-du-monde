scoreboard players add #wait edm_seg_ctl 2
execute if loaded 96 0 224 if loaded 96 0 240 if loaded 96 0 256 if loaded 112 0 224 if loaded 112 0 240 if loaded 112 0 256 if loaded 128 0 224 if loaded 128 0 240 if loaded 128 0 256 run function les_echos_du_monde:world/segments_v17/segment/s_p03_p07/place
execute if score #active edm_seg_ctl matches 162 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p03_p07/fail
