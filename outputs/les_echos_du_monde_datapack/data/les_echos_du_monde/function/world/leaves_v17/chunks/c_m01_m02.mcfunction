# Exact orphan positions recorded in the original export; preserve other blocks and different leaf states.
execute if block -14 -1 -27 minecraft:oak_leaves[persistent=true,distance=7,waterlogged=false] run setblock -14 -1 -27 minecraft:air
scoreboard players set c_m01_m02 edm_leaf_fix 1
