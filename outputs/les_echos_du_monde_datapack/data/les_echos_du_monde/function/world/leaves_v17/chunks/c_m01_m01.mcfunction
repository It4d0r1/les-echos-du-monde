# Exact orphan positions recorded in the original export; preserve other blocks and different leaf states.
execute if block -13 -1 -1 minecraft:oak_leaves[persistent=false] run setblock -13 -1 -1 minecraft:air
execute if block -12 -1 -1 minecraft:oak_leaves[persistent=false] run setblock -12 -1 -1 minecraft:air
execute if block -11 -1 -1 minecraft:oak_leaves[persistent=false] run setblock -11 -1 -1 minecraft:air
scoreboard players set c_m01_m01 edm_leaf_fix 1
