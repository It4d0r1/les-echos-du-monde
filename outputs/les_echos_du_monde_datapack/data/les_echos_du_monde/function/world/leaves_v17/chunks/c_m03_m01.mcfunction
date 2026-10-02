# Exact orphan positions recorded in the original export; preserve other blocks and different leaf states.
execute if block -40 -3 -14 minecraft:oak_leaves[persistent=true,distance=7,waterlogged=false] run setblock -40 -3 -14 minecraft:air
scoreboard players set c_m03_m01 edm_leaf_fix 1
