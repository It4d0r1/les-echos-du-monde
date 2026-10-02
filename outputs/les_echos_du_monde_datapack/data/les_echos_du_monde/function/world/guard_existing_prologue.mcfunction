# Cancel previous placement chains once, retaining their ownership cleanup.
execute unless data storage les_echos_du_monde:state legacy_cleanup_done run function les_echos_du_monde:world/pause_legacy_automation
data modify storage les_echos_du_monde:state legacy_cleanup_done set value 1b
function les_echos_du_monde:world/pause_automation
data modify storage les_echos_du_monde:state platform_requires_new_world set value 1b
