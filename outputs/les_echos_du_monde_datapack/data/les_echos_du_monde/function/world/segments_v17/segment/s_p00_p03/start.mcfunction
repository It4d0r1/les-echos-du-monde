execute unless score #budget edm_seg_ctl matches 1 run return 0
execute if score #active edm_seg_ctl matches 0.. run return 0
scoreboard players set #budget edm_seg_ctl 0
scoreboard players set #active edm_seg_ctl 115
scoreboard players set #wait edm_seg_ctl 0
data modify storage les_echos_du_monde:segments_v17 active set value "s_p00_p03"
scoreboard players set #owned0 edm_seg_ctl 0
scoreboard players set #forced0 edm_seg_ctl 0
execute store success score #forced0 edm_seg_ctl run forceload query 0 96
execute unless score #forced0 edm_seg_ctl matches 1 store success score #owned0 edm_seg_ctl run forceload add 0 96
scoreboard players set #owned1 edm_seg_ctl 0
scoreboard players set #forced1 edm_seg_ctl 0
execute store success score #forced1 edm_seg_ctl run forceload query 0 112
execute unless score #forced1 edm_seg_ctl matches 1 store success score #owned1 edm_seg_ctl run forceload add 0 112
scoreboard players set #owned2 edm_seg_ctl 0
scoreboard players set #forced2 edm_seg_ctl 0
execute store success score #forced2 edm_seg_ctl run forceload query 0 128
execute unless score #forced2 edm_seg_ctl matches 1 store success score #owned2 edm_seg_ctl run forceload add 0 128
scoreboard players set #owned3 edm_seg_ctl 0
scoreboard players set #forced3 edm_seg_ctl 0
execute store success score #forced3 edm_seg_ctl run forceload query 16 96
execute unless score #forced3 edm_seg_ctl matches 1 store success score #owned3 edm_seg_ctl run forceload add 16 96
scoreboard players set #owned4 edm_seg_ctl 0
scoreboard players set #forced4 edm_seg_ctl 0
execute store success score #forced4 edm_seg_ctl run forceload query 16 112
execute unless score #forced4 edm_seg_ctl matches 1 store success score #owned4 edm_seg_ctl run forceload add 16 112
scoreboard players set #owned5 edm_seg_ctl 0
scoreboard players set #forced5 edm_seg_ctl 0
execute store success score #forced5 edm_seg_ctl run forceload query 16 128
execute unless score #forced5 edm_seg_ctl matches 1 store success score #owned5 edm_seg_ctl run forceload add 16 128
scoreboard players set #owned6 edm_seg_ctl 0
scoreboard players set #forced6 edm_seg_ctl 0
execute store success score #forced6 edm_seg_ctl run forceload query 32 96
execute unless score #forced6 edm_seg_ctl matches 1 store success score #owned6 edm_seg_ctl run forceload add 32 96
scoreboard players set #owned7 edm_seg_ctl 0
scoreboard players set #forced7 edm_seg_ctl 0
execute store success score #forced7 edm_seg_ctl run forceload query 32 112
execute unless score #forced7 edm_seg_ctl matches 1 store success score #owned7 edm_seg_ctl run forceload add 32 112
scoreboard players set #owned8 edm_seg_ctl 0
scoreboard players set #forced8 edm_seg_ctl 0
execute store success score #forced8 edm_seg_ctl run forceload query 32 128
execute unless score #forced8 edm_seg_ctl matches 1 store success score #owned8 edm_seg_ctl run forceload add 32 128
