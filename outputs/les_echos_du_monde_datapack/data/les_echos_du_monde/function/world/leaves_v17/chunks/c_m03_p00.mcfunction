# Exact orphan positions recorded in the original export; preserve other blocks and different leaf states.
execute if block -43 0 13 minecraft:oak_leaves[persistent=false] run setblock -43 0 13 minecraft:air
execute if block -42 -1 13 minecraft:oak_leaves[persistent=false] run setblock -42 -1 13 minecraft:air
execute if block -42 0 12 minecraft:oak_leaves[persistent=false] run setblock -42 0 12 minecraft:air
execute if block -42 0 13 minecraft:oak_leaves[persistent=false] run setblock -42 0 13 minecraft:air
execute if block -42 0 14 minecraft:oak_leaves[persistent=false] run setblock -42 0 14 minecraft:air
execute if block -42 1 13 minecraft:oak_leaves[persistent=false] run setblock -42 1 13 minecraft:air
execute if block -41 0 12 minecraft:oak_leaves[persistent=false] run setblock -41 0 12 minecraft:air
execute if block -41 0 13 minecraft:oak_leaves[persistent=false] run setblock -41 0 13 minecraft:air
execute if block -41 0 14 minecraft:oak_leaves[persistent=false] run setblock -41 0 14 minecraft:air
scoreboard players set c_m03_p00 edm_leaf_fix 1
