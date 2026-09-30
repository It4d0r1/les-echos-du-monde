import fs from 'node:fs/promises';
const out='outputs/2026-09-25-tableau-quetes';
const lines=['flowchart LR','    subgraph MF["Les Mythes oubliés"]','        A([Départ])'];
for (let i=1;i<=15;i++) lines.push(`        A --> P${i}["Pokémon ${i}"]`);
lines.push('        A --> ART["Artikodin"] --> TART["Tâche à préciser"]','    end','');
await fs.writeFile(`${out}/legendaries.mmd`,lines.join('\n'),'utf8');
const firstY=120, step=84, count=16, startY=firstY+(count-1)*step/2;
const paths=[];
for(let i=0;i<count;i++){
 const y=firstY+i*step;
 paths.push(`<path class="edge" d="M 194 ${startY} C 310 ${startY}, 340 ${y}, 470 ${y}"/>`);
}
const cards=[];
for(let i=0;i<15;i++){
 const y=firstY+i*step, cy=y+28;
 cards.push(`<g><rect class="node" x="470" y="${y}" width="340" height="56"/><text class="label" x="640" y="${cy+8}" text-anchor="middle">Pokémon ${i+1}</text></g>`);
}
const artY=firstY+15*step, cy=artY+28;
cards.push(`<g><rect class="node" x="470" y="${artY}" width="290" height="56"/><text class="label" x="615" y="${cy+8}" text-anchor="middle">Artikodin</text></g>`);
paths.push(`<path class="edge" d="M 760 ${cy} H 850"/>`);
cards.push(`<g><rect class="task" x="850" y="${artY}" width="390" height="56"/><text class="label" x="1045" y="${cy+8}" text-anchor="middle">Tâche à préciser</text></g>`);
const height=firstY+(count-1)*step+100;
const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="${height}" viewBox="0 0 1320 ${height}" role="img" aria-labelledby="title desc">
<title id="title">Les Mythes oubliés — branches de Pokémon</title>
<desc id="desc">Seize branches partent directement de Départ : Pokémon 1 à Pokémon 15, et une branche Artikodin avec un emplacement pour sa tâche.</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#95a2b0"/></marker>
<style>.edge{fill:none;stroke:#95a2b0;stroke-width:2.5;marker-end:url(#arrow)}.node{fill:#303843;stroke:#909ca8;stroke-width:2.5;rx:14}.task{fill:#443b29;stroke:#d8b663;stroke-width:2.5;rx:14}.start{fill:#454e57;stroke:#c2ccd4;stroke-width:3}.title{font:600 30px 'Segoe UI',Arial,sans-serif;fill:#f2f5f7}.label{font:500 22px 'Segoe UI',Arial,sans-serif;fill:#f2f5f7}.caption{font:400 17px 'Segoe UI',Arial,sans-serif;fill:#c1cbd4}</style></defs>
<rect width="1320" height="${height}" fill="#1c232c"/>
<text class="title" x="48" y="52">Les Mythes oubliés</text><text class="caption" x="48" y="81">16 branches · noms provisoires sauf Artikodin</text>
${paths.join('\n')}
<circle class="start" cx="140" cy="${startY}" r="54"/><text class="label" x="140" y="${startY+8}" text-anchor="middle">Départ</text>
${cards.join('\n')}
</svg>`;
await fs.writeFile(`${out}/arbre-legendaire.svg`,svg,'utf8');
