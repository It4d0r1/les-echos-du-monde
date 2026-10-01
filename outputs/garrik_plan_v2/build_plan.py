from pathlib import Path
from collections import Counter
import json, csv, math
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A3, landscape

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '06_RESSOURCES' / 'Images' / 'Maison garrike' / 'Plan exterieur coherent v2'
OUT.mkdir(parents=True, exist_ok=True)
QA = Path(__file__).parent / 'qa'
QA.mkdir(exist_ok=True)
FONTROOT = Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('Plan', str(FONTROOT / 'arial.ttf')))
pdfmetrics.registerFont(TTFont('PlanBold', str(FONTROOT / 'arialbd.ttf')))

M = {
 'S': ('Pierre de fondation', '#aaa9a2'),
 'B': ('Poutres en bois', '#704a31'),
 'P': ('Planches en bois', '#b88a53'),
 'E': ('Enduit clair', '#ece4cf'),
 'G': ('Vitres', '#88bccb'),
 'D': ('Portes : partie basse / haute', '#99673e'),
 'R': ('Escaliers de toiture', '#a06e3e'),
 'H': ('Bois plein : faîtage', '#c19352'),
 'C': ('Pierre des cheminées', '#767b7b'),
 'L': ('Lanternes', '#e5b84c'),
 'V': ('Feuillage et jardinières', '#73874b'),
 'N': ('Bannières décoratives', '#414765'),
 'A': ('Escaliers du perron', '#969894'),
}
model = {}
orient = {}
def put(x,y,z,m,up=None):
    model[(x,y,z)] = m
    if up: orient[(x,y,z)] = up
    else: orient.pop((x,y,z),None)

# Single exterior shell: X left to right from the entrance, Z entrance to rear.
# Height values are voxel base levels. A block at Y=18 ends at height 19.
for x in range(25):
 for z in range(17):
  if x in (0,24) or z in (0,16):
   for y in range(10):
    mat = 'S' if y <= 4 else 'P'
    if y == 5 or y == 9: mat = 'B'
    if y >= 5 and ((z in (0,16) and x in (0,5,9,14,16,20,24)) or (x in (0,24) and z in (0,4,8,12,16))): mat='B'
    put(x,y,z,mat)

def window(face,a,b,lo,hi):
 def coord(u,y):
  return {'front': (u,y,0), 'rear': (u,y,16), 'left': (0,y,u), 'right': (24,y,u)}[face]
 for u in range(a,b+1):
  for y in range(lo,hi+1): put(*coord(u,y),'G')
 for u in (a-1,b+1):
  for y in range(lo,hi+1): put(*coord(u,y),'B')
 for u in range(a,b+1):
  put(*coord(u,lo-1),'S' if lo==1 else 'B')
  put(*coord(u,hi+1),'B')

for a,b in [(2,4),(10,12),(17,19),(21,23)]: window('front',a,b,1,3)
for a,b in [(2,4),(6,8),(10,12),(17,19),(21,23)]: window('front',a,b,6,8)
for a,b in [(3,5),(11,13),(19,21)]:
 window('rear',a,b,1,3); window('rear',a,b,6,8)
for face in ('left','right'):
 for a,b in [(2,4),(7,9),(12,14)]:
  window(face,a,b,1,3); window(face,a,b,6,8)
for x in (6,7):
 for y in (1,2): put(x,y,0,'D')
 put(x,3,0,'G')
for y in (1,2,3):
 for x in (5,8): put(x,y,0,'B')
for x in range(5,9): put(x,4,0,'B')

def main_roof(z): return 16-math.ceil(abs(z-8)*.75)
def cross_roof(x,z=0): return 18-abs(x-7)-max(0,z-4)
def roof_height(x,z):
 a=main_roof(z)
 b=cross_roof(x,z) if -1<=x<=15 and -1<=z<=8 else -100
 return max(a,b)

# Side gables and the tall entrance gable, with no internal floors or rooms.
for x in (0,24):
 for z in range(17):
  for y in range(10,roof_height(x,z)):
   mat='B' if z==8 or y==roof_height(x,z)-1 else 'E'
   put(x,y,z,mat)
