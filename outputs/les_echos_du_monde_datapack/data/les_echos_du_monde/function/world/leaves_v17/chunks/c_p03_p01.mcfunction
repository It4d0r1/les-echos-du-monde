# Exact orphan positions recorded in the original export; preserve other blocks and different leaf states.
execute if block 56 2 31 minecraft:oak_leaves[persistent=false] run setblock 56 2 31 minecraft:air
scoreboard players set c_p03_p01 edm_leaf_fix 1
