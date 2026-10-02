scoreboard players add #wait edm_seg_ctl 2
execute if loaded 128 0 0 if loaded 128 0 16 if loaded 128 0 32 if loaded 144 0 0 if loaded 144 0 16 if loaded 144 0 32 if loaded 160 0 0 if loaded 160 0 16 if loaded 160 0 32 run function les_echos_du_monde:world/segments_v17/segment/s_p04_p00/place
execute if score #active edm_seg_ctl matches 170 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p04_p00/fail