for x in range(15):
 for y in range(10,roof_height(x,0)):
  put(x,y,0,'B' if x in (0,7,14) or y==roof_height(x,0)-1 else 'E')
window('front',6,8,12,15)
window('left',7,9,12,15)
window('right',7,9,12,15)

# Boolean union of two pitched roofs. Junctions share the same height function.
for x in range(-1,26):
 for z in range(-1,18):
  h=roof_height(x,z)
  cross=(-1<=x<=15 and -1<=z<=8 and cross_roof(x,z)>main_roof(z))
  if cross:
   ridge=x==7; up='X+' if x<7 else 'X-'
  else:
   ridge=z==8; up='Z+' if z<8 else 'Z-'
  put(x,h,z,'H' if ridge else 'R', None if ridge else up)

# Front dormer: X=19..21, face Z=1. Rear dormer: X=11..13, face Z=15.
def dormer(center,face_z,inward):
 for x in range(center-2,center+3):
  top=15-abs(x-center)
  for depth in range(5):
   z=face_z+inward*depth
   h0=main_roof(z)
   if top <= h0: continue
   if depth==0 or x in (center-2,center+2):
    for y in range(h0,top): put(x,y,z,'B' if x in (center-2,center+2) or y==11 else 'P')
   put(x,top,z,'H' if x==center else 'R', None if x==center else ('X+' if x<center else 'X-'))
 for x in range(center-1,center+2):
  for y in (12,13): put(x,y,face_z,'G')
  put(x,14,face_z,'B')
dormer(20,1,1)
dormer(12,15,-1)

# Two immutable 2x2 chimney footprints, both ending at height 23.
for xa in (2,21):
 for x in (xa,xa+1):
  for z in (11,12):
   for y in range(13,23): put(x,y,z,'C')

# Small entrance canopy and three-cell-deep approach, outside the wall footprint.
for x in range(4,11):
 for z in range(-3,0):
  h=6-abs(x-7)
  put(x,h,z,'H' if x==7 else 'R', None if x==7 else ('X+' if x<7 else 'X-'))
for x in (4,10):
 for y in range(3): put(x,y,-2,'B')
for x in range(5,9):
 put(x,-1,-4,'A','Z+')
 put(x,0,-3,'A','Z+')
 put(x,0,-2,'S')
 put(x,0,-1,'S')

# Decoration is located once, so it also agrees across every projection.
for a,b in [(2,4),(10,12),(17,19),(21,23)]:
 for x in range(a,b+1): put(x,5,-1,'V')
for x in (13,14):
 for y in range(1,9): put(x,y,-1,'V')
for y in range(2,9): put(7,y,17,'V')
for y in range(1,9): put(-1,y,5,'V')
for y in range(2,6): put(25,y,11,'V')
for z in (5,11):
 for y in range(7,10): put(25,y,z,'N')
for x in (1,15,24): put(x,7,-1,'L')
for x in (1,23): put(x,7,17,'L')
for z in (1,15):
 put(-1,7,z,'L'); put(25,7,z,'L')

assert all(-1<=x<=25 and -4<=z<=17 and -1<=y<=22 for x,y,z in model)
assert { (x,z) for x,y,z in model if y==22 } == {(x,z) for x in (2,3,21,22) for z in (11,12)}
assert max(y for (x,y,z),m in model.items() if m in ('R','H')) == 18
assert all(model[(x,22,z)]=='C' for x in (2,3,21,22) for z in (11,12))
assert len(model)==len(set(model))
counts=Counter(model.values())

