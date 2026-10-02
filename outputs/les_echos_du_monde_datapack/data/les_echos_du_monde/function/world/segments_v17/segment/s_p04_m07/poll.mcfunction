scoreboard players add #wait edm_seg_ctl 2
execute if loaded 128 0 -224 if loaded 128 0 -208 if loaded 128 0 -192 if loaded 144 0 -224 if loaded 144 0 -208 if loaded 144 0 -192 if loaded 160 0 -224 if loaded 160 0 -208 if loaded 160 0 -192 run function les_echos_du_monde:world/segments_v17/segment/s_p04_m07/place
execute if score #active edm_seg_ctl matches 163 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p04_m07/fail
