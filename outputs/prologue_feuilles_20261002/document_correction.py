"""Document the leaf correction without replacing existing instruction sections."""
from pathlib import Path
import json
import shutil

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parents[1]
WORK=PROJECT/'outputs/prologue_plateforme17'
PACK=WORK/'datapack'

TEXT='''## Correctif du 2 octobre 2026 — feuilles flottantes

La feuille de chêne visée sur la capture à **(-20, -1, 6)** existe déjà dans le NBT original. Elle appartient à un fragment de neuf feuilles sans tronc ni support voisin. La préparation et le découpage avaient conservé ce fragment. En jeu, sa distance aux troncs a été recalculée de 1 à 7.

La copie préparée et ses segments retirent désormais **109 feuilles de chêne**, réparties en **14 fragments isolés** : aucune connexion à un tronc, au sol ou au décor proche. Les feuilles des arbres et des buissons soutenus sont conservées. Les fragments de cerisier proches des canopées et les feuilles d’azalée n’ont pas été modifiés par ce correctif.

### Monde déjà créé

Au prochain démarrage du monde utilisant `segments_v17`, les fonctions `world/leaves_v17` nettoient automatiquement les **positions exactes** de ces fragments, lorsque leur chunk déjà généré est chargé. Aucune commande joueur nécessaire. La réparation est enregistrée par chunk et ne remplace pas les segments terminés. Les constructions restent en place. Les autres types de blocs aux positions recensées sont conservés.

Parmi les fragments d’origine, **103 feuilles sont non persistantes** et **6 sont persistantes**. Le nettoyage vérifie ce caractère à chaque position ; pour les six persistantes, il exige aussi `distance=7` et `waterlogged=false`. Une feuille de chêne ajoutée depuis avec exactement ces mêmes propriétés et au même emplacement serait également retirée lors du premier passage du correctif.

La réparation respecte la pause du prologue. Si la génération est volontairement en pause, utiliser la reprise habituelle lorsque le nettoyage est souhaité.

### Vérification au retour

1. Redémarrer complètement Minecraft, puis ouvrir le monde actuel **1**.
2. Revenir près de **(-20, -1, 6)** : le fragment de la capture doit avoir disparu.
3. Parcourir la zone pour charger les autres chunks concernés ; vérifier que les arbres complets et les buissons posés au sol restent présents.
4. Vérifier qu’une construction ou un bloc modifié dans un segment terminé reste intact ; se reconnecter et vérifier à nouveau.
5. Facultatif : créer un nouveau monde de test et vérifier l’absence de ces mêmes fragments.

Contrôles hors jeu : source originale inchangée ; comparaison de la copie avant/après limitée aux **109 états de feuilles remplacés par de l’air** ; toutes les autres entrées, les plantes ajoutées et les données NBT conservées. Le nettoyage utilise uniquement les coordonnées enregistrées, ajoute zéro chargement forcé et ne remet aucun score de génération à zéro.

Les journaux et la sauvegarde du monde 1 confirment le chargement du datapack, l’arrivée dans le prologue et **127 segments terminés** avant ce correctif. **Le nettoyage correctif n’a pas encore été observé dans Minecraft.**
'''

def append_once(path,text):
    previous=path.read_text(encoding='utf-8')
    marker='## Correctif du 2 octobre 2026 — feuilles flottantes'
    if marker in previous: previous=previous.split(marker)[0].rstrip()+'\n'
    path.write_text(previous.rstrip()+'\n\n'+text,encoding='utf-8')

def main():
    append_once(WORK/'TESTS_ET_UTILISATION.md',TEXT)
    shutil.copy2(WORK/'TESTS_ET_UTILISATION.md',PACK/'TESTS.md')
    append_once(PACK/'README.md',TEXT)
    append_once(PROJECT/'Consignes_creation_zone_depart.md',TEXT)
    backup=(ROOT/'backup_path.txt').read_text(encoding='utf-8-sig').strip()
    (ROOT/'CORRECTIF_FEUILLES.md').write_text('# Feuilles flottantes — diagnostic et correction\n\n'+TEXT+f'\nSauvegarde du datapack avant correctif : `{backup}`.\n\nRapports : `diagnostic_feuilles.json`, `verification_correctif.json`, `rapport_correctif.json`.\n',encoding='utf-8')
    shutil.copy2(ROOT/'CORRECTIF_FEUILLES.md',PACK/'CORRECTIF_FEUILLES.md')
    print('Leaf correction documentation updated.')

if __name__=='__main__': main()
