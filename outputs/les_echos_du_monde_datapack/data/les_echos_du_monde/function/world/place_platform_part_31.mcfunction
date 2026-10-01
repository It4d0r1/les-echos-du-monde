# Tranche 32/32 ; plage Z d’origine 471–485.
execute store success score #edm_platform edm_internal in les_echos_du_monde:prologue run place template les_echos_du_monde:plateforme_prologue_slice_31 -224 -56 228
execute if score #edm_platform edm_internal matches 1 run data modify storage les_echos_du_monde:state platform_placed set value 1b
execute if score #edm_platform edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_error
execute unless score #edm_platform edm_internal matches 1 run data modify storage les_echos_du_monde:state platform_error set value 1b
