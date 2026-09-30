# Initialise les regles et points par defaut une fois par sauvegarde.
execute unless data storage les_echos_du_monde:state initialized run function les_echos_du_monde:world/initialize
# Efface les anciens marqueurs et annule l'ancienne chaine de 32 tranches, une seule fois.
execute unless data storage les_echos_du_monde:state platform_chunk_migrated run function les_echos_du_monde:world/migrate_platform_marker
# Prepare le score necessaire au resultat de /place template.
execute unless data storage les_echos_du_monde:state platform_score_ready run function les_echos_du_monde:world/setup_platform_score

# Suspend l'arrivee, la sortie automatique et le placement de la plateforme.
execute unless data storage les_echos_du_monde:state {prologue_automation_paused:1b} run function les_echos_du_monde:world/pause_automation
