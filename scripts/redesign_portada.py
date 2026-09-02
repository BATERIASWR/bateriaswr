# Trigger de reparación WR — no altera la lógica de la portada
from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

css = r'''
/* PORTADA WR - REDISEÑO VISUAL */
.hero{height:500px;background:#090b0f;overflow:hidden;position:relative}
.hero::before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 50% 35%,rgba(245,184,0,.16),transparent 45%),linear-gradient(120deg,#090b0f 0%,#151b27 55%,#090b0f 100%);z-index:0}
.hero-contenido{position:relative;z-index:2;background:linear-gradient(180deg,rgba(0,0,0,.12),rgba(0,0,0,.35));padding:25px 4% 35px;justify-content:flex-start}
.hero h1{font-size:48px;line-height:1.02;max-width:1000px;margin:8px auto;letter-spacing:.5px}
.hero h1 span{color:#f5b800}.hero p{font-size:20px;margin-bottom:18px}
.wr-cambio{width:min(1180px,100%);margin:auto;display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.wr-paso{position:relative;min-height:235px;border:1px solid rgba(245,184,0,.55);border-radius:16px;background:rgba(8,10,14,.78);overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding:14px 12px 16px;box-shadow:0 12px 35px rgba(0,0,0,.28)}
.wr-paso::after{content:"";position:absolute;inset:auto 0 0;height:3px;background:#f5b800}.wr-paso-num{position:absolute;top:12px;left:12px;width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:#f5b800;color:#111;font-weight:900;font-size:17px;z-index:3}
.wr-paso h3{position:relative;z-index:3;font-size:19px;color:#fff;margin-top:5px}.wr-paso h3 b{color:#f5b800}.wr-car{width:100%;height:150px;display:grid;place-items:center}.wr-car svg{width:92%;height:145px;filter:drop-shadow(0 8px 10px rgba(0,0,0,.45))}.wr-flecha{position:absolute;right:-25px;top:96px;color:#f5b800;font-size:38px;font-weight:900;z-index:5}
.wr-paso:nth-child(2){animation:wrPulse 3.8s ease-in-out infinite}.wr-paso:nth-child(3){animation:wrPulse 3.8s ease-in-out 1.9s infinite}@keyframes wrPulse{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
@media(max-width:750px){.hero{height:auto;min-height:620px}.hero h1{font-size:32px}.hero p{font-size:16px}.wr-cambio{grid-template-columns:1fr}.wr-paso{min-height:170px}.wr-car{height:105px}.wr-car svg{height:105px}.wr-flecha{display:none}}
'''

if '/* PORTADA WR - REDISEÑO VISUAL */' not in s:
    marker='/* DOMICILIO IMAGEN */'
    if marker not in s:
        raise SystemExit('No se encontró el punto seguro para CSS')
    s=s.replace(marker,css+'\n'+marker,1)

svg1='''<svg viewBox="0 0 520 190" xmlns="http://www.w3.org/2000/svg" aria-label="Carro con batería usada"><rect x="20" y="150" width="480" height="8" rx="4" fill="#f5b800" opacity=".75"/><path d="M100 125 L125 75 Q135 58 160 58 H350 Q380 58 398 82 L425 125 Z" fill="#252b35" stroke="#fff" stroke-width="4"/><circle cx="155" cy="128" r="27" fill="#090b0f" stroke="#fff" stroke-width="5"/><circle cx="370" cy="128" r="27" fill="#090b0f" stroke="#fff" stroke-width="5"/><rect x="205" y="65" width="105" height="45" rx="6" fill="#151b27" stroke="#aaa" stroke-width="3"/><rect x="220" y="55" width="75" height="10" rx="4" fill="#777"/><path d="M248 65v-12h18v12" stroke="#f5b800" stroke-width="5"/><path d="M255 72 l-13 18 h12 l-7 15 24-23 h-12z" fill="#f5b800"/></svg>'''
svg2='''<svg viewBox="0 0 520 190" xmlns="http://www.w3.org/2000/svg" aria-label="Retirando la batería"><rect x="20" y="150" width="480" height="8" rx="4" fill="#f5b800" opacity=".75"/><path d="M100 125 L125 75 Q135 58 160 58 H350 Q380 58 398 82 L425 125 Z" fill="#252b35" stroke="#fff" stroke-width="4"/><circle cx="155" cy="128" r="27" fill="#090b0f" stroke="#fff" stroke-width="5"/><circle cx="370" cy="128" r="27" fill="#090b0f" stroke="#fff" stroke-width="5"/><rect x="215" y="78" width="95" height="42" rx="6" fill="#151b27" stroke="#777" stroke-width="3" transform="rotate(-10 262 99)"/><path d="M215 45 Q260 20 305 45" fill="none" stroke="#f5b800" stroke-width="8" stroke-linecap="round"/><path d="M260 40 V78" stroke="#f5b800" stroke-width="8" stroke-linecap="round"/><path d="M250 68 l10 12 10-12" fill="none" stroke="#fff" stroke-width="4"/></svg>'''
svg3='''<svg viewBox="0 0 520 190" xmlns="http://www.w3.org/2000/svg" aria-label="Instalando batería nueva"><rect x="20" y="150" width="480" height="8" rx="4" fill="#f5b800"/><path d="M100 125 L125 75 Q135 58 160 58 H350 Q380 58 398 82 L425 125 Z" fill="#252b35" stroke="#fff" stroke-width="4"/><circle cx="155" cy="128" r="27" fill="#090b0f" stroke="#fff" stroke-width="5"/><circle cx="370" cy="128" r="27" fill="#090b0f" stroke="#fff" stroke-width="5"/><rect x="205" y="70" width="105" height="45" rx="6" fill="#151b27" stroke="#f5b800" stroke-width="4"/><rect x="220" y="60" width="75" height="10" rx="4" fill="#f5b800"/><path d="M248 70v-12h18v12" stroke="#fff" stroke-width="5"/><path d="M255 76 l-13 18 h12 l-7 15 24-23 h-12z" fill="#f5b800"/><path d="M245 35 l10 10 20-22" fill="none" stroke="#25D366" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>'''

hero=f'''<section class="hero"><div class="hero-contenido"><h1>CAMBIAMOS TU BATERÍA,<br><span>IMPULSAMOS TU CAMINO</span></h1><p>Encuentra la batería ideal para tu vehículo y llévala hasta donde estés.</p><div class="wr-cambio"><div class="wr-paso"><span class="wr-paso-num">1</span><div class="wr-car">{svg1}</div><h3><b>BATERÍA</b> USADA</h3><span class="wr-flecha">→</span></div><div class="wr-paso"><span class="wr-paso-num">2</span><div class="wr-car">{svg2}</div><h3><b>RETIRAMOS</b> LA ANTERIOR</h3><span class="wr-flecha">→</span></div><div class="wr-paso"><span class="wr-paso-num">3</span><div class="wr-car">{svg3}</div><h3><b>INSTALAMOS</b> LA NUEVA</h3></div></div></div></section>'''

s2=re.sub(r'<section class="hero">.*?</section>',hero,s,count=1,flags=re.S)
if s2==s:
    raise SystemExit('No se encontró la sección HERO')
p.write_text(s2,encoding='utf-8')
print('OK: portada rediseñada sin modificar la lógica del buscador/chatbot')
