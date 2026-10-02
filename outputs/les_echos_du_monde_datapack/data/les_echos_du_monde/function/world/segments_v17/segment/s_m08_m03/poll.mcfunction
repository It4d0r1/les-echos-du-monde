scoreboard players add #wait edm_seg_ctl 2
execute if loaded -256 0 -96 if loaded -256 0 -80 if loaded -256 0 -64 if loaded -240 0 -96 if loaded -240 0 -80 if loaded -240 0 -64 if loaded -224 0 -96 if loaded -224 0 -80 if loaded -224 0 -64 run function les_echos_du_monde:world/segments_v17/segment/s_m08_m03/place
execute if score #active edm_seg_ctl matches 0 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m08_m03/fail
