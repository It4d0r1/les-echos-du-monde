execute if score #owned0 edm_seg_ctl matches 1 run forceload remove 160 96
execute if score #owned1 edm_seg_ctl matches 1 run forceload remove 160 112
execute if score #owned2 edm_seg_ctl matches 1 run forceload remove 160 128
execute if score #owned3 edm_seg_ctl matches 1 run forceload remove 176 96
execute if score #owned4 edm_seg_ctl matches 1 run forceload remove 176 112
execute if score #owned5 edm_seg_ctl matches 1 run forceload remove 176 128
execute if score #owned6 edm_seg_ctl matches 1 run forceload remove 192 96
execute if score #owned7 edm_seg_ctl matches 1 run forceload remove 192 112
execute if score #owned8 edm_seg_ctl matches 1 run forceload remove 192 128
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
