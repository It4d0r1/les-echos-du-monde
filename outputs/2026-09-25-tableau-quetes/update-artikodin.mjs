import fs from 'node:fs/promises';
const out='outputs/2026-09-25-tableau-quetes';
const lines=['flowchart LR','    subgraph MF["Les Mythes oubliés"]','        A([Départ])'];
for(let i=1;i<=15;i++) lines.push(`        A --> P${i}["Pokémon ${i}"]`);
lines.push('        A --> ART["Artikodin"]','        ART --> S["Trouver le Sanctuaire glacé"]','        S --> ICE["Trouver la pierre de glace"]','        S --> B["Battre 375 Pokémon"]','        ICE --> C["Capturer Artikodin"]','        B --> C','    end','    classDef planned fill:#5a4a20,color:#ffffff,stroke:#e4c45a,stroke-width:2px;','    class ART,S,ICE,B,C planned;','');
await fs.writeFile(`${out}/legendaries-artikodin.mmd`,lines.join('\n'),'utf8');
const firstY=120,step=84,startY=750;
const paths=[];
for(let i=0;i<15;i++){const y=firstY+i*step;paths.push(`<path class="edge" d="M 194 ${startY} C 310 ${startY}, 340 ${y+28}, 470 ${y+28}"/>`);}
const cards=[];
for(let i=0;i<15;i++){const y=firstY+i*step,cy=y+28;cards.push(`<g><rect class="node" x="470" y="${y}" width="340" height="56"/><text class="label" x="640" y="${cy+8}" text-anchor="middle">Pokémon ${i+1}</text></g>`);}
const artY=1370;
const artCy=artY+35;
paths.push(`<path class="edge" d="M 194 ${startY} C 310 ${startY}, 340 ${artCy}, 470 ${artCy}"/>`);
paths.push(`<path class="edge" d="M 700 ${artCy} H 780"/>`);
paths.push(`<path class="edge" d="M 1140 1405 C 1180 1405, 1180 1350, 1220 1350"/>`);
paths.push(`<path class="edge" d="M 1140 1405 C 1180 1405, 1180 1470, 1220 1470"/>`);
paths.push(`<path class="edge" d="M 1580 1350 C 1620 1350, 1620 1405, 1660 1405"/>`);
paths.push(`<path class="edge" d="M 1580 1470 C 1620 1470, 1620 1405, 1660 1405"/>`);
cards.push(`<g><rect class="task" x="470" y="${artY}" width="230" height="70"/><text class="label" x="585" y="${artCy+8}" text-anchor="middle">Artikodin</text></g>`);
cards.push(`<g><rect class="task" x="780" y="1370" width="360" height="70"/><text class="label" x="960" y="${artCy+8}" text-anchor="middle">Trouver le Sanctuaire glacé</text></g>`);
cards.push(`<g><rect class="task" x="1220" y="1320" width="360" height="60"/><text class="label" x="1400" y="1357" text-anchor="middle">Trouver la pierre de glace</text></g>`);
cards.push(`<g><rect class="task" x="1220" y="1440" width="360" height="60"/><text class="label" x="1400" y="1477" text-anchor="middle">Battre 375 Pokémon</text></g>`);
cards.push(`<g><rect class="task" x="1660" y="1375" width="310" height="60"/><text class="label" x="1815" y="1412" text-anchor="middle">Capturer Artikodin</text></g>`);
const width=2030,height=1570;
const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="title desc">
<title id="title">Les Mythes oubliés — branche Artikodin</title><desc id="desc">Quinze branches Pokémon génériques. La branche Artikodin mène au Sanctuaire glacé, puis à deux objectifs en parallèle — trouver la pierre de glace et battre 375 Pokémon — avant de converger vers la capture d’Artikodin.</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#95a2b0"/></marker>
<style>.edge{fill:none;stroke:#95a2b0;stroke-width:2.5;marker-end:url(#arrow)}.node{fill:#303843;stroke:#909ca8;stroke-width:2.5;rx:14}.task{fill:#5a4a20;stroke:#e4c45a;stroke-width:2.5;rx:14}.start{fill:#454e57;stroke:#c2ccd4;stroke-width:3}.title{font:600 30px 'Segoe UI',Arial,sans-serif;fill:#f2f5f7}.label{font:500 22px 'Segoe UI',Arial,sans-serif;fill:#f2f5f7}.caption{font:400 17px 'Segoe UI',Arial,sans-serif;fill:#e8ddb9}</style></defs>
<rect width="${width}" height="${height}" fill="#1c232c"/><text class="title" x="48" y="52">Les Mythes oubliés</text><text class="caption" x="48" y="81">Branche Artikodin · étapes vers l’obtention du légendaire</text>
${paths.join('\n')}
<circle class="start" cx="140" cy="${startY}" r="54"/><text class="label" x="140" y="${startY+8}" text-anchor="middle">Départ</text>
${cards.join('\n')}
</svg>`;
await fs.writeFile(`${out}/arbre-legendaire-artikodin.svg`,svg,'utf8');
