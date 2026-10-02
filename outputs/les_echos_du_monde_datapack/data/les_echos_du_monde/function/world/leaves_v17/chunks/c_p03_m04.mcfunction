# Exact orphan positions recorded in the original export; preserve other blocks and different leaf states.
execute if block 53 -3 -59 minecraft:oak_leaves[persistent=true,distance=7,waterlogged=false] run setblock 53 -3 -59 minecraft:air
execute if block 54 -3 -59 minecraft:oak_leaves[persistent=true,distance=7,waterlogged=false] run setblock 54 -3 -59 minecraft:air
scoreboard players set c_p03_m04 edm_leaf_fix 1
