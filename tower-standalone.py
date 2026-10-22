from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,json
P=Path(__file__).parent
# Reuse original drawing primitives; retain exact room footprints and walkways.
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import json, zipfile, math
P=Path(__file__).parent
W,H,S=2048,1536,2
im=Image.new('RGB',(W*S,H*S),'#0c1017'); d=ImageDraw.Draw(im)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def rect(b,fill,outline=None,width=1,r=0):
 b=tuple(int(v*S) for v in b)
 if r:d.rounded_rectangle(b,r*S,fill=fill,outline=outline,width=width*S)
 else:d.rectangle(b,fill=fill,outline=outline,width=width*S)
def line(points,fill,width=1):d.line([(int(x*S),int(y*S)) for x,y in points],fill=fill,width=width*S)
def text(x,y,t,size=20,fill='#e8edf5',weight=False):d.text((x*S,y*S),t,font=ImageFont.truetype(bold if weight else font,size*S),fill=fill)
def ellipse(b,fill,outline=None,width=1):d.ellipse(tuple(int(v*S) for v in b),fill=fill,outline=outline,width=width*S)
walls=[]
def wall(x1,y1,x2,y2):
 walls.append((x1,y1,x2,y2));rect((x1,y1,x2,y2),'#39414d');rect((x1+3,y1+3,x2-3,y2-3),'#1c222c')
def glass(x1,y1,x2,y2):
 walls.append((x1,y1,x2,y2));rect((x1,y1,x2,y2),'#213a4c');line([(x1,y1),(x2,y1)],'#6b9bad',2)
def plant(x,y):
 ellipse((x-22,y-22,x+22,y+22),'#11151c','#4e5968',2)
 for a in range(0,360,60):
  dx,dy=math.cos(math.radians(a))*17,math.sin(math.radians(a))*17
  ellipse((x+dx-10,y+dy-8,x+dx+10,y+dy+8),'#29594c')
 ellipse((x-7,y-7,x+7,y+7),'#55927b')
def chair(x,y,blue=False):
 rect((x-19,y-18,x+19,y+20),'#0c1017',r=9)
 rect((x-16,y-16,x+16,y+14),'#263952' if blue else '#343b47','#5c6978',1,7)
 rect((x-17,y+10,x+17,y+20),'#0066ff' if blue else '#515b69',r=5)
def desk(x,y):
 chair(x,y+52)
 rect((x-66,y-29,x+70,y+28),'#090d13',r=8)
 rect((x-70,y-35,x+66,y+21),'#303947','#707b88',1,6)
 rect((x-31,y-28,x+31,y-6),'#0a0f17','#5a718b',1,3)
 line([(x-27,y-23),(x+25,y-23)],'#0b80ff',2)
 rect((x-22,y+1,x+21,y+9),'#141b25',r=2)
 rect((x+40,y-19,x+52,y-3),'#cdd3dc',r=2)
def label(x,y,n,title,sub):
 text(x,y,n,16,'#168cff',True);text(x+35,y-3,title,21,weight=True);text(x+35,y+29,sub,12,'#8c9aaf')

def poly(pts,fill,outline=None,width=1):
 d.polygon([(int(x*S),int(y*S)) for x,y in pts],fill=fill)
 if outline:line(pts+[pts[0]],outline,width)
def panel(b,c='#1c354b',edge='#32658b',cut=16):
 x,y,r,bottom=b
 poly([(x+cut,y),(r-cut,y),(r,y+cut),(r,bottom-cut),(r-cut,bottom),(x+cut,bottom),(x,bottom-cut),(x,y+cut)],c,edge,2)
def arc(cx,cy,r,start,end,c,w=3):
 pts=[(cx+math.cos(math.radians(a))*r,cy+math.sin(math.radians(a))*r) for a in range(start,end+1,2)]
 line(pts,c,w)
def console(x,y,c):
 chair(x,y+55,True)
 panel((x-75,y-32,x+75,y+30),'#0b131f','#486078',10)
 panel((x-72,y-38,x+72,y+19),'#283a4a','#59788e',9)
 line([(x-55,y+20),(x+55,y+20)],c,3)
 rect((x-48,y-31,x+48,y-5),'#06111e',c,1,3)
 for j in range(7):line([(x-42+j*12,y-11),(x-42+j*12,y-15-(j*7)%13)],c,3)
 rect((x-28,y+2,x+28,y+9),'#101e2a','#435e73',1,2)
