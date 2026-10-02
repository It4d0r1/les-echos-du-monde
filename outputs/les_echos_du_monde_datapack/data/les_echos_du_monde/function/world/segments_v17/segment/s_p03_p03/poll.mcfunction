scoreboard players add #wait edm_seg_ctl 2
execute if loaded 96 0 96 if loaded 96 0 112 if loaded 96 0 128 if loaded 112 0 96 if loaded 112 0 112 if loaded 112 0 128 if loaded 128 0 96 if loaded 128 0 112 if loaded 128 0 128 run function les_echos_du_monde:world/segments_v17/segment/s_p03_p03/place
execute if score #active edm_seg_ctl matches 158 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p03_p03/fail
