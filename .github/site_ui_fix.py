from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Cargar una sola capa de interfaz al final del documento, sin tocar la lógica existente.
marker='<!-- WR-UI-FIX-2026 -->'
if marker not in s:
    block=r'''<!-- WR-UI-FIX-2026 -->
<style>
/* Buscador y categorias: una sola zona limpia y desplegable */
.buscador-box{position:relative}
.buscador-box .wr-categoria-toggle{width:100%;display:flex;align-items:center;justify-content:space-between;gap:12px;border:0;border-radius:10px;background:#fff;color:#151b27;padding:15px 17px;font-size:16px;font-weight:800;cursor:pointer;margin-top:18px}
.wr-categoria-toggle span:last-child{font-size:20px;transition:.2s}
.wr-categoria-toggle.abierto span:last-child{transform:rotate(180deg)}
.buscador-box .formulario{display:grid;max-height:0;overflow:hidden;opacity:0;transition:max-height .3s ease,opacity .2s ease;margin-top:0}
.buscador-box .formulario.wr-visible{max-height:500px;opacity:1;margin-top:12px}
.wr-catalogo-acordeon{max-width:1250px;margin:0 auto 35px;background:#fff;border-radius:14px;box-shadow:0 4px 16px rgba(0,0,0,.08);overflow:hidden;border:1px solid #e4e6e9}
.wr-catalogo-acordeon>button{width:100%;border:0;background:#151b27;color:#fff;padding:18px 20px;display:flex;justify-content:space-between;align-items:center;font-size:18px;font-weight:800;cursor:pointer;text-align:left}
.wr-catalogo-acordeon>button b{color:#f5b800}
.wr-catalogo-contenido{display:none;padding:18px 20px}
.wr-catalogo-acordeon.abierto .wr-catalogo-contenido{display:block}
.wr-categoria{border:1px solid #e3e5e8;border-radius:10px;margin-bottom:9px;overflow:hidden}
.wr-categoria:last-child{margin-bottom:0}
.wr-categoria>button{width:100%;border:0;background:#f7f8fa;padding:13px 15px;display:flex;justify-content:space-between;align-items:center;color:#151b27;font-weight:800;cursor:pointer;text-align:left}
.wr-categoria-opciones{display:none;padding:10px 12px;background:#fff}
.wr-categoria.abierto .wr-categoria-opciones{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.wr-categoria-opciones a{display:block;padding:10px;border:1px solid #e5e6e8;border-radius:8px;color:#333;text-decoration:none;font-size:13px;background:#fff}
.wr-categoria-opciones a:hover{border-color:#f5b800;background:#fffdf2}
@media(max-width:650px){.buscador-box .wr-categoria-toggle{font-size:14px}.wr-categoria.abierto .wr-categoria-opciones{grid-template-columns:1fr 1fr}.wr-catalogo-contenido{padding:12px}}
@media(max-width:420px){.wr-categoria.abierto .wr-categoria-opciones{grid-template-columns:1fr}}
</style>
<script>
(function(){
  function initWRUI(){
    const box=document.querySelector('.buscador-box');
    const form=document.querySelector('.buscador-box .formulario');
    if(box&&form&&!box.querySelector('.wr-categoria-toggle')){
      const toggle=document.createElement('button');
      toggle.type='button';
      toggle.className='wr-categoria-toggle';
      toggle.innerHTML='<span>Seleccionar vehículo</span><span>⌄</span>';
      toggle.addEventListener('click',function(){
        const open=form.classList.toggle('wr-visible');
        toggle.classList.toggle('abierto',open);
      });
      form.parentNode.insertBefore(toggle,form);
    }

    const productos=document.querySelector('.productos');
    if(productos&&!document.querySelector('.wr-catalogo-acordeon')){
      const section=document.createElement('section');
      section.className='wr-catalogo-acordeon';
      section.innerHTML='<button type="button"><span>🔋 <b>Categorías de baterías</b></span><span>⌄</span></button><div class="wr-catalogo-contenido"></div>';
      const content=section.querySelector('.wr-catalogo-contenido');
      const cards=[...productos.querySelectorAll('.producto')];
      const grupos={};
      cards.forEach(card=>{
        const title=(card.querySelector('h3')||{}).textContent?.trim()||'Batería';
        const link=card.getAttribute('onclick')||'';
        const href=(link.match(/location\.href=['\"]([^'\"]+)/)||[])[1]||'#';
        const key=title.startsWith('N-')?'JIS':title.startsWith('NS')?'JIS':'Otros';
        (grupos[key]??=[]).push({title,href});
      });
      Object.entries(grupos).forEach(([name,items])=>{
        const cat=document.createElement('div');cat.className='wr-categoria';
        cat.innerHTML='<button type="button"><span>'+name+'</span><span>+</span></button><div class="wr-categoria-opciones"></div>';
        const opts=cat.querySelector('.wr-categoria-opciones');
        items.forEach(x=>{const a=document.createElement('a');a.href=x.href;a.textContent=x.title;opts.appendChild(a)});
        cat.querySelector('button').addEventListener('click',()=>cat.classList.toggle('abierto'));
        content.appendChild(cat);
      });
      section.querySelector('button').addEventListener('click',()=>section.classList.toggle('abierto'));
      productos.parentNode.insertBefore(section,productos);
    }
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',initWRUI); else initWRUI();
})();
</script>
'''
    s=s.replace('</body>',block+'\n</body>',1)
    p.write_text(s,encoding='utf-8')
