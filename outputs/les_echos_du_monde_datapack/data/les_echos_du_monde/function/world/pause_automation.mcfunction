# Pause generation and first arrival. The automatic exit remains available.
data modify storage les_echos_du_monde:state prologue_automation_paused set value 1b
function les_echos_du_monde:world/segments_v17/pause_internal
