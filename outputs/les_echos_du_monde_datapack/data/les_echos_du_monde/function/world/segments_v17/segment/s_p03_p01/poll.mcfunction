scoreboard players add #wait edm_seg_ctl 2
execute if loaded 96 0 32 if loaded 96 0 48 if loaded 96 0 64 if loaded 112 0 32 if loaded 112 0 48 if loaded 112 0 64 if loaded 128 0 32 if loaded 128 0 48 if loaded 128 0 64 run function les_echos_du_monde:world/segments_v17/segment/s_p03_p01/place
execute if score #active edm_seg_ctl matches 156 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p03_p01/fail
