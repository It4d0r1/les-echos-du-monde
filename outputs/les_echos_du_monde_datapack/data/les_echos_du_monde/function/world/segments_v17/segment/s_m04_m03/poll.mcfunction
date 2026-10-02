scoreboard players add #wait edm_seg_ctl 2
execute if loaded -128 0 -96 if loaded -128 0 -80 if loaded -128 0 -64 if loaded -112 0 -96 if loaded -112 0 -80 if loaded -112 0 -64 if loaded -96 0 -96 if loaded -96 0 -80 if loaded -96 0 -64 run function les_echos_du_monde:world/segments_v17/segment/s_m04_m03/place
execute if score #active edm_seg_ctl matches 47 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m04_m03/fail
