execute if score #owned0 edm_seg_ctl matches 1 run forceload remove -32 -160
execute if score #owned1 edm_seg_ctl matches 1 run forceload remove -32 -144
execute if score #owned2 edm_seg_ctl matches 1 run forceload remove -32 -128
execute if score #owned3 edm_seg_ctl matches 1 run forceload remove -16 -160
execute if score #owned4 edm_seg_ctl matches 1 run forceload remove -16 -144
execute if score #owned5 edm_seg_ctl matches 1 run forceload remove -16 -128
execute if score #owned6 edm_seg_ctl matches 1 run forceload remove 0 -160
execute if score #owned7 edm_seg_ctl matches 1 run forceload remove 0 -144
execute if score #owned8 edm_seg_ctl matches 1 run forceload remove 0 -128
scoreboard players set #owned0 edm_seg_ctl 0
scoreboard players set #owned1 edm_seg_ctl 0
scoreboard players set #owned2 edm_seg_ctl 0
scoreboard players set #owned3 edm_seg_ctl 0
scoreboard players set #owned4 edm_seg_ctl 0
scoreboard players set #owned5 edm_seg_ctl 0
scoreboard players set #owned6 edm_seg_ctl 0
scoreboard players set #owned7 edm_seg_ctl 0
scoreboard players set #owned8 edm_seg_ctl 0
scoreboard players set #active edm_seg_ctl -1
data remove storage les_echos_du_monde:segments_v17 active
