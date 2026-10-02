scoreboard players add #wait edm_seg_ctl 2
execute if loaded 128 0 160 if loaded 128 0 176 if loaded 128 0 192 if loaded 144 0 160 if loaded 144 0 176 if loaded 144 0 192 if loaded 160 0 160 if loaded 160 0 176 if loaded 160 0 192 run function les_echos_du_monde:world/segments_v17/segment/s_p04_p05/place
execute if score #active edm_seg_ctl matches 175 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p04_p05/fail
