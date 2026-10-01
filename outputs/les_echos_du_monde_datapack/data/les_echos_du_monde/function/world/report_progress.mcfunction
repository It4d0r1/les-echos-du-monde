scoreboard players set #platform_ui_clock edm_internal 0
execute as @a[tag=!edm_prologue_done] run title @s actionbar [{"text":"Préparation du prologue : ","color":"gold"},{"score":{"name":"#platform_progress","objective":"edm_internal"}},{"text":" / "},{"score":{"name":"#platform_total","objective":"edm_internal"}}]
