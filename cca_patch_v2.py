from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = 'CCA-CR-V2-INTEGRADO'
if marker in s:
    print('CCA ya integrado')
    raise SystemExit(0)

css_anchor = '''.nota{\n  color:#666;\n  font-size:13px;\n}'''
css_insert = '''\n\n/* CCA-CR-V2-INTEGRADO */\n.cca-panel{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:16px 0;}\n.cca-card{background:#f5f6f8;border:1px solid #e2e4e8;border-radius:10px;padding:14px 10px;text-align:center;}\n.cca-card strong{display:block;font-size:22px;color:#151b27;margin-top:5px;}\n.cca-card span{color:#666;font-size:12px;font-weight:bold;text-transform:uppercase;}\n.cca-aviso{color:#666;font-size:12px;line-height:1.45;margin-top:5px;}\n@media(max-width:650px){.cca-panel{grid-template-columns:1fr;}}\n'''
if css_anchor not in s:
    raise SystemExit('No se encontro ancla CSS')
s = s.replace(css_anchor, css_anchor + css_insert, 1)

data_anchor = 'const baseDatos = {'
data_insert = '''\n\n/* CCA-CR-V2-INTEGRADO */\n/* Valores de referencia derivados de catalogos/comercializacion en Costa Rica. No sustituyen la verificacion de aplicacion. */\nconst referenciaCCA = {\n  'N-40': {min:410, rec:500, perfil:'Compacto / estandar'},\n  'NS40M': {min:400, rec:500, perfil:'Compacto / estandar'},\n  'N-50': {min:450, rec:600, perfil:'Sedan / SUV ligero'},\n  '42R': {min:500, rec:550, perfil:'Sedan / SUV ligero'},\n  'N-60': {min:439, rec:500, perfil:'Sedan / SUV mediano'},\n  'N-70': {min:600, rec:700, perfil:'SUV / pickup / diesel'},\n  'N-80': {min:null, rec:null, perfil:'Confirmar aplicacion'},\n  'N-100': {min:680, rec:760, perfil:'Trabajo pesado / alta demanda'}\n};\n\nfunction obtenerReferenciaCCA(bateria){\n  const texto=String(bateria||'').toUpperCase();\n  const claves=Object.keys(referenciaCCA).sort((a,b)=>b.length-a.length);\n  for(const clave of claves){\n    if(texto.includes(clave.toUpperCase())) return referenciaCCA[clave];\n  }\n  return {min:null,rec:null,perfil:'Confirmar aplicacion'};\n}\n\nfunction formatearCCA(valor){\n  return Number.isFinite(valor) ? valor+' CCA' : 'Por confirmar';\n}\n'''
if data_anchor not in s:
    raise SystemExit('No se encontro ancla baseDatos')
s = s.replace(data_anchor, data_anchor + data_insert, 1)

old_return = '''    bateria:datos[3],\n    nota:datos[4]\n  };'''
new_return = '''    bateria:datos[3],\n    nota:datos[4],\n    cca:obtenerReferenciaCCA(datos[3])\n  };'''
if old_return not in s:
    raise SystemExit('No se encontro retorno de registro')
s = s.replace(old_return, new_return, 1)

# Insertar panel justo despues del bloque de bateria recomendada, usando el texto real del archivo.
pattern = r'''(<div class="bateria-recomendada">'\+\n\s*registro\.bateria\+\n\s*"</div>"\+)'''
replacement = r'''\1+\n\n    '<div class="cca-panel">'+\n      '<div class="cca-card"><span>CCA minimo de referencia</span><strong>'+formatearCCA(registro.cca.min)+'</strong></div>'+\n      '<div class="cca-card"><span>CCA recomendado</span><strong>'+formatearCCA(registro.cca.rec)+'</strong></div>'+\n      '<div class="cca-card"><span>Perfil</span><strong style="font-size:17px">'+registro.cca.perfil+'</strong></div>'+\n    '</div>'+\n    '<p class="cca-aviso"><strong>Referencia Costa Rica:</strong> orienta la seleccion de bateria disponible localmente. La aplicacion exacta puede variar por motor, generacion, version, medidas y polaridad.</p>'+'''
new_s, count = re.subn(pattern, replacement, s, count=1)
if count != 1:
    raise SystemExit('No se encontro bloque de resultado')
s = new_s

# Chatbot: insertar CCA despues de la recomendacion y antes de la informacion.
chat_anchor = '''       registro.bateria+\n       "</strong>"+'''
chat_insert = '''       registro.bateria+\n       "</strong>"+\n\n       "<br><br>"+\n       "❄️ CCA minimo de referencia: <strong>"+formatearCCA(registro.cca.min)+"</strong>"+\n       "<br>⚡ CCA recomendado: <strong>"+formatearCCA(registro.cca.rec)+"</strong>"+\n       "<br>🎯 Perfil: <strong>"+registro.cca.perfil+"</strong>"+\n\n       "<br><br>"+\n       '<span style="font-size:12px;color:#666">Referencia Costa Rica; confirmar aplicacion exacta antes de instalar.</span>'+'''
if chat_anchor not in s:
    raise SystemExit('No se encontro ancla del chatbot')
s = s.replace(chat_anchor, chat_insert, 1)

p.write_text(s, encoding='utf-8')
print('CCA integrado correctamente')
