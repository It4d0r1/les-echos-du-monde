# Only called when this runtime has never been initialized in this world.
data modify storage les_echos_du_monde:segments_v17 runtime_initialized set value 1b
data modify storage les_echos_du_monde:segments_v17 layout set value "segments_v17"
# Diagnostic metadata; these compiled values are not editable runtime settings.
data modify storage les_echos_du_monde:segments_v17 generated_settings set value {radius_segments:2,max_placements_per_two_ticks:1,timeout_ticks:100,max_failures_per_segment:3}
data modify storage les_echos_du_monde:segments_v17 spawn_ready set value 0b
scoreboard players set #enabled edm_seg_ctl 1
scoreboard players set #active edm_seg_ctl -1
scoreboard players set #wait edm_seg_ctl 0
scoreboard players set #completed edm_seg_ctl 0
