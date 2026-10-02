scoreboard players add #wait edm_seg_ctl 2
execute if loaded 160 0 -256 if loaded 160 0 -240 if loaded 160 0 -224 if loaded 176 0 -256 if loaded 176 0 -240 if loaded 176 0 -224 if loaded 192 0 -256 if loaded 192 0 -240 if loaded 192 0 -224 run function les_echos_du_monde:world/segments_v17/segment/s_p05_m08/place
execute if score #active edm_seg_ctl matches 177 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p05_m08/fail
