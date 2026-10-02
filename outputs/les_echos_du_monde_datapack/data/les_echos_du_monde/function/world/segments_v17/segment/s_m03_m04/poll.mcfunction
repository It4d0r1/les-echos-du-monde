scoreboard players add #wait edm_seg_ctl 2
execute if loaded -96 0 -128 if loaded -96 0 -112 if loaded -96 0 -96 if loaded -80 0 -128 if loaded -80 0 -112 if loaded -80 0 -96 if loaded -64 0 -128 if loaded -64 0 -112 if loaded -64 0 -96 run function les_echos_du_monde:world/segments_v17/segment/s_m03_m04/place
execute if score #active edm_seg_ctl matches 61 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m03_m04/fail
