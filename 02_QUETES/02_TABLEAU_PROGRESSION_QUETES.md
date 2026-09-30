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
    C5 --> C6["Q-13A à Q-14<br/>Construire une nouvelle ville"]
    C6 --> C7["Q-15A à Q-16B<br/>Choisir un champion allié"]
    C7 --> C8["Les oiseaux divins"]
```

## Chapitre 1 — Premières explorations

```mermaid
flowchart LR
    Q9A["09A · Un nouveau départ<br/>Résumé du prologue · 🟢 Validée"] --> Q10["10 · Les pistes de Maëlle<br/>Fabriquer les boussoles et le sac à dos · 🟡 À valider"]
    Q10 --> Q11["11 · À la recherche de réponses<br/>Fouiller les coffres et trouver la photographie · 🟡 À valider"]
    Q11 --> Q12["12 · Le retour au village<br/>Un silence inquiétant · 🟡 À valider"]
    Q12 --> CHOIX_RAVITAILLEMENT{"Choisir le camp ou le bateau"}
    CHOIX_RAVITAILLEMENT --> Q13A["13A · Le camp de ravitaillement<br/>Construire le camp · 🟡 À valider"]
    CHOIX_RAVITAILLEMENT --> Q13B["13B · Le bateau de ravitaillement<br/>Construire le bateau · 🟡 À valider"]
    Q13A --> Q14["14 · L’hôtel de ville<br/>Récupérer le bloc dans le coffre · 🟡 À valider"]
    Q13B --> Q14
    Q14 --> CHOIX{"Choisir l’arène Glace ou Électrik"}
    CHOIX --> Q15A["15A · Vers l’arène Glace<br/>Visiter le village de l’arène · 🟡 À valider"]
    CHOIX --> Q15B["15B · Vers l’arène Électrik<br/>Visiter le village de l’arène · 🟡 À valider"]
    Q15A --> Q16A["16A · Le champion Glace<br/>Vaincre le champion · 🟡 À valider"] --> A1["Quêtes d’Artikodin"]
    Q15B --> Q16B["16B · Le champion Électrik<br/>Vaincre le champion · 🟡 À valider"] --> CHOIX_ELEC{"Choisir Électhor ou Sulfura"}
    CHOIX_ELEC --> B1["Quêtes d’Électhor"]
    CHOIX_ELEC --> C1["Quêtes de Sulfurar"]

    
    classDef complete fill:#315d3b,color:#ffffff,stroke:#8fce00,stroke-width:2px;
    classDef planned fill:#5a4a20,color:#ffffff,stroke:#e4c45a,stroke-width:2px;
    class Q9A complete;
    class Q10,Q11,Q12,CHOIX_RAVITAILLEMENT,Q13A,Q13B,Q14,CHOIX,Q15A,Q15B,Q16A,Q16B,CHOIX_ELEC,A1,B1,C1 planned;
```

| N° | Quête | Objectif principal | Récompense | État |
|---:|---|---|---|---|
| 10 | Les pistes de Maëlle | Fabriquer une Explorer’s Compass, une Nature’s Compass et un sac à dos | 2 500 Pokédollars | À valider |
| 11 | À la recherche de réponses | Fouiller les coffres des cités abandonnées et obtenir une photographie de famille | 2 500 Pokédollars (proposition) | À valider |
| 12 | Le retour au village | Retourner au village de Garrick | Aucune | À valider |
| 13A | Le camp de ravitaillement | Construire le camp de ravitaillement | Débloque l’hôtel de ville | À valider |
| 13B | Le bateau de ravitaillement | Construire le bateau de ravitaillement | Débloque l’hôtel de ville | À valider |
| 14 | L’hôtel de ville | Récupérer le bloc de l’hôtel de ville dans le coffre de ravitaillement | Débloque le choix d’une arène | À valider |
| 15A | Vers l’arène Glace | Visiter le village de l’arène Glace | Accès au champion Glace | À valider |
| 15B | Vers l’arène Électrik | Visiter le village de l’arène Électrik | Accès au champion Électrik | À valider |
| 16A | Le champion Glace | Vaincre le champion Glace | Débloque les quêtes d’Artikodin | À valider |
| 16B | Le champion Électrik | Vaincre le champion Électrik | Débloque le choix entre les quêtes d’Électhor et de Sulfura | À valider |
