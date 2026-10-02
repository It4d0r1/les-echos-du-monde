# Exact orphan positions recorded in the original export; preserve other blocks and different leaf states.
execute if block -25 0 -3 minecraft:oak_leaves[persistent=false] run setblock -25 0 -3 minecraft:air
execute if block -25 0 -2 minecraft:oak_leaves[persistent=false] run setblock -25 0 -2 minecraft:air
execute if block -25 0 -1 minecraft:oak_leaves[persistent=false] run setblock -25 0 -1 minecraft:air
execute if block -24 -1 -2 minecraft:oak_leaves[persistent=false] run setblock -24 -1 -2 minecraft:air
execute if block -24 0 -3 minecraft:oak_leaves[persistent=false] run setblock -24 0 -3 minecraft:air
execute if block -24 0 -2 minecraft:oak_leaves[persistent=false] run setblock -24 0 -2 minecraft:air
execute if block -24 0 -1 minecraft:oak_leaves[persistent=false] run setblock -24 0 -1 minecraft:air
execute if block -24 1 -2 minecraft:oak_leaves[persistent=false] run setblock -24 1 -2 minecraft:air
execute if block -23 0 -2 minecraft:oak_leaves[persistent=false] run setblock -23 0 -2 minecraft:air
execute if block -23 0 -1 minecraft:oak_leaves[persistent=false] run setblock -23 0 -1 minecraft:air
execute if block -22 0 -1 minecraft:oak_leaves[persistent=false] run setblock -22 0 -1 minecraft:air
execute if block -21 0 -1 minecraft:oak_leaves[persistent=false] run setblock -21 0 -1 minecraft:air
scoreboard players set c_m02_m01 edm_leaf_fix 1
