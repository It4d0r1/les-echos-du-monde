scoreboard players add #wait edm_seg_ctl 2
execute if loaded 64 0 64 if loaded 64 0 80 if loaded 64 0 96 if loaded 80 0 64 if loaded 80 0 80 if loaded 80 0 96 if loaded 96 0 64 if loaded 96 0 80 if loaded 96 0 96 run function les_echos_du_monde:world/segments_v17/segment/s_p02_p02/place
execute if score #active edm_seg_ctl matches 143 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p02_p02/fail
