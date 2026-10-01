# Evite de superposer automatiquement deux modeles d'origines differentes dans une ancienne sauvegarde.
function les_echos_du_monde:world/pause_automation
data modify storage les_echos_du_monde:state platform_requires_new_world set value 1b
