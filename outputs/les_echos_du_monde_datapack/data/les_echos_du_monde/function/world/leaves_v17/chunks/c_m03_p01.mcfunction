# Exact orphan positions recorded in the original export; preserve other blocks and different leaf states.
execute if block -47 0 22 minecraft:oak_leaves[persistent=false] run setblock -47 0 22 minecraft:air
execute if block -47 0 23 minecraft:oak_leaves[persistent=false] run setblock -47 0 23 minecraft:air
execute if block -46 -1 23 minecraft:oak_leaves[persistent=false] run setblock -46 -1 23 minecraft:air
execute if block -46 0 22 minecraft:oak_leaves[persistent=false] run setblock -46 0 22 minecraft:air
execute if block -46 0 23 minecraft:oak_leaves[persistent=false] run setblock -46 0 23 minecraft:air
execute if block -46 0 24 minecraft:oak_leaves[persistent=false] run setblock -46 0 24 minecraft:air
execute if block -46 1 23 minecraft:oak_leaves[persistent=false] run setblock -46 1 23 minecraft:air
execute if block -45 0 22 minecraft:oak_leaves[persistent=false] run setblock -45 0 22 minecraft:air
execute if block -45 0 23 minecraft:oak_leaves[persistent=false] run setblock -45 0 23 minecraft:air
execute if block -39 -1 25 minecraft:oak_leaves[persistent=false] run setblock -39 -1 25 minecraft:air
execute if block -39 -1 26 minecraft:oak_leaves[persistent=false] run setblock -39 -1 26 minecraft:air
execute if block -39 -1 27 minecraft:oak_leaves[persistent=false] run setblock -39 -1 27 minecraft:air
execute if block -38 -2 26 minecraft:oak_leaves[persistent=false] run setblock -38 -2 26 minecraft:air
execute if block -38 -1 25 minecraft:oak_leaves[persistent=false] run setblock -38 -1 25 minecraft:air
execute if block -38 -1 26 minecraft:oak_leaves[persistent=false] run setblock -38 -1 26 minecraft:air
execute if block -38 -1 27 minecraft:oak_leaves[persistent=false] run setblock -38 -1 27 minecraft:air
execute if block -38 0 26 minecraft:oak_leaves[persistent=false] run setblock -38 0 26 minecraft:air
execute if block -37 -1 26 minecraft:oak_leaves[persistent=false] run setblock -37 -1 26 minecraft:air
scoreboard players set c_m03_p01 edm_leaf_fix 1
