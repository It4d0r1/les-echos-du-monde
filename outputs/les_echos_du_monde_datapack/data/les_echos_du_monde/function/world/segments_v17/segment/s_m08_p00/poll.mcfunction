scoreboard players add #wait edm_seg_ctl 2
execute if loaded -256 0 0 if loaded -256 0 16 if loaded -256 0 32 if loaded -240 0 0 if loaded -240 0 16 if loaded -240 0 32 if loaded -224 0 0 if loaded -224 0 16 if loaded -224 0 32 run function les_echos_du_monde:world/segments_v17/segment/s_m08_p00/place
execute if score #active edm_seg_ctl matches 3 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m08_p00/fail