with (OUT/'Modele_exterieur_v2.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.writer(f,delimiter=';'); writer.writerow(['X','Y','Z','Code','Materiau','Montee_escalier'])
 for (x,y,z),m in sorted(model.items(),key=lambda a:(a[0][1],a[0][2],a[0][0])):
  writer.writerow([x,y,z,m,M[m][0],orient.get((x,y,z),'')])
(OUT/'Verification_v2.json').write_text(json.dumps({'wall_footprint':[25,17], 'roof_envelope':[27,19], 'wall_height':10,'roof_height':19,'chimney_height':23,'chimneys':[[2,3,11,12],[21,22,11,12]],'unique_cells':len(model),'counts':dict(counts),'checks':'Toutes les vues et couches proviennent du même dictionnaire de blocs. Dimensions vérifiées sur les coordonnées, pas sur la photographie.'},ensure_ascii=False,indent=2),encoding='utf-8')

def iso_image():
 polygons=[]
 # Face subdivision models stairs as half-block steps; full opaque glazing keeps exterior only.
 def parts(x,y,z,m):
  up=orient.get((x,y,z))
  if m not in ('R','A'): return [(x,y,z,1,1,1)]
  p=[(x,y,z,1,.5,1)]
  if up=='X+': p.append((x+.5,y+.5,z,.5,.5,1))
  elif up=='X-': p.append((x,y+.5,z,.5,.5,1))
  elif up=='Z+': p.append((x,y+.5,z+.5,1,.5,.5))
  else: p.append((x,y+.5,z,1,.5,.5))
  return p
 def project(x,y,z): return ((x-z)*20, -(x+z)*9-y*22)
 for (x,y,z),m in model.items():
  for xx,yy,zz,dx,dy,dz in parts(x,y,z,m):
   verts=[(xx,yy,zz),(xx+dx,yy,zz),(xx+dx,yy,zz+dz),(xx,yy,zz+dz),(xx,yy+dy,zz),(xx+dx,yy+dy,zz),(xx+dx,yy+dy,zz+dz),(xx,yy+dy,zz+dz)]
   color=tuple(int(M[m][1][i:i+2],16) for i in (1,3,5))
   for indexes,shade in [([0,1,5,4],.78),([0,3,7,4],.92),([4,5,6,7],1.12)]:
    poly=[project(*verts[i]) for i in indexes]
    depth=sum(-verts[i][0]-verts[i][2]+(18/22)*verts[i][1] for i in indexes)/4
    rgb=tuple(min(255,int(a*shade)) for a in color)
    polygons.append((depth,poly,rgb))
 xs=[p[0] for _,poly,_ in polygons for p in poly]; ys=[p[1] for _,poly,_ in polygons for p in poly]
 xmin,ymin=min(xs)-30,min(ys)-30
 im=Image.new('RGB',(int(max(xs)-xmin+30),int(max(ys)-ymin+30)), '#faf8f2')
 d=ImageDraw.Draw(im)
 for depth,poly,col in sorted(polygons,key=lambda a:a[0]):
  pts=[(a-xmin,b-ymin) for a,b in poly]
  d.polygon(pts,fill=col,outline=tuple(int(a*.6) for a in col))
 im.save(QA/'axonometric.png')
 return im
iso=iso_image()

W,H=landscape(A3)
PDF=OUT/'Maison_de_Garrik_Plan_exterieur_coherent_v2.pdf'
c=canvas.Canvas(str(PDF),pagesize=(W,H))
c.setTitle('Maison de Garrik - plan extérieur cohérent v2')
c.setAuthor('Les Échos du Monde')
INK=HexColor('#26323b'); MUTED=HexColor('#59666e'); LINE=HexColor('#d4d6d1'); BG=HexColor('#faf8f2'); ACC=HexColor('#8c613f')
def txt(x,y,s,size=10,bold=False,color=INK):
 c.setFillColor(color); c.setFont('PlanBold' if bold else 'Plan',size); c.drawString(x,y,s)
def centered(x,y,s,size=10,bold=False):
 c.setFillColor(INK); c.setFont('PlanBold' if bold else 'Plan',size); c.drawCentredString(x,y,s)
def line(x1,y1,x2,y2,color=LINE,width=.5):
 c.setStrokeColor(color); c.setLineWidth(width); c.line(x1,y1,x2,y2)
def page(n,subtitle):
 c.setFillColor(BG); c.rect(0,0,W,H,fill=1,stroke=0)
 txt(35,H-42,'MAISON DE GARRIK',25,True)
 txt(35,H-65,subtitle,13,True,ACC)
 txt(35,H-84,'Reconstruction proposée depuis une image - géométrie commune vérifiée - extérieur uniquement',10,color=MUTED)
 line(35,H-99,W-35,H-99)
 line(35,48,W-35,48)
 txt(35,31,'1 case = 1 bloc. X : gauche > droite ; Z : entrée > arrière ; Y : niveau du bloc.',9,color=MUTED)
 txt(W-140,31,f'VERSION 2  /  {n} sur 5',9,True)
def end(): c.showPage()
def arrow(x1,y1,x2,y2,label,vertical=False):
 line(x1,y1,x2,y2,INK,.7)
 a=math.atan2(y2-y1,x2-x1)
 for x,y,ang in [(x1,y1,a),(x2,y2,a+math.pi)]:
  pts=[(x,y),(x+5*math.cos(ang+.36),y+5*math.sin(ang+.36)),(x+5*math.cos(ang-.36),y+5*math.sin(ang-.36))]
  c.setFillColor(INK); p=c.beginPath(); p.moveTo(*pts[0]); p.lineTo(*pts[1]); p.lineTo(*pts[2]); p.close(); c.drawPath(p,fill=1,stroke=0)
 if vertical:
  c.saveState(); c.translate(x1-5,(y1+y2)/2); c.rotate(90); centered(0,0,label,9,True); c.restoreState()
 else: centered((x1+x2)/2,y1-15,label,10,True)
def legend(x,y,compact=False):
 size=8 if compact else 10; step=90 if compact else 125
 items=[('S','Pierre'),('B','Poutres'),('P','Planches'),('E','Enduit'),('G','Vitres'),('R','Toiture'),('C','Cheminées'),('V','Végétation')]
 for i,(m,label) in enumerate(items):
  xx=x+(i%4)*step; yy=y-(i//4)*18
  c.setFillColor(HexColor(M[m][1])); c.rect(xx,yy-1,9,9,fill=1,stroke=0); txt(xx+14,yy,label,size)

def project_view(face):
 p={}
 for (x,y,z),m in model.items():
  if face=='front': u,depth=x,z
  elif face=='rear': u,depth=24-x,-z
  elif face=='left': u,depth=16-z,x
  else: u,depth=z,-x
  if (u,y) not in p or depth<p[(u,y)][0]: p[(u,y)]=(depth,m,(x,y,z))
 return p

def elevation(face,x,y,title):
 s=10.3; umax=24 if face in ('front','rear') else 16
 # Shared grid range: 0..23 in height. The drawing origin is the wall datum Y=0.
 ox=x+140; oy=y+36
 txt(x+12,y+305,title,13,True)
 c.setStrokeColor(LINE); c.setLineWidth(.28)
 for u in range(-5,umax+5): c.line(ox+u*s,oy-s,ox+u*s,oy+23*s)
 for v in range(-1,24): c.line(ox-5*s,oy+v*s,ox+(umax+4)*s,oy+v*s)
 for (u,v),(_,m,coord) in project_view(face).items():
  c.setFillColor(HexColor(M[m][1])); c.setStrokeColor(Color(.20,.20,.16,alpha=.42)); c.setLineWidth(.25)
  c.rect(ox+u*s,oy+v*s,s,s,fill=1,stroke=1)
  if m=='G':
   line(ox+(u+.18)*s,oy+(v+.18)*s,ox+(u+.82)*s,oy+(v+.82)*s,HexColor('#deeff0'),.65)
  if m=='L':
   c.setFillColor(HexColor('#fff2a1')); c.rect(ox+(u+.2)*s,oy+(v+.2)*s,.6*s,.6*s,fill=1,stroke=0)
 line(ox-5*s,oy,ox+(umax+4)*s,oy,INK,1)
 for height in (10,19,23):
  c.setDash(2,2); line(ox-4.9*s,oy+height*s,ox+(umax+3)*s,oy+height*s,MUTED,.4); c.setDash()
  txt(ox+(umax+3)*s+4,oy+height*s-3,str(height),8)
 arrow(ox,oy-18,ox+(umax+1)*s,oy-18,f'Murs : {umax+1} blocs')
 arrow(ox-5.8*s,oy,ox-5.8*s,oy+23*s,'Cheminées : 23',True)
 arrow(ox-3.8*s,oy,ox-3.8*s,oy+19*s,'Toit : 19',True)
 txt(x+12,y+7,{'front':'Vue depuis Z négatif. X croît vers la droite.','rear':'Vue depuis Z positif. X croît vers la gauche.','left':'Vue depuis X négatif. Z croît vers la gauche.','right':'Vue depuis X positif. Z croît vers la droite.'}[face],9,color=MUTED)
 c.setStrokeColor(LINE); c.setLineWidth(.6); c.roundRect(x,y,548,325,5,fill=0,stroke=1)

page(1,'FAÇADES COTÉES - même échelle et même modèle')
elevation('front',35,414,'FAÇADE PRINCIPALE')
elevation('rear',607,414,'FAÇADE ARRIÈRE')
elevation('left',35,75,'CÔTÉ GAUCHE')
elevation('right',607,75,'CÔTÉ DROIT')
txt(35,57,'Cotes depuis le bas du socle (Y=0) : murs 10 ; haut du toit 19 ; haut des cheminées 23. Le jardin est hors cote.',9,color=MUTED)
end()

def cellplan(x,y,s,layer=None,labels=True,upstairs=False):
 # Fixed frame used on every layer, including the entrance stair at Z=-4.
 xmin,xmax,zmin,zmax=-1,25,-4,17
 for xx in range(xmin,xmax+1):
  for zz in range(zmin,zmax+1):
   candidates=[(yy,m) for (a,yy,b),m in model.items() if a==xx and b==zz and (layer is None or yy==layer)]
   topcell=max(candidates,key=lambda a:a[0]) if candidates else None
   m=topcell[1] if topcell else None
   py=y+(zz-zmin)*s; px=x+(xx-xmin)*s
   c.setFillColor(HexColor(M[m][1]) if m else BG); c.setStrokeColor(LINE); c.setLineWidth(.22)
   c.rect(px,py,s,s,fill=1,stroke=1)
   if topcell and layer is None and m in ('R','H','C'):
    c.setFillColor(HexColor('#fff7e6') if m in ('R','C') else INK)
    c.setFont('Plan',max(4,s*.37)); c.drawCentredString(px+s/2,py+s*.31,str(topcell[0]))
   if m and layer is not None:
    if m in ('R','A'):
     up=orient.get((xx,layer,zz),'Z+')
     # Arrow indicates direction of the higher half of the stair, not compass north.
     cx,cy=px+s/2,py+s/2; d=s*.25
     dx,dz={'X+':(1,0),'X-':(-1,0),'Z+':(0,1),'Z-':(0,-1)}[up]
     ux,uy=dx*d,dz*d
     line(cx-ux,cy-uy,cx+ux,cy+uy,HexColor('#f9eacb'),.55)
     a=math.atan2(uy,ux); ex,ey=cx+ux,cy+uy
     for aa in (a+2.5,a-2.5): line(ex,ey,ex+2*math.cos(aa),ey+2*math.sin(aa),HexColor('#f9eacb'),.55)
    elif m in ('D','L','N','H'):
     centered(px+s/2,py+s*.24,m,max(4,s*.52),True)
 if labels:
  for xx in (-1,0,5,10,15,20,24,25): centered(x+(xx-xmin+.5)*s,y+22*s+5,str(xx),6)
  for zz in (-4,0,4,8,12,16,17): txt(x-18,y+(zz-zmin+.3)*s,str(zz),6)
  txt(x+27*s+4,y+21*s,'X',7,True); txt(x-18,y-12,'Z',7,True)
 # Wall line follows exact outside block boundaries, excluding roof and decoration.
 c.setDash(2,2); c.setStrokeColor(INK); c.setLineWidth(.65)
 c.rect(x+s,y+4*s,25*s,17*s,fill=0,stroke=1); c.setDash()

page(2,'TOIT ET VOLUME - positions communes à toutes les vues')
txt(45,706,'VOLUME EXTÉRIEUR',14,True)
c.drawImage(ImageReader(iso),45,222,width=535,height=464,preserveAspectRatio=True,anchor='c',mask='auto')
txt(45,204,'Schéma volumétrique du même assemblage ; aucun intérieur ajouté.',10,color=MUTED)
legend(45,172)
txt(650,706,'VUE DU DESSUS - entrée en bas',14,True)
sx,sy,sz=665,293,15.8
cellplan(sx,sy,sz)
arrow(sx,sy+22*sz+34,sx+27*sz,sy+22*sz+34,'Toiture : 27 blocs')
arrow(sx+27*sz+35,sy+3*sz,sx+27*sz+35,sy+22*sz,'Toiture : 19',True)
txt(677,275,'Chiffres dans la toiture : niveau Y de la cellule supérieure.',9,color=MUTED)
txt(650,258,'Pointillés : murs 25 × 17. Débord : 1 bloc sur les quatre côtés.',10)
txt(650,241,'Porche : X=4..10, Z=-3..-1. Perron : X=5..8, Z=-4..-1.',10)
txt(650,221,'REPÈRES DE CONSTRUCTION',12,True)
for j,s in enumerate([
 'Faîtage principal : Z=8, sur toute la largeur.',
 'Grand pignon avant : X=7 ; raccord progressif au toit.',
 'Lucarne avant : axe X=20, face Z=1.',
 'Lucarne arrière : axe X=12, face Z=15.',
 'Cheminée C1 : X=2..3 ; Z=11..12.',
 'Cheminée C2 : X=21..22 ; Z=11..12.',
 'Deux cheminées : sommet à 23 blocs, soit les cellules Y=22.',
]): txt(650,201-j*17,s,10)
txt(45,102,'FIDÉLITÉ À LA RÉFÉRENCE',12,True)
txt(45,83,'Conservés : pignon avant à gauche, lucarne avant à droite, socle en pierre, colombages, entrée couverte, deux cheminées.',10)
txt(45,65,'Choisis pour rendre la construction cohérente : dimensions, coordonnées exactes, pente du toit et raccords. Le jardin reste libre.',10,color=MUTED)
end()

for pg,start in [(3,-1),(4,7),(5,15)]:
 page(pg,f'COUCHES DE CONSTRUCTION - cellules Y={start} à {start+7}')
 txt(35,716,'Vue du dessus, entrée en bas. Placer seulement les cases colorées. Les cases vides restent libres.',10)
 txt(35,698,'Le pointillé suit les murs. Les flèches indiquent le côté haut des escaliers. Chaque couche utilise les mêmes coordonnées.',10,color=MUTED)
 for k in range(8):
  row,col=divmod(k,4); lev=start+k
  px=35+col*284; py=389-row*281
  c.setStrokeColor(LINE); c.setLineWidth(.6); c.roundRect(px,py,267,264,5,fill=0,stroke=1)
  txt(px+12,py+244,f'Y = {lev}',13,True)
  count=sum(1 for x,y,z in model if y==lev)
  txt(px+91,py+245,f'{count} cellules à placer',9,color=MUTED)
  cellplan(px+31,py+57,7.5,layer=lev)
  txt(px+12,py+23,('Terrain / premier escalier' if lev==-1 else ('Socle, murs et détails' if lev<10 else ('Pignons, toit et cheminées' if lev<19 else 'Cheminées uniquement'))),9)
  if lev==22: txt(px+12,py+9,'Sommet = 23 blocs depuis Y=0.',8,color=MUTED)
 legend(35,90,True)
 # Additional symbol key, same on all layer pages.
 txt(470,90,'H : faîtage en bois plein    D : éléments des portes    L : lanternes',9)
 txt(470,72,'N : bannières    Gris du perron : escaliers / pierre    V : végétation à ajuster',9)
 end()
c.save()

notes='''# Maison de Garrik - plan extérieur cohérent v2

Statut : reconstruction proposée à partir de l’image fournie. Les coordonnées sont celles d’un modèle unique, pas des mesures extraites de la photographie. Aucune vérification en jeu n’a été effectuée.

## Comment lire le plan

- Une case représente une cellule de bloc, pas un pixel décoratif.
- X augmente de gauche à droite lorsqu’on regarde la façade principale ; Z augmente de l’entrée vers l’arrière ; Y augmente vers le haut.
- Les murs occupent X=0..24 et Z=0..16 : 25 × 17 blocs. Leur sommet rectangulaire est à la hauteur 10.
- Le toit principal et le grand pignon occupent X=-1..25 et Z=-1..17 : enveloppe de 27 × 19 blocs, avec un débord d’un bloc.
- Le bloc le plus haut du faîtage est placé en Y=18 : son sommet est à la hauteur 19. Les cheminées se terminent en Y=22 : sommet à 23.
- La première marche est en Y=-1, sous le niveau de référence du socle. Préparer le terrain en conséquence.
- Les façades sont des projections du même modèle. Sur la façade arrière, X se lit de droite à gauche ; sur le côté gauche, Z se lit de droite à gauche.
- Les pages de couches gardent l’entrée en bas et X croissant vers la droite. Les pointillés indiquent l’emprise des murs, pas une cloison intérieure.

## Ordre de construction

1. Réserver les 25 × 17 blocs des murs et le débord du toit. Prévoir aussi le perron jusqu’à Z=-4 ; le jardin et la clôture sont à choisir autour de cette emprise.
2. Poser les couches Y=-1 à 4 : première marche, socle, maçonnerie, ouvertures et porte d’entrée. Ne pas remplir le centre : ce dossier représente seulement l’enveloppe extérieure.
3. Poser Y=5 à 9 : colombages, fenêtres du niveau supérieur, jardinières et auvent. Les vitres peuvent être réalisées en blocs ou panneaux selon le rendu recherché.
4. Poser Y=10 à 18 : pignons, toiture et lucarnes selon les couches. Les flèches des cellules d’escalier désignent leur côté haut ; elles ne désignent pas le nord. Les cellules H sont du bois plein, pas des demi-dalles. Aux croisements de toit, suivre la couche plutôt que prolonger chaque pente indépendamment.
5. Poursuivre les deux cheminées jusqu’à Y=22. Les cellules C occupent X=2..3 et X=21..22, avec Z=11..12. Elles traversent le toit ; une cellule ne reçoit jamais deux matériaux.
6. Ajouter les lanternes, bannières et végétation. Les cellules de végétation indiquent un volume décoratif à adapter avec feuilles, fleurs et jardinières. Ne pas compter ces éléments comme des dimensions du bâtiment.

## Ce qui est conservé et ce qui est choisi

La référence guide la silhouette, le grand pignon avant à gauche, la petite lucarne à droite, les deux niveaux, la pierre, le bois, les fenêtres, le porche, les lanternes et la végétation. Elle ne donne pas de mesures fiables et ne permet pas d’imposer un raccord de toiture unique. Les dimensions, la grille, les coordonnées des ouvertures et le placement exact des deux cheminées sont donc des choix de reconstruction, explicitement proposés.

Le toit est composé d’un toit principal à deux pentes (axe Z=8, hauteur 17), d’un grand pignon avant transversal (axe X=7, hauteur 19), d’une lucarne avant (axe X=20) et d’une lucarne arrière (axe X=12). La hauteur du grand pignon décroît derrière Z=4 pour se raccorder au toit principal. Le même calcul de surface sert aux quatre façades, à la vue du dessus et aux couches.

La clôture, le portail et l’allée du jardin sont des aménagements extérieurs libres ; ils ne sont pas cotés faute d’échelle fiable sur la référence. Aucun intérieur ni mobilier n’est défini.

## Matériaux

Les quantités ci-dessous comptent les cellules du modèle, avec les parties cachées de l’enveloppe. Ce sont des repères pour la construction : D compte séparément la moitié basse et la moitié haute d’une porte, V regroupe plusieurs possibilités de décoration ; ce n’est donc pas une liste exacte d’objets à collecter en survie.

'''
notes+='| Code | Matériau | Cellules |\n|---|---|---:|\n'
for m in M: notes+=f'| {m} | {M[m][0]} | {counts[m]} |\n'
notes+='\n## Vérifications réalisées\n\n- Unicité des coordonnées : aucun doublon.\n- Mêmes positions et mêmes matériaux dans toutes les projections.\n- Sommet du toit à 19, cheminées à 23, emprise des murs 25 × 17 et enveloppe de toiture 27 × 19.\n- 24 couches couvrent intégralement le modèle, de Y=-1 à Y=22.\n- Le CSV répertorie chaque cellule et la direction du côté haut de chaque escalier.\n\nCes contrôles vérifient la cohérence du modèle. Ils ne démontrent pas une reproduction exacte de l’image ni un résultat testé dans Minecraft.\n'
(OUT/'Guide_de_construction_v2.md').write_text(notes,encoding='utf-8')
print(json.dumps({'pdf':str(PDF),'cells':len(model),'counts':dict(counts),'pages':5},ensure_ascii=False))
