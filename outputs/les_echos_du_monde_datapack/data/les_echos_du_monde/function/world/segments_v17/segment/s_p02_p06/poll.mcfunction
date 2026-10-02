scoreboard players add #wait edm_seg_ctl 2
execute if loaded 64 0 192 if loaded 64 0 208 if loaded 64 0 224 if loaded 80 0 192 if loaded 80 0 208 if loaded 80 0 224 if loaded 96 0 192 if loaded 96 0 208 if loaded 96 0 224 run function les_echos_du_monde:world/segments_v17/segment/s_p02_p06/place
execute if score #active edm_seg_ctl matches 147 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p02_p06/fail
