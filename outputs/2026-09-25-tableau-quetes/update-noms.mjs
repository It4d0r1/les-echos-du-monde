import fs from 'node:fs/promises';
const base='outputs/2026-09-25-tableau-quetes';
let mmd=await fs.readFile(`${base}/legendaries-artikodin.mmd`,'utf8');
mmd=mmd.replace('A --> P1["Pokémon 1"]','A --> P1["Mew"]').replace('A --> P2["Pokémon 2"]','A --> P2["Artikodin"]');
await fs.writeFile(`${base}/legendaries-noms.mmd`,mmd,'utf8');
let svg=await fs.readFile(`${base}/arbre-legendaire-artikodin.svg`,'utf8');
svg=svg.replace('>Pokémon 1</text>','>Mew</text>').replace('>Pokémon 2</text>','>Artikodin</text>');
svg=svg.replace('Quinze branches Pokémon génériques. La branche Artikodin mène au Sanctuaire glacé, puis à deux objectifs en parallèle — trouver la pierre de glace et battre 375 Pokémon — avant de converger vers la capture d’Artikodin.','Quinze branches partent de Départ : Mew, Artikodin et Pokémon 3 à 15. La branche spécifique Artikodin mène au Sanctuaire glacé, puis à deux objectifs en parallèle — trouver la pierre de glace et battre 375 Pokémon — avant la capture.');
await fs.writeFile(`${base}/arbre-legendaire-noms.svg`,svg,'utf8');