def hologram(x,y,c,scale=1):
 ellipse((x-53,y-14,x+53,y+14),'#0b1c2b',c,2)
 for r in (23,35,47):arc(x,y,r,205,335,c,1)
 line([(x,y-90),(x,y-23)],'#285370',1)
 poly([(x,y-102),(x+35,y-69),(x,y-38),(x-35,y-69)],'#123851',c,2)
 line([(x-35,y-69),(x+35,y-69)],c)
 line([(x,y-102),(x,y-38)],c)
# Dark structural shell with precise engineering grid.
rect((32,32,2016,1504),'#080d16','#425369',2,40)
for x in range(48,2010,32):line([(x,48),(x,1488)],'#101c29')
for y in range(48,1490,32):line([(48,y),(2000,y)],'#101c29')
for x in (56,1992):line([(x,96),(x,1424)],'#226991',2)
# Circulation: continuous central spine and transverse bridge corridors.
panel((696,56,1352,1480),'#111e2b','#243d56',28)
for y in (488,984,1416):
 rect((72,y,1976,y+32),'#142335')
 line([(96,y+16),(1952,y+16)],'#234765',1)
for x in (713,1335):
 for y in range(512,1400,80):line([(x,y),(x,y+48)],'#057fff',3)
rooms=[
 ((80,80,672,480),'01','DIRECCIÓN','ESTRATEGIA / ROB GIMÉNEZ','#b5d9f2','#1b2937'),
 ((736,80,1312,480),'02','SALA DE REUNIONES','MESA TÁCTICA / EQUIPO','#53b7ff','#142a42'),
 ((1376,80,1968,480),'03','CLIENTES & GROWTH','RELACIONES / EXPANSIÓN','#69c6e3','#142d37'),
 ((80,528,672,976),'04','MARKETING & ADS','CAMPAÑAS / PERFORMANCE','#237cff','#142347'),
 ((1376,528,1968,976),'05','ESTUDIO CREATIVO','DISEÑO / CONTENIDO','#c4d9ed','#26303c'),
 ((80,1024,672,1408),'06','SEO & AUTOMATIZACIÓN','DATOS / SISTEMAS','#2da7d9','#102c3b'),
 ((1376,1024,1968,1408),'07','GO AI LAB','AGENCYOS / INTELIGENCIA','#53d5f4','#123140')]
for (x,y,r,b),num,title,sub,c,bg in rooms:
 panel((x,y,r,b),bg,'#3b5269',18)
 # Inset metallic frame, floor lines, ceiling light strips.
 for yy in range(y+112,b-30,40):line([(x+23,yy),(r-23,yy)],'#2b3b4b')
 line([(x+25,y+16),(r-25,y+16)],c,4)
 rect((x+14,y+20,x+21,b-23),'#354252')
 rect((r-21,y+20,r-14,b-23),'#354252')
 panel((x+26,y+30,r-26,y+105),'#0b1724','#32475d',8)
 text(x+43,y+45,num,16,c,True)
 text(x+80,y+40,title,20,'#eff6ff',True)
 text(x+80,y+72,sub,11,'#91a9c1')
 mid=(x+r)//2
 for left,right in [(x+10,mid-56),(mid+56,r-10)]:
  rect((left,b-22,right,b-6),'#234359')
  line([(left,b-22),(right,b-22)],c,2)
  for xx in range(left+6,right,32):line([(xx,b-20),(xx+10,b-8)],'#416b80')
 line([(mid-46,b-9),(mid+46,b-9)],c,3)
 for xx in (x+30,r-38):rect((xx,y+12,xx+8,y+18),'#e43a4c',r=1)
# Executive suite
console(356,282,'#b5d9f2');hologram(551,340,'#b5d9f2')
for x in (142,610):
 panel((x-22,366,x+22,426),'#17202c','#576f83',6)
 line([(x-12,380),(x+12,380)],'#a4cee5',2)
# Tactical circular conference table
ellipse((880,219,1168,407),'#050b13','#3b668b',2)
ellipse((890,213,1158,389),'#263b51','#7ca5c2',3)
ellipse((930,246,1118,356),'#071c2f','#229aff',2)
for radius in (25,43):arc(1024,301,radius,0,358,'#40b6ff',2)
line([(958,301),(1090,301)],'#6abdf0',1);line([(1024,260),(1024,342)],'#6abdf0',1)
for x in (942,1024,1106):chair(x,197,True);chair(x,420,True)
chair(850,303,True);chair(1198,303,True)
# Growth command desks
console(1548,282,'#69c6e3');console(1788,282,'#69c6e3')
for x in range(1450,1900,80):rect((x,402,x+44,407),'#407d92',r=2)
# Two studio wings
for x in (244,498):
 for y in (735,875):console(x,y,'#237cff')
for x in (1540,1804):
 for y in (735,875):console(x,y,'#c4d9ed')
