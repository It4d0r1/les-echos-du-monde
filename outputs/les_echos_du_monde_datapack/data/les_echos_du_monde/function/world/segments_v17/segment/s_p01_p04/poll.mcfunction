scoreboard players add #wait edm_seg_ctl 2
execute if loaded 32 0 128 if loaded 32 0 144 if loaded 32 0 160 if loaded 48 0 128 if loaded 48 0 144 if loaded 48 0 160 if loaded 64 0 128 if loaded 64 0 144 if loaded 64 0 160 run function les_echos_du_monde:world/segments_v17/segment/s_p01_p04/place
execute if score #active edm_seg_ctl matches 131 if score #wait edm_seg_ctl matches 100.. run function les_echos_du_monde:world/segments_v17/segment/s_p01_p04/fail
