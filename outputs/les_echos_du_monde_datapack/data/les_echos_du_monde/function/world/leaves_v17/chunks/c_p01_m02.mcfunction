# Exact orphan positions recorded in the original export; preserve other blocks and different leaf states.
execute if block 29 -2 -32 minecraft:oak_leaves[persistent=true,distance=7,waterlogged=false] run setblock 29 -2 -32 minecraft:air
scoreboard players set c_p01_m02 edm_leaf_fix 1
