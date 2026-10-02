execute unless score #budget edm_seg_ctl matches 1 run return 0
execute if score #active edm_seg_ctl matches 0.. run return 0
scoreboard players set #budget edm_seg_ctl 0
scoreboard players set #active edm_seg_ctl 157
scoreboard players set #wait edm_seg_ctl 0
data modify storage les_echos_du_monde:segments_v17 active set value "s_p03_p02"
scoreboard players set #owned0 edm_seg_ctl 0
scoreboard players set #forced0 edm_seg_ctl 0
execute store success score #forced0 edm_seg_ctl run forceload query 96 64
execute unless score #forced0 edm_seg_ctl matches 1 store success score #owned0 edm_seg_ctl run forceload add 96 64
scoreboard players set #owned1 edm_seg_ctl 0
scoreboard players set #forced1 edm_seg_ctl 0
execute store success score #forced1 edm_seg_ctl run forceload query 96 80
execute unless score #forced1 edm_seg_ctl matches 1 store success score #owned1 edm_seg_ctl run forceload add 96 80
scoreboard players set #owned2 edm_seg_ctl 0
scoreboard players set #forced2 edm_seg_ctl 0
execute store success score #forced2 edm_seg_ctl run forceload query 96 96
execute unless score #forced2 edm_seg_ctl matches 1 store success score #owned2 edm_seg_ctl run forceload add 96 96
scoreboard players set #owned3 edm_seg_ctl 0
scoreboard players set #forced3 edm_seg_ctl 0
execute store success score #forced3 edm_seg_ctl run forceload query 112 64
execute unless score #forced3 edm_seg_ctl matches 1 store success score #owned3 edm_seg_ctl run forceload add 112 64
scoreboard players set #owned4 edm_seg_ctl 0
scoreboard players set #forced4 edm_seg_ctl 0
execute store success score #forced4 edm_seg_ctl run forceload query 112 80
execute unless score #forced4 edm_seg_ctl matches 1 store success score #owned4 edm_seg_ctl run forceload add 112 80
scoreboard players set #owned5 edm_seg_ctl 0
scoreboard players set #forced5 edm_seg_ctl 0
execute store success score #forced5 edm_seg_ctl run forceload query 112 96
execute unless score #forced5 edm_seg_ctl matches 1 store success score #owned5 edm_seg_ctl run forceload add 112 96
scoreboard players set #owned6 edm_seg_ctl 0
scoreboard players set #forced6 edm_seg_ctl 0
execute store success score #forced6 edm_seg_ctl run forceload query 128 64
execute unless score #forced6 edm_seg_ctl matches 1 store success score #owned6 edm_seg_ctl run forceload add 128 64
scoreboard players set #owned7 edm_seg_ctl 0
scoreboard players set #forced7 edm_seg_ctl 0
execute store success score #forced7 edm_seg_ctl run forceload query 128 80
execute unless score #forced7 edm_seg_ctl matches 1 store success score #owned7 edm_seg_ctl run forceload add 128 80
scoreboard players set #owned8 edm_seg_ctl 0
scoreboard players set #forced8 edm_seg_ctl 0
execute store success score #forced8 edm_seg_ctl run forceload query 128 96
execute unless score #forced8 edm_seg_ctl matches 1 store success score #owned8 edm_seg_ctl run forceload add 128 96
