# Pixelmon — Les Échos du Monde

## Acte I : Un monde inconnu — Prologue

```mermaid
flowchart LR
    A([Début]) --> Q1["01 · Un monde qui n’est pas le mien<br/>🎯 Valider la scène avec Garrick<br/>🎁 5 Poké Balls"]
    Q1 --> Q2["02 · Quelques souvenirs<br/>🎯 Valider la scène avec Garrick<br/>🎁 Outils en pierre"]
    Q2 --> Q3A["03A · Dans la mine !<br/>🟢 Validée"]
    Q2 --> Q3B["03B · Un peu de bois<br/>🟢 Validée"]
    Q2 --> Q3C["03C · Les mains dans la terre<br/>🟢 Validée"]
    Q3A --> Q4["04 · Le repas du soir<br/>🟢 Validée"]
    Q3B --> Q4
    Q3C --> Q4
    Q4 --> Q5A["05A · Des réflexes de Dresseur<br/>Capturer 5 Pokémon · 🟢 Validée"]
    Q4 --> Q5B["05B · Toujours à mes côtés<br/>Faire évoluer 1 Pokémon · 🟢 Validée"]
    Q4 --> Q5C["05C · Prendre soin des siens<br/>Souvenir : Potion · 🟢 Validée"]
    Q5A --> Q6["06 · Sur le chemin<br/>Activer le PokéStop de la gare abandonnée + vaincre 15 Pokémon · 🟢 Validée"]
    Q5B --> Q6
    Q5C --> Q6
    Q6 --> Q7["07 · Peut-être des réponses<br/>🟢 Validée"]
    Q7 --> Q8["08 · L’épreuve de Maëlle<br/>🟢 Validée"]
    Q8 --> Q9["09 · Souvenir<br/>🟢 Validée"]
    Q9 --> Q9A["09A · Un nouveau départ<br/>Résumé du prologue · 🟢 Validée"]

    classDef complete fill:#315d3b,color:#ffffff,stroke:#8fce00,stroke-width:2px;
    classDef planned fill:#5a4a20,color:#ffffff,stroke:#e4c45a,stroke-width:2px;
    class Q1,Q2 complete;
    class Q3A,Q3B,Q3C,Q4,Q5A,Q5B,Q5C,Q6,Q7,Q8,Q9,Q9A complete;
```

| N° | Quête | Objectif principal | Récompense | État |
|---:|---|---|---|---|
| 1 | Un monde qui n’est pas le mien | Valider la scène avec Garrick | 5 Poké Balls | Terminée |
| 2 | Quelques souvenirs | Valider la scène avec Garrick | Pioche, hache, pelle et houe en pierre | Terminée |
| 3A | Dans la mine ! | 32 pierres, 1 four et 16 charbons | 16 torches + récompense supplémentaire à définir | Validée |
| 3B | Un peu de bois | 32 bûches et 1 pousse d’arbre | À définir | Validée |
| 3C | Les mains dans la terre | Obtenir 8 blés et 4 graines de blé | 4 pommes de terre cuites | Validée |
| 4 | Le repas du soir | Reparler à Garrick | 8 pains | Validée |
| 5A | Des réflexes de Dresseur | Capturer 5 Pokémon | 1 000 Pokédollars | Validée |
| 5B | Toujours à mes côtés | Faire évoluer 1 Pokémon | 1 Super Bonbon et 5 Potions | Validée |
| 5C | Prendre soin des siens | Prendre soin de l’équipe ; souvenir d’une Potion | 8 Poudres de Blaze | Validée |
| 6 | Sur le chemin | Activer le PokéStop près de la gare abandonnée et vaincre 15 Pokémon | 2 500 Pokédollars | Validée |
| 7 | Peut-être des réponses | Parler à Maëlle | 1 000 Pokédollars | Validée |
| 8 | L’épreuve de Maëlle | Vaincre les 3 Dresseurs choisis par Maëlle | 5 000 Pokédollars | Validée |
| 9 | Souvenir | Retrouver un souvenir de stratégie | 5 Super Balls | Validée |
| 9A | Un nouveau départ | Lire le résumé du prologue | Aucune | Validée |

## Progression prévue après le prologue

```mermaid
flowchart LR
    P["Prologue<br/>Quêtes 1 à 9A"] --> C4["Q-10 à Q-11<br/>Premières explorations et cités abandonnées"]
    C4 --> C5["Q-12<br/>Le retour au village"]
    C5 --> C6["Q-13A ou Q-13B<br/>Ravitaillement et hôtel de ville"]
    C6 --> C7["Q-14A à Q-15B<br/>Choisir un champion allié"]
    C7 --> C8["Les oiseaux divins"]
```

## Chapitre 1 — Premières explorations
 # partie 1

