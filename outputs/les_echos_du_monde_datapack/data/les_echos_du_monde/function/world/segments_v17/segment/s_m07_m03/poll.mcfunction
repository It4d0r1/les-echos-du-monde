scoreboard players add #wait edm_seg_ctl 2
execute if loaded -224 0 -96 if loaded -224 0 -80 if loaded -224 0 -64 if loaded -208 0 -96 if loaded -208 0 -80 if loaded -208 0 -64 if loaded -192 0 -96 if loaded -192 0 -80 if loaded -192 0 -64 run function les_echos_du_monde:world/segments_v17/segment/s_m07_m03/place
execute if score #active edm_seg_ctl matches 9 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m07_m03/fail
