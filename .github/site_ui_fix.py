from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

start = s.find('<!-- WR-UI-FIX-2026 -->')
if start >= 0:
    end = s.find('</body>', start)
    if end >= 0:
        s = s[:start] + s[end:]

block = r'''<!-- WR-UI-FIX-2026 -->
<style>
/* WR: interfaz limpia, un solo lugar para grupos y sin duplicar tarjetas */
.wr-grupos{max-width:1250px;margin:0 auto 35px;background:#fff;border:1px solid #e2e4e8;border-radius:16px;overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,.08)}
.wr-grupos-head{width:100%;padding:18px 20px;background:#151b27;color:#fff;font-size:20px;font-weight:800;display:flex;align-items:center;justify-content:space-between;cursor:pointer;border:0;text-align:left}
.wr-grupos-head b{color:#f5b800}
.wr-grupos-body{display:none;padding:14px}
.wr-grupos.open .wr-grupos-body{display:block}
.wr-bateria-grupo{border:1px solid #e1e3e6;border-radius:11px;overflow:hidden;margin-bottom:10px;background:#fff}
.wr-bateria-grupo:last-child{margin-bottom:0}
.wr-bateria-grupo>button{width:100%;border:0;background:#f6f7f9;color:#151b27;padding:15px 16px;font-size:17px;font-weight:800;display:flex;justify-content:space-between;align-items:center;cursor:pointer;text-align:left}
.wr-bateria-grupo>button span:last-child{font-size:21px;color:#d71920}
.wr-bateria-items{display:none;padding:12px;grid-template-columns:repeat(4,1fr);gap:12px}
.wr-bateria-grupo.open .wr-bateria-items{display:grid}
.wr-bateria-item{border:1px solid #e3e5e8;border-radius:10px;padding:14px;background:#fff}
.wr-bateria-item strong{display:block;font-size:18px;color:#151b27;margin-bottom:5px}
.wr-bateria-item small{display:block;color:#666;line-height:1.4;margin-bottom:10px}
.wr-bateria-item a{display:block;text-align:center;background:#151b27;color:#fff;text-decoration:none;padding:9px;border-radius:7px;font-weight:700;font-size:13px}
#catalogo-cr-verificado{margin-top:10px;padding-top:35px}
.wr-catalogo-toggle{display:flex;max-width:1100px;margin:0 auto 18px;width:100%;padding:15px 18px;background:#151b27;color:#fff;border:0;border-radius:10px;font-size:17px;font-weight:800;justify-content:space-between;align-items:center;cursor:pointer}
.wr-catalogo-toggle b{color:#f5b800}
.wr-catalogo-verificado-body{display:none;max-width:1100px;margin:auto}
.wr-catalogo-verificado-body.open{display:block}
@media(max-width:900px){.wr-bateria-items{grid-template-columns:repeat(2,1fr)}}
@media(max-width:520px){.wr-bateria-items{grid-template-columns:1fr}.wr-grupos-head{font-size:17px}}

/* Buscador: se despliega, pero no rompe sus controles ni sus eventos */
.buscador-box .wr-buscar-toggle{width:100%;border:0;border-radius:9px;background:#fff;color:#151b27;padding:14px 16px;margin-top:14px;font-size:16px;font-weight:800;display:flex;justify-content:space-between;align-items:center;cursor:pointer}
.buscador-box .formulario.wr-cerrado{display:none!important}
.buscador-box .formulario.wr-abierto{display:grid!important}
.wr-buscar-toggle span:last-child{font-size:20px;color:#d71920}
@media(max-width:650px){.buscador-box .formulario.wr-abierto{grid-template-columns:1fr!important}.buscador-box .boton-buscar{grid-column:auto!important}}
</style>
<script>
(function(){
  function initWR(){
    /* BUSCADOR */
    const box=document.querySelector('.buscador-box');
    const form=box && box.querySelector('.formulario');
    if(box && form && !box.querySelector('.wr-buscar-toggle')){
      const b=document.createElement('button');
      b.type='button'; b.className='wr-buscar-toggle';
      b.innerHTML='<span>Seleccionar vehículo</span><span>⌄</span>';
      form.classList.add('wr-cerrado');
      b.onclick=function(){
        const open=form.classList.toggle('wr-abierto');
        form.classList.toggle('wr-cerrado',!open);
        b.querySelector('span:last-child').textContent=open?'⌃':'⌄';
      };
      form.parentNode.insertBefore(b,form);
    }

    /* GRUPOS: las tarjetas reales se mueven, no se clonan. */
    const productos=document.querySelector('.productos');
    if(productos && !document.querySelector('.wr-grupos')){
      const cards=[...productos.querySelectorAll(':scope > .producto')];
      const data={
        'N-40':cards.filter(c=>(c.querySelector('h3')?.textContent||'').trim()==='N-40'),
        'N-50':cards.filter(c=>(c.querySelector('h3')?.textContent||'').trim()==='N-50'),
        'N-60':cards.filter(c=>(c.querySelector('h3')?.textContent||'').trim()==='N-60'),
        'N-70':cards.filter(c=>(c.querySelector('h3')?.textContent||'').trim()==='N-70')
      };
      const wrap=document.createElement('section'); wrap.className='wr-grupos';
      wrap.innerHTML='<button type="button" class="wr-grupos-head"><span>🔋 <b>Grupos de baterías</b></span><span>⌄</span></button><div class="wr-grupos-body"></div>';
      const body=wrap.querySelector('.wr-grupos-body');
      Object.entries(data).forEach(([name,items])=>{
        const group=document.createElement('div'); group.className='wr-bateria-grupo';
        group.innerHTML='<button type="button"><span>'+name+'</span><span>+</span></button><div class="wr-bateria-items"></div>';
        const itemsBox=group.querySelector('.wr-bateria-items');
        items.forEach(card=>{
          const item=document.createElement('div'); item.className='wr-bateria-item';
          const title=card.querySelector('h3')?.textContent.trim()||name;
          const cca=card.querySelector('.cca')?.textContent.trim()||'CCA: consultar';
          const onclick=card.getAttribute('onclick')||'';
          const m=onclick.match(/location\.href=['\"]([^'\"]+)['\"]/);
          const href=m?m[1]:'#';
          item.innerHTML='<strong>🔋 '+title+'</strong><small>'+cca+'</small><a href="'+href+'">Ver batería</a>';
          itemsBox.appendChild(item);
        });
        group.querySelector('button').onclick=function(){
          group.classList.toggle('open');
          group.querySelector('button span:last-child').textContent=group.classList.contains('open')?'−':'+';
        };
        body.appendChild(group);
      });
      wrap.querySelector('.wr-grupos-head').onclick=function(){
        wrap.classList.toggle('open');
        this.querySelector('span:last-child').textContent=wrap.classList.contains('open')?'⌃':'⌄';
      };
      productos.style.display='none';
      productos.parentNode.insertBefore(wrap,productos);
    }

    /* Catálogo comercial: un solo botón, marcas dentro al abrir. */
    const catalogo=document.getElementById('catalogo-cr-verificado');
    if(catalogo && !catalogo.querySelector('.wr-catalogo-toggle')){
      const title=catalogo.querySelector('.titulo');
      const aviso=catalogo.querySelector('.catalogo-cr-aviso');
      const marcas=[...catalogo.querySelectorAll('.catalogo-cr-marca')];
      const fuentes=catalogo.querySelector('.catalogo-cr-fuentes');
      const body=document.createElement('div'); body.className='wr-catalogo-verificado-body';
      [aviso,...marcas,fuentes].filter(Boolean).forEach(x=>body.appendChild(x));
      const toggle=document.createElement('button'); toggle.type='button'; toggle.className='wr-catalogo-toggle';
      toggle.innerHTML='<span>📦 <b>Catálogo comercial verificado</b></span><span>⌄</span>';
      toggle.onclick=function(){body.classList.toggle('open');toggle.querySelector('span:last-child').textContent=body.classList.contains('open')?'⌃':'⌄'};
      if(title) title.style.display='none';
      catalogo.insertBefore(toggle,catalogo.firstChild);
      catalogo.appendChild(body);
    }
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',initWR); else initWR();
})();
</script>
'''

s = s.replace('</body>', block + '\n</body>', 1)
p.write_text(s, encoding='utf-8')
