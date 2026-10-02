scoreboard players add #wait edm_seg_ctl 2
execute if loaded 96 0 0 if loaded 96 0 16 if loaded 96 0 32 if loaded 112 0 0 if loaded 112 0 16 if loaded 112 0 32 if loaded 128 0 0 if loaded 128 0 16 if loaded 128 0 32 run function les_echos_du_monde:world/segments_v17/segment/s_p03_p00/place
execute if score #active edm_seg_ctl matches 155 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p03_p00/fail
