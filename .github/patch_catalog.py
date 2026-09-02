from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'index.html'
DATA = ROOT / 'data' / 'catalogo-cr-2026.json'

s = INDEX.read_text(encoding='utf-8')
data = json.loads(DATA.read_text(encoding='utf-8'))
items = data['baterias']

# CCA: nunca inventar para referencias que no tengan dato verificado.
s = s.replace(
    '  "42R":{min:500,rec:550,perfil:"Sedán / SUV ligero"},',
    '  "42R":{min:null,rec:null,perfil:"CCA según referencia comercial; confirmar aplicación"},\n  "36F":{min:null,rec:null,perfil:"CCA según referencia comercial; confirmar aplicación"},',
    1,
)

# Evitar equivalencias BCI forzadas para referencias cuyo formato comercial no permite
# demostrar equivalencia solo por el nombre.
needle = '  if(/N70ZL|N70Z|N70/.test(t)) return "BCI 27";'
if 'if(/42R|R42L|36F/.test(t)) return "Verificar equivalencia BCI";' not in s:
    s = s.replace(needle, needle + '\n  if(/42R|R42L|36F/.test(t)) return "Verificar equivalencia BCI";', 1)

# Catálogo visible, generado desde datos verificables locales.
start = '<section id="catalogo-cr-verificado" class="catalogo-cr-verificado">'
end = '</section>'
if start in s:
    a = s.index(start)
    b = s.index(end, a) + len(end)
    s = s[:a] + s[b:]

from collections import defaultdict
by_brand = defaultdict(list)
for x in items:
    by_brand[x['marca']].append(x)

cards = []
for brand in sorted(by_brand, key=str.casefold):
    rows = []
    for x in by_brand[brand]:
        details = []
        if x.get('grupo'):
            details.append('Grupo ' + x['grupo'])
        if x.get('dimensiones_mm'):
            details.append(x['dimensiones_mm'] + ' mm')
        if x.get('cca') is not None:
            details.append(str(x['cca']) + ' CCA')
        if not details:
            details.append('Especificación por confirmar')
        rows.append(
            '<article class="catalogo-cr-card">'
            '<h4>' + x['modelo'] + '</h4>'
            '<p>' + ' · '.join(details) + '</p>'
            '<a href="https://wa.me/50663928294?text=' +
            'Hola%20WRbateriasCr%2C%20quiero%20consultar%20por%20la%20bater%C3%ADa%20' +
            x['modelo'].replace(' ', '%20') + '" target="_blank" rel="noopener">Consultar</a>'
            '</article>'
        )
    cards.append('<div class="catalogo-cr-marca"><h3>' + brand + '</h3><div class="catalogo-cr-grid">' + ''.join(rows) + '</div></div>')

section = (
    start + '\n'
    '<div class="titulo"><h2>Catálogo verificado en Costa Rica</h2>'
    '<p>Referencias comerciales encontradas en distribuidores y comercios locales. Última revisión: 2 de septiembre de 2026.</p></div>'
    '<div class="catalogo-cr-aviso">⚠️ La referencia comercial no sustituye la verificación de compatibilidad. Antes de instalar: medidas, polaridad, posición de bornes, capacidad y CCA.</div>'
    + ''.join(cards) + '\n'
    '<p class="catalogo-cr-fuentes">Fuentes consultadas: La Casa de las Baterías, Walmart Costa Rica, Maxipalí, Coopelesca, Baterías CR y El Genio de las Baterías.</p>'
    + end
)

marker = '<section class="marcas" id="marcas">'
if marker not in s:
    raise SystemExit('No se encontró el punto de inserción del catálogo')
s = s.replace(marker, section + '\n\n' + marker, 1)

css_marker = '</style>'
css = '''
.catalogo-cr-verificado{background:#f4f5f7;padding:55px 20px 70px}
.catalogo-cr-verificado .titulo{max-width:1100px;margin:0 auto 20px}
.catalogo-cr-aviso{max-width:1100px;margin:0 auto 30px;background:#fff;border-left:5px solid #f5b800;border-radius:10px;padding:15px 18px;color:#555;line-height:1.5}
.catalogo-cr-marca{max-width:1100px;margin:0 auto 28px}
.catalogo-cr-marca h3{font-size:22px;margin:0 0 12px;color:#151b27}
.catalogo-cr-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.catalogo-cr-card{background:#fff;border-radius:12px;padding:17px;box-shadow:0 3px 12px rgba(0,0,0,.08);border:1px solid #e4e6e9}
.catalogo-cr-card h4{font-size:18px;margin-bottom:9px;color:#151b27}
.catalogo-cr-card p{font-size:13px;color:#666;line-height:1.45;min-height:38px}
.catalogo-cr-card a{display:inline-block;margin-top:12px;background:#151b27;color:#fff;text-decoration:none;padding:8px 13px;border-radius:6px;font-size:13px;font-weight:bold}
.catalogo-cr-fuentes{max-width:1100px;margin:25px auto 0;color:#777;font-size:12px;line-height:1.5}
@media(max-width:900px){.catalogo-cr-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:520px){.catalogo-cr-grid{grid-template-columns:1fr}}
'''
if '.catalogo-cr-verificado' not in s:
    s = s.replace(css_marker, css + css_marker, 1)

# Chatbot: referencias comerciales que antes no tenían respuesta específica.
chat_marker = '  /* TAMAÑOS */'
chat_add = '''  /* REFERENCIAS COMERCIALES CR */

  if(t.includes("42r") || t.includes("r42l")){
    return("🔋 <strong>42R / R42L</strong>"+
      "<br><br>En Costa Rica se encuentran referencias como Record R42-O-MF y R42L-O-MF, con 242×175×175 mm y 330 CCA en la ficha local."+
      "<br><br>La equivalencia BCI no se debe asumir solo por el nombre; hay que verificar dimensiones y polaridad."+
      "<br><br><a href="https://wa.me/50663928294" target="_blank" rel="noopener">📲 Consultar disponibilidad</a>");
  }

  if(t.includes("36f")){
    return("🔋 <strong>36F / 36F-P</strong>"+
      "<br><br>Referencia comercial encontrada en Costa Rica: Tasco Gold 36F-P."+
      "<br><br>La ficha debe confirmarse por dimensiones, polaridad, capacidad y CCA antes de instalar."+
      "<br><br><a href="https://wa.me/50663928294" target="_blank" rel="noopener">📲 Consultar disponibilidad</a>");
  }

'''
if '/* REFERENCIAS COMERCIALES CR */' not in s:
    s = s.replace(chat_marker, chat_add + chat_marker, 1)

# Marcar la revisión sin duplicar el marcador.
if '/* CATALOGO-CR-REVISION-2026 */' not in s:
    s = s.replace('</script>', '/* CATALOGO-CR-REVISION-2026 */\n</script>', 1)

INDEX.write_text(s, encoding='utf-8')
print(f'Catálogo actualizado: {len(items)} referencias comerciales')
