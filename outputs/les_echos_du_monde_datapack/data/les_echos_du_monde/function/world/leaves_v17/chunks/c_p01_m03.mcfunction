# Exact orphan positions recorded in the original export; preserve other blocks and different leaf states.
execute if block 31 -2 -34 minecraft:oak_leaves[persistent=true,distance=7,waterlogged=false] run setblock 31 -2 -34 minecraft:air
scoreboard players set c_p01_m03 edm_leaf_fix 1
