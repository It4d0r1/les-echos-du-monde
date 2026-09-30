# Fabriquer les plaques d’Arceus

Statut : 18 recettes ajoutées au datapack — test en jeu à faire

## Principe

Chaque recette utilise quatre feuilles de laiton (`create:brass_sheet`) aux coins de la grille. Les cinq autres cases contiennent chacune un tesson. Les proportions ont été choisies en comparant les couleurs moyennes des icônes des Plaques et des six tessons Pixelmon de base. C’est un rapprochement visuel ; Pixelmon ne mélange pas réellement les couleurs des objets.

## Grilles 3 × 3

Chaque case représente une unité. « Laiton » désigne une feuille de laiton Create.

### Plaque Draco (`pixelmon:draco_plate`)

| Laiton | Bleu | Laiton |
|---|---|---|
| Rouge | Bleu | Rouge |
| Laiton | Bleu | Laiton |

### Plaque Dread (`pixelmon:dread_plate`)

| Laiton | Bleu | Laiton |
|---|---|---|
| Noir | Blanc | Noir |
| Laiton | Bleu | Laiton |

### Plaque Terre (`pixelmon:earth_plate`)

| Laiton | Rouge | Laiton |
|---|---|---|
| Jaune | Rouge | Rouge |
| Laiton | Rouge | Laiton |

### Plaque Poing (`pixelmon:fist_plate`)

| Laiton | Rouge | Laiton |
|---|---|---|
| Jaune | Rouge | Jaune |
| Laiton | Rouge | Laiton |

### Plaque Flamme (`pixelmon:flame_plate`)

| Laiton | Rouge | Laiton |
|---|---|---|
| Rouge | Rouge | Rouge |
| Laiton | Rouge | Laiton |

### Plaque Glaçon (`pixelmon:icicle_plate`)

| Laiton | Bleu | Laiton |
|---|---|---|
| Vert | Blanc | Bleu |
| Laiton | Bleu | Laiton |

### Plaque Insecte (`pixelmon:insect_plate`)

| Laiton | Vert | Laiton |
|---|---|---|
| Jaune | Vert | Jaune |
| Laiton | Vert | Laiton |

### Plaque Fer (`pixelmon:iron_plate`)

| Laiton | Blanc | Laiton |
|---|---|---|
| Noir | Blanc | Noir |
| Laiton | Blanc | Laiton |

### Plaque Légende (`pixelmon:legend_plate`)

| Laiton | Blanc | Laiton |
|---|---|---|
| Blanc | Noir | Blanc |
| Laiton | Blanc | Laiton |

### Plaque Prairie (`pixelmon:meadow_plate`)

| Laiton | Vert | Laiton |
|---|---|---|
| Jaune | Vert | Vert |
| Laiton | Vert | Laiton |

### Plaque Esprit (`pixelmon:mind_plate`)

| Laiton | Rouge | Laiton |
|---|---|---|
| Bleu | Bleu | Bleu |
| Laiton | Bleu | Laiton |

### Plaque Pixie (`pixelmon:pixie_plate`)

| Laiton | Rouge | Laiton |
|---|---|---|
| Bleu | Rouge | Rouge |
| Laiton | Rouge | Laiton |

### Plaque Ciel (`pixelmon:sky_plate`)

| Laiton | Bleu | Laiton |
|---|---|---|
| Vert | Bleu | Bleu |
| Laiton | Bleu | Laiton |

### Plaque Splash (`pixelmon:splash_plate`)

| Laiton | Bleu | Laiton |
|---|---|---|
| Bleu | Bleu | Bleu |
| Laiton | Bleu | Laiton |

### Plaque Fantôme (`pixelmon:spooky_plate`)

| Laiton | Bleu | Laiton |
|---|---|---|
| Rouge | Bleu | Bleu |
| Laiton | Bleu | Laiton |

### Plaque Pierre (`pixelmon:stone_plate`)

| Laiton | Rouge | Laiton |
|---|---|---|
| Jaune | Jaune | Rouge |
| Laiton | Jaune | Laiton |

### Plaque Toxique (`pixelmon:toxic_plate`)

| Laiton | Bleu | Laiton |
|---|---|---|
| Bleu | Rouge | Bleu |
| Laiton | Bleu | Laiton |

### Plaque Zap (`pixelmon:zap_plate`)

| Laiton | Jaune | Laiton |
|---|---|---|
| Rouge | Jaune | Jaune |
| Laiton | Rouge | Laiton |

## Vérifications faites

- Pixelmon 1.21.1-9.4.1, Create et Global Packs sont installés dans l’instance.
- Les couleurs ont été relevées directement dans les textures des 18 Plaques et des tessons rouge, bleu, vert, noir, blanc et jaune.
- Les 18 recettes façonnées sont dans `global_packs/required_data/les_echos_du_monde/data/les_echos_du_monde/recipe/arceus_plates/`.
- Les fichiers JSON sont lisibles et chaque grille est distincte ; les recettes n’ont pas encore été vérifiées en jeu.

## À tester avant validation

- Charger un monde, vérifier que les 18 recettes apparaissent dans JEI et essayer les recettes.
- Vérifier comment obtenir chaque type de tesson dans cette partie et ajuster l’équilibrage si nécessaire.
- Définir si une Plaque suffit pour protéger une personne et si elle est consommée ou conservée après le passage d’une Ultra-Brèche.
- Décider si la Plaque Légende doit être craftable ou réservée à une obtention narrative.

## Liens

- Lore : section « Ultra-Brèches, Arceus et Plaques » dans `01_LORE_DETAILLE_MIGRE.txt`.
- Légendaires : entrée Arceus dans `02_QUETES/04_LEGENDAIRES_ET_QUETES.md`.
- Recettes : `global_packs/required_data/les_echos_du_monde/data/les_echos_du_monde/recipe/arceus_plates/` dans l’instance Minecraft.

## Usage envisagée : invoquer les trois bêtes légendaires

Les Plaques d’Arceus pourraient servir d’objets d’invocation pour Entei, Raikou et Suicune. Correspondance proposée d’après leurs types :

- Entei : Plaque Flamme (`pixelmon:flame_plate`).
- Raikou : Plaque Zap (`pixelmon:zap_plate`).
- Suicune : Plaque Splash (`pixelmon:splash_plate`).

La plaque sert de clé pour invoquer le Pokémon et reste intacte.

