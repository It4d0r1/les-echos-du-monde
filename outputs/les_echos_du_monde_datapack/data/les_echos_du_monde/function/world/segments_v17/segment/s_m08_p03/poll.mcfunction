scoreboard players add #wait edm_seg_ctl 2
execute if loaded -256 0 96 if loaded -256 0 112 if loaded -256 0 128 if loaded -240 0 96 if loaded -240 0 112 if loaded -240 0 128 if loaded -224 0 96 if loaded -224 0 112 if loaded -224 0 128 run function les_echos_du_monde:world/segments_v17/segment/s_m08_p03/place
execute if score #active edm_seg_ctl matches 6 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m08_p03/fail