# Server arrays and data desk
console(300,1220,'#2da7d9')
for x in (505,565):
 panel((x,1160,x+44,1334),'#101b28','#51758b',7)
 for y in range(1175,1320,24):
  rect((x+7,y,x+37,y+13),'#21394b',r=2);ellipse((x+28,y+4,x+32,y+8),'#3caaff')
# AI command bay: one actual existing agent, two clearly empty docks.
hologram(1672,1214,'#53d5f4')
text(1580,1310,'DEFAULT',21,'#eefaff',True)
text(1562,1340,'AGENCYOS · 55 HABILIDADES',10,'#88bfd6')
for x in (1472,1872):
 ellipse((x-48,1250,x+48,1280),'#0b1c2b','#30566d',2)
 line([(x-12,1265),(x+12,1265)],'#41647b',2)
 text(x-45,1310,'DISPONIBLE',11,'#66849c')
# Arc-core lobby, transparent display rings and exact GO ADS logo.
for r,c,w in [(232,'#243e58',2),(219,'#1677bf',2),(201,'#1f4e70',4),(181,'#1675d1',2)]:
 for a in (0,120,240):arc(1024,752,r,a+6,a+106,c,w)
ellipse((854,582,1194,922),'#0b1726','#356184',2)
for a in range(0,360,15):
 rad=math.radians(a)
 line([(1024+math.cos(rad)*226,752+math.sin(rad)*226),(1024+math.cos(rad)*236,752+math.sin(rad)*236)],'#3aa7ea',2)
logo=Image.open(P/'go-ads-logo-original.png').convert('RGBA');logo=logo.crop(logo.getbbox());logo.thumbnail((315*S,240*S),Image.Resampling.LANCZOS)
im.paste(logo,(1024*S-logo.width//2,752*S-logo.height//2),logo)
panel((815,1000,1233,1092),'#0b1522','#52768e',16)
text(884,1018,'GO ADS / CONTROL',22,'#edf8ff',True)
text(899,1052,'HAZLO DIFERENTE',14,'#63b8ed')
for x in (821,1221):rect((x,1026,x+5,1065),'#e83b50',r=2)
# Reception work surface / elevator entrance
panel((872,1150,1176,1222),'#1d3449','#5a87a4',14)
rect((902,1164,1146,1191),'#061a2b','#2993cf',1,4)
for x in range(914,1130,26):line([(x,1171),(x+14,1171)],'#39c1ef',2)
text(894,1284,'TORRE GO ADS',28,'#dfeeff',True)
text(917,1327,'CENTRO DE MANDO',14,'#6397bd')
panel((960,1393,1088,1470),'#0b2c51','#2189ff',14)
line([(1005,1439),(1024,1420),(1043,1439)],'#b4e8ff',3)
# Architectural and wayfinding micro-details.
for x,y in [(75,1456),(1945,1456),(707,98),(1337,98)]:rect((x,y,x+20,y+4),'#e53348')
im=im.resize((W,H),Image.Resampling.LANCZOS);im.save(P/'go-ads-tower-v3.png')
# Original animated humanoid robotic avatar (64x64, two breathing-light frames).
sprite=Image.new('RGBA',(128,64));q=ImageDraw.Draw(sprite)
for f in range(2):
 ox=f*64
 def box(b,c,edge=None,r=0):
  b=(b[0]+ox,b[1],b[2]+ox,b[3]);q.rounded_rectangle(b,r,fill=c,outline=edge)
 q.ellipse((ox+12,52,ox+53,62),fill='#0c1729',outline='#41bce6')
 box((22,37,30,55),'#647b94','#c0d4e4',2);box((34,37,42,55),'#647b94','#c0d4e4',2)
 box((19,52,30,57),'#162a43','#77a6ca',2);box((34,52,45,57),'#162a43','#77a6ca',2)
 box((13,22,20,41),'#59748e','#bad5e6',3);box((44,22,51,41),'#59748e','#bad5e6',3)
 box((21,21,43,40),'#92adc4','#e0edf6',4)
 q.polygon([(ox+24,24),(ox+40,24),(ox+37,35),(ox+27,35)],fill='#143453')
 q.ellipse((ox+29,26,ox+35,32),fill='#c7fbff' if f else '#38bfff',outline='#00a7ed')
 box((23,7,41,21),'#afc3d4','#eaf6ff',4)
 box((25,12,39,16),'#02304b',r=2)
 q.line([(ox+27,14),(ox+37,14)],fill='#8ffaff' if f else '#30b9ff',width=2)
 box((15,24,18,27),'#ed304c',r=1)
sprite.save(P/'go-ai-avatar-v3.png')
print('Rendered tower and animated agent sprites')
