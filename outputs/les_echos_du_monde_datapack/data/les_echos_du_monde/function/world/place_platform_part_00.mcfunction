# Tranche 1/32 ; plage Z d’origine 0–15.
execute store success score #edm_platform edm_internal in les_echos_du_monde:prologue run place template les_echos_du_monde:plateforme_prologue_slice_00 -224 -56 -243
execute if score #edm_platform edm_internal matches 1 run schedule function les_echos_du_monde:world/place_platform_part_01 1t
execute unless score #edm_platform edm_internal matches 1 run data modify storage les_echos_du_monde:state platform_error set value 1b
