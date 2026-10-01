# Nouveau monde : initialise l'origine de cette version. Ancien monde : pause explicite.
execute unless data storage les_echos_du_monde:state initialized run function les_echos_du_monde:world/initialize
execute unless data storage les_echos_du_monde:state platform_score_ready run function les_echos_du_monde:world/setup_platform_score
execute unless data storage les_echos_du_monde:state {platform_layout:"vegetation_20261001"} run function les_echos_du_monde:world/guard_existing_prologue
scoreboard players set #platform_ui_clock edm_internal 0
