execute unless data storage les_echos_du_monde:state {platform_layout:"segments_v17"} run return 0
execute if data storage les_echos_du_monde:state {prologue_automation_paused:1b} run return 0
execute unless score #enabled edm_seg_ctl matches 1 run return 0
# Inspect only already placed, loaded chunks. This repair adds no force-load tickets.
execute in les_echos_du_monde:prologue if score s_m02_m01 edm_seg_done matches 1 unless score c_m03_m01 edm_leaf_fix matches 1 if loaded -48 0 -16 run function les_echos_du_monde:world/leaves_v17/chunks/c_m03_m01
execute in les_echos_du_monde:prologue if score s_m02_p00 edm_seg_done matches 1 unless score c_m03_p00 edm_leaf_fix matches 1 if loaded -48 0 0 run function les_echos_du_monde:world/leaves_v17/chunks/c_m03_p00
execute in les_echos_du_monde:prologue if score s_m02_p00 edm_seg_done matches 1 unless score c_m03_p01 edm_leaf_fix matches 1 if loaded -48 0 16 run function les_echos_du_monde:world/leaves_v17/chunks/c_m03_p01
execute in les_echos_du_monde:prologue if score s_m01_m01 edm_seg_done matches 1 unless score c_m02_m01 edm_leaf_fix matches 1 if loaded -32 0 -16 run function les_echos_du_monde:world/leaves_v17/chunks/c_m02_m01
execute in les_echos_du_monde:prologue if score s_m01_p00 edm_seg_done matches 1 unless score c_m02_p00 edm_leaf_fix matches 1 if loaded -32 0 0 run function les_echos_du_monde:world/leaves_v17/chunks/c_m02_p00
execute in les_echos_du_monde:prologue if score s_m01_m01 edm_seg_done matches 1 unless score c_m01_m02 edm_leaf_fix matches 1 if loaded -16 0 -32 run function les_echos_du_monde:world/leaves_v17/chunks/c_m01_m02
execute in les_echos_du_monde:prologue if score s_m01_m01 edm_seg_done matches 1 unless score c_m01_m01 edm_leaf_fix matches 1 if loaded -16 0 -16 run function les_echos_du_monde:world/leaves_v17/chunks/c_m01_m01
execute in les_echos_du_monde:prologue if score s_m01_p00 edm_seg_done matches 1 unless score c_m01_p00 edm_leaf_fix matches 1 if loaded -16 0 0 run function les_echos_du_monde:world/leaves_v17/chunks/c_m01_p00
execute in les_echos_du_monde:prologue if score s_p00_m02 edm_seg_done matches 1 unless score c_p01_m03 edm_leaf_fix matches 1 if loaded 16 0 -48 run function les_echos_du_monde:world/leaves_v17/chunks/c_p01_m03
execute in les_echos_du_monde:prologue if score s_p00_m01 edm_seg_done matches 1 unless score c_p01_m02 edm_leaf_fix matches 1 if loaded 16 0 -32 run function les_echos_du_monde:world/leaves_v17/chunks/c_p01_m02
execute in les_echos_du_monde:prologue if score s_p01_m02 edm_seg_done matches 1 unless score c_p03_m04 edm_leaf_fix matches 1 if loaded 48 0 -64 run function les_echos_du_monde:world/leaves_v17/chunks/c_p03_m04
execute in les_echos_du_monde:prologue if score s_p01_p00 edm_seg_done matches 1 unless score c_p03_p01 edm_leaf_fix matches 1 if loaded 48 0 16 run function les_echos_du_monde:world/leaves_v17/chunks/c_p03_p01
