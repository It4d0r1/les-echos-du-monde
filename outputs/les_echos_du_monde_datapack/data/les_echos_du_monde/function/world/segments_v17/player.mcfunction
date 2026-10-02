# data get floors coordinates, including negatives; integer ranges avoid selector bounding-box overlap.
execute store result score #px edm_seg_tmp run data get entity @s Pos[0] 1
execute store result score #pz edm_seg_tmp run data get entity @s Pos[2] 1
scoreboard players set #safe edm_seg_tmp 0
execute if score #px edm_seg_tmp matches -256..-225 run function les_echos_du_monde:world/segments_v17/dispatch/x_m08
execute if score #px edm_seg_tmp matches -224..-193 run function les_echos_du_monde:world/segments_v17/dispatch/x_m07
execute if score #px edm_seg_tmp matches -192..-161 run function les_echos_du_monde:world/segments_v17/dispatch/x_m06
execute if score #px edm_seg_tmp matches -160..-129 run function les_echos_du_monde:world/segments_v17/dispatch/x_m05
execute if score #px edm_seg_tmp matches -128..-97 run function les_echos_du_monde:world/segments_v17/dispatch/x_m04
execute if score #px edm_seg_tmp matches -96..-65 run function les_echos_du_monde:world/segments_v17/dispatch/x_m03
execute if score #px edm_seg_tmp matches -64..-33 run function les_echos_du_monde:world/segments_v17/dispatch/x_m02
execute if score #px edm_seg_tmp matches -32..-1 run function les_echos_du_monde:world/segments_v17/dispatch/x_m01
execute if score #px edm_seg_tmp matches 0..31 run function les_echos_du_monde:world/segments_v17/dispatch/x_p00
execute if score #px edm_seg_tmp matches 32..63 run function les_echos_du_monde:world/segments_v17/dispatch/x_p01
execute if score #px edm_seg_tmp matches 64..95 run function les_echos_du_monde:world/segments_v17/dispatch/x_p02
execute if score #px edm_seg_tmp matches 96..127 run function les_echos_du_monde:world/segments_v17/dispatch/x_p03
execute if score #px edm_seg_tmp matches 128..159 run function les_echos_du_monde:world/segments_v17/dispatch/x_p04
execute if score #px edm_seg_tmp matches 160..191 run function les_echos_du_monde:world/segments_v17/dispatch/x_p05
execute if score #px edm_seg_tmp matches 192..223 run function les_echos_du_monde:world/segments_v17/dispatch/x_p06
# Partial border cells contain empty padding outside the exported structure.
execute if score #px edm_seg_tmp matches ..-251 run scoreboard players set #safe edm_seg_tmp 0
execute if score #px edm_seg_tmp matches 201.. run scoreboard players set #safe edm_seg_tmp 0
execute if score #pz edm_seg_tmp matches ..-236 run scoreboard players set #safe edm_seg_tmp 0
execute if score #pz edm_seg_tmp matches 226.. run scoreboard players set #safe edm_seg_tmp 0
execute unless entity @s[gamemode=creative] unless entity @s[gamemode=spectator] unless score #safe edm_seg_tmp matches 1 if data storage les_echos_du_monde:segments_v17 {spawn_ready:1b} run function les_echos_du_monde:world/segments_v17/transfer
