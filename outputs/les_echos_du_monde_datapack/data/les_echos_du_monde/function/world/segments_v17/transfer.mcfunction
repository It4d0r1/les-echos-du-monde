# Fail-safe if flight or fast movement reaches terrain not yet placed.
execute unless data storage les_echos_du_monde:segments_v17 {spawn_ready:1b} run return 0
function les_echos_du_monde:player/teleport_to_prologue
title @s actionbar {"text":"Le terrain devant vous se prépare…","color":"yellow"}
