scoreboard players add #wait edm_seg_ctl 2
execute if loaded -256 0 128 if loaded -256 0 144 if loaded -256 0 160 if loaded -240 0 128 if loaded -240 0 144 if loaded -240 0 160 if loaded -224 0 128 if loaded -224 0 144 if loaded -224 0 160 run function les_echos_du_monde:world/segments_v17/segment/s_m08_p04/place
execute if score #active edm_seg_ctl matches 7 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_m08_p04/fail
