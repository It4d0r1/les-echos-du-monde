scoreboard players add #wait edm_seg_ctl 2
execute if loaded 96 0 192 if loaded 96 0 208 if loaded 96 0 224 if loaded 112 0 192 if loaded 112 0 208 if loaded 112 0 224 if loaded 128 0 192 if loaded 128 0 208 if loaded 128 0 224 run function les_echos_du_monde:world/segments_v17/segment/s_p03_p06/place
execute if score #active edm_seg_ctl matches 161 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p03_p06/fail
