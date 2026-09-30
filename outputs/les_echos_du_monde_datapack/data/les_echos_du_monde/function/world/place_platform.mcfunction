# Charge la construction Axiom centrée sur X/Z 0.
# Ancre -224 -56 -243 : le bloc de sol central (coordonnées structure 224,51,243)
# arrive en (0,-5,0), juste sous l'arrivée joueur (0.5,-4,0.5).
execute store success score #edm_platform edm_internal in les_echos_du_monde:prologue run place template les_echos_du_monde:plateforme_prologue -224 -56 -243
execute if score #edm_platform edm_internal matches 1 run data modify storage les_echos_du_monde:state platform_placed set value 1b
execute if score #edm_platform edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_error
execute unless score #edm_platform edm_internal matches 1 run data modify storage les_echos_du_monde:state platform_error set value 1b
