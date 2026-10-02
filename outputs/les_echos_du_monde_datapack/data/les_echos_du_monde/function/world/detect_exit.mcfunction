# Box coordinates: X=-1..1, Y=-4..-2, Z=6..8. Change this selector to move the exit.
# Only the current dimension's players are considered, even while generation is paused.
execute in les_echos_du_monde:prologue as @a[tag=edm_prologue_done,x=-1,y=-4,z=6,dx=2,dy=2,dz=2] run function les_echos_du_monde:player/exit
