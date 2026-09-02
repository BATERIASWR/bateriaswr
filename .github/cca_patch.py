from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if '/* CCA-COSTA-RICA-INTEGRADO */' in s:
    raise SystemExit(0)

css = '.nota{\n  color:#666;\n  font-size:13px;\n}'
css_add = '''\n\n/* CCA Y PERFIL DE REFERENCIA - COSTA RICA */\n.cca-panel{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:16px 0}.cca-card{background:#f5f6f8;border:1px solid #e2e4e8;border-radius:10px;padding:14px 10px;text-align:center}.cca-card strong{display:block;font-size:22px;color:#151b27;margin-top:5px}.cca-card span{color:#666;font-size:12px;font-weight:bold;text-transform:uppercase}.cca-aviso{color:#666;font-size:12px;line-height:1.45;margin-top:5px}@media(max-width:650px){.cca-panel{grid-template-columns:1fr}}\n'''
if css not in s:
    raise SystemExit('CSS no encontrado')
s = s.replace(css, css + css_add, 1)

anchor = 'const baseDatos = {'
data = '''\n\n/* CCA-COSTA-RICA-INTEGRADO */\n/* Referencia de baterías comercializadas en Costa Rica; no sustituye la verificación de aplicación. */\nconst referenciaCCA={\n  'N-40':{min:410,rec:500,perfil:'Compacto / estándar'},\n  'NS40M':{min:400,rec:500,perfil:'Compacto / estándar'},\n  'N-50':{min:450,rec:600,perfil:'Sedán / SUV ligero'},\n  '42R':{min:500,rec:550,perfil:'Sedán / SUV ligero'},\n  'N-60':{min:439,rec:500,perfil:'Sedán / SUV mediano'},\n  'N-70':{min:600,rec:700,perfil:'SUV / pickup / diésel'},\n  'N-80':{min:null,rec:null,perfil:'Confirmar aplicación'},\n  'N-100':{min:680,rec:760,perfil:'Trabajo pesado / alta demanda'}\n};\nfunction obtenerReferenciaCCA(bateria){\n  const t=String(bateria||'').toUpperCase();\n  for(const k of Object.keys(referenciaCCA).sort((a,b)=>b.length-a.length)){\n    if(t.includes(k.toUpperCase())) return referenciaCCA[k];\n  }\n  return {min:null,rec:null,perfil:'Confirmar aplicación'};\n}\nfunction formatearCCA(v){return Number.isFinite(v)?v+' CCA':'Por confirmar'}\n'''
if anchor not in s:
    raise SystemExit('baseDatos no encontrada')
s = s.replace(anchor, anchor + data, 1)

old = '''    bateria:datos[3],\n    nota:datos[4]\n  };'''
new = '''    bateria:datos[3],\n    nota:datos[4],\n    cca:obtenerReferenciaCCA(datos[3])\n  };'''
if old not in s:
    raise SystemExit('retorno de registro no encontrado')
s = s.replace(old, new, 1)

old = '''    '<div class="bateria-recomendada">'+\n    registro.bateria+\n    "</div>"+\n\n    "<p><strong>Información:</strong> "+'''
new = '''    '<div class="bateria-recomendada">'+\n    registro.bateria+\n    "</div>"+\n\n    '<div class="cca-panel">'+\n      '<div class="cca-card"><span>CCA mínimo de referencia</span><strong>'+formatearCCA(registro.cca.min)+'</strong></div>'+\n      '<div class="cca-card"><span>CCA recomendado</span><strong>'+formatearCCA(registro.cca.rec)+'</strong></div>'+\n      '<div class="cca-card"><span>Perfil</span><strong style="font-size:17px">'+registro.cca.perfil+'</strong></div>'+\n    '</div>'+\n    '<p class="cca-aviso"><strong>Referencia Costa Rica:</strong> el CCA orienta la selección según baterías disponibles localmente. La aplicación exacta puede variar por motor, generación, versión, dimensiones y polaridad.</p>'+\n\n    "<p><strong>Información:</strong> "+'''
if old not in s:
    raise SystemExit('resultado no encontrado')
s = s.replace(old, new, 1)

old = '''       "ℹ️ "+registro.nota+'''
new = '''       "❄️ CCA mínimo de referencia: <strong>"+formatearCCA(registro.cca.min)+"</strong>"+\n       "<br>⚡ CCA recomendado: <strong>"+formatearCCA(registro.cca.rec)+"</strong>"+\n       "<br>🎯 Perfil: <strong>"+registro.cca.perfil+"</strong>"+\n       "<br><br>"+\n       '<span style="font-size:12px;color:#666">Referencia Costa Rica; confirmar aplicación exacta antes de instalar.</span>'+\n       "<br><br>"+\n       "ℹ️ "+registro.nota+'''
if old not in s:
    raise SystemExit('chat no encontrado')
s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
print('CCA integrado correctamente')