```mermaid
flowchart LR
    Q9A["09A · Un nouveau départ<br/>Résumé du prologue · 🟢 Validée"] --> Q10["10 · Les pistes de Maëlle<br/>Fabriquer les boussoles et le sac à dos · 🟡 À valider"]
    Q10 --> Q11["11 · À la recherche de réponses<br/>Fouiller les coffres et trouver la photographie · 🟡 À valider"]
    Q11 --> Q12["12 · Le retour au village<br/>Un silence inquiétant · 🟡 À valider"]
    Q12 --> AUX1["AUX1 · Checkmark explicatif<br/>Camp ou bateau ?<br/>Le choix ne bloque pas la suite"]
    AUX1 --> Q13A["13A · Le camp de ravitaillement<br/>Installer le camp et récupérer le bloc de l’hôtel de ville · 🟡 À valider"]
    AUX1 --> Q13B["13B · Le bateau de ravitaillement<br/>Installer le bateau et récupérer le bloc de l’hôtel de ville · 🟡 À valider"]
    Q13A --> AUX2["AUX2 · Checkmark explicatif<br/>Arène Glace ou Électrik ?<br/>Le choix ne bloque pas la suite"]
    Q13B --> AUX2
    AUX2 --> Q14A["14A · Vers l’arène Glace<br/>Visiter le village de l’arène · 🟡 À valider"]
    AUX2 --> Q14B["14B · Vers l’arène Électrik<br/>Visiter le village de l’arène · 🟡 À valider"]
    Q14A --> Q15A["15A · Le champion Glace<br/>Vaincre le champion · 🟡 À valider"] --> A1["Quêtes d’Artikodin"]
    Q14B --> Q15B["15B · Le champion Électrik<br/>Vaincre le champion · 🟡 À valider"] --> AUX3["AUX3 · Checkmark explicatif<br/>Électhor ou Sulfura ?<br/>Le choix ne bloque pas la suite"]
    AUX3 --> B1["Quêtes d’Électhor"]
    AUX3 --> C1["Quêtes de Sulfura"]

    
    classDef complete fill:#315d3b,color:#ffffff,stroke:#8fce00,stroke-width:2px;
    classDef planned fill:#5a4a20,color:#ffffff,stroke:#e4c45a,stroke-width:2px;
    class Q9A complete;
    class Q10,Q11,Q12,Q13A,Q13B,Q14A,Q14B,Q15A,Q15B,A1,B1,C1 planned;
    classDef explanatory fill:#39445e,color:#ffffff,stroke:#9aaad0,stroke-dasharray:5 5;
    class AUX1,AUX2,AUX3 explanatory;
```

| N° | Quête | Objectif principal | Récompense | État |
|---:|---|---|---|---|
| 10 | Les pistes de Maëlle | Fabriquer une Explorer’s Compass, une Nature’s Compass et un sac à dos | 2 500 Pokédollars | À valider |
| 11 | À la recherche de réponses | Fouiller les coffres des cités abandonnées et obtenir une photographie de famille | 2 500 Pokédollars (proposition) | À valider |
| 12 | Le retour au village | Retourner au village de Garrick | Aucune | À valider |
| AUX1 | Checkmark explicatif — Camp ou bateau ? | Expliquer le choix entre le camp et le bateau. Ce choix ne bloque pas la suite de l’histoire. | Aucune | Explicatif |
| 13A | Le camp de ravitaillement | Installer le camp et récupérer le bloc de l’hôtel de ville dans son coffre | 5 000 Pokédollars ; débloque le choix d’une arène | À valider |
| 13B | Le bateau de ravitaillement | Installer le bateau et récupérer le bloc de l’hôtel de ville dans son coffre | 5 000 Pokédollars ; débloque le choix d’une arène | À valider |
| AUX2 | Checkmark explicatif — Arène Glace ou Électrik ? | Expliquer le choix entre les deux arènes. Ce choix ne bloque pas la suite de l’histoire. | Aucune | Explicatif |
| 14A | Vers l’arène Glace | Visiter le village de l’arène Glace | Accès au champion Glace | À valider |
| 14B | Vers l’arène Électrik | Visiter le village de l’arène Électrik | Accès au champion Électrik | À valider |
| AUX3 | Checkmark explicatif — Électhor ou Sulfura ? | Expliquer le choix entre les deux oiseaux. Ce choix ne bloque pas la suite de l’histoire. | Aucune | Explicatif |
| 15A | Le champion Glace | Vaincre le champion Glace | Débloque les quêtes d’Artikodin | À valider |
| 15B | Le champion Électrik | Vaincre le champion Électrik | Débloque le choix entre les quêtes d’Électhor et de Sulfura | À valider |

## Chapitre 1 — Premières explorations
 # Partie 2

```mermaid
flowchart LR
    A([Débloque les quêtes d’Artikodi])
    B([Débloque les quêtes de Sulfura et Électhor])
    A --> ART["Artikodin"]
    ART --> ICE["Trouver le Sanctuair glacé"]
    ICE --> ART1["Trouver la pierre de Glace"]
    ICE --> ART2["Battre 375 Pokémon"]
    ART1 --> ART3["Capturer Artikodin<br/>Je m’amuse"]
    ART2 --> ART3
    B -->SUL["Sulfura"]
    SUL --> FIRE["Trouver le Sanctuair ardent"]
    FIRE --> SUL1["Trouver la pierre de feu"]
    FIRE --> SUL2["Battre 375 Pokémon"]
    SUL1 --> SUL3["Capturer Sulfura"]
    SUL2 --> SUL3
    B --> THOR["Électhor"]
    THOR --> ELEC["Trouver le Sanctuair statique"]
    ELEC --> THOR1["Trouver la pierre de Foudre"]
    ELEC --> THOR2["Battre 375 Pokémon"]
    THOR1 --> THOR3["Capturer Électhor"]
    THOR2 --> THOR3
    ART3 --> F[Chapitre 2 — Tutoriels Pokémon]
    SUL3 --> F
    THOR3 --> F
```

Le chapitre 2 comprendra un groupe de tutoriels Pokémon à créer : stratégie, EV, IV et talents. Ce groupe s’ouvre après la fin de la quête de l’oiseau divin choisi.
