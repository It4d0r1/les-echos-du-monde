# New worlds only. Do not reset existing platform/player progress.
setworldspawn 0 80 0
gamerule spawnRadius 0
data modify storage les_echos_du_monde:state initialized set value 1b
data modify storage les_echos_du_monde:state platform_layout set value "segments_v17"
data remove storage les_echos_du_monde:state prologue_automation_paused
data remove storage les_echos_du_monde:state platform_requires_new_world
