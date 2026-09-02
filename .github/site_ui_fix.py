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
/* Solo catálogo comercial: no modificar las opciones N40/N50/N60/N70 del sitio principal. */
#catalogo-cr-verificado{margin-top:10px;padding-top:35px}
.wr-catalogo-toggle{display:flex;max-width:1100px;margin:0 auto 18px;width:100%;padding:15px 18px;background:#151b27;color:#fff;border:0;border-radius:10px;font-size:17px;font-weight:800;justify-content:space-between;align-items:center;cursor:pointer}
.wr-catalogo-toggle b{color:#f5b800}
.wr-catalogo-verificado-body{display:none;max-width:1100px;margin:auto}
.wr-catalogo-verificado-body.open{display:block}
.wr-catalogo-marca-bateria{display:flex;align-items:center;gap:18px;padding:16px;margin:10px 0;border:1px solid #e1e3e6;border-radius:12px;background:#fff}
.wr-catalogo-marca-bateria img{width:110px;height:85px;object-fit:contain;flex:0 0 110px}
.wr-catalogo-marca-bateria .wr-cat-info{flex:1}
.wr-catalogo-marca-bateria strong{display:block;font-size:17px;color:#151b27;margin-bottom:5px}
.wr-catalogo-marca-bateria small{display:block;color:#666;line-height:1.4}
@media(max-width:520px){.wr-catalogo-marca-bateria{gap:12px}.wr-catalogo-marca-bateria img{width:82px;height:70px;flex-basis:82px}}
</style>
<script>
(function(){
  function initWR(){
    const catalogo=document.getElementById('catalogo-cr-verificado');
    if(!catalogo || catalogo.querySelector('.wr-catalogo-toggle')) return;

    const title=catalogo.querySelector('.titulo');
    const aviso=catalogo.querySelector('.catalogo-cr-aviso');
    const marcas=[...catalogo.querySelectorAll('.catalogo-cr-marca')];
    const fuentes=catalogo.querySelector('.catalogo-cr-fuentes');

    /* El catálogo conserva exactamente sus productos y datos. Solo añadimos una imagen representativa. */
    const imageByName={
      'N-40':'https://raw.githubusercontent.com/BATERIASWR/bateriaswr/main/assets/baterias/n40.png',
      'N40':'https://raw.githubusercontent.com/BATERIASWR/bateriaswr/main/assets/baterias/n40.png',
      'NS40':'https://raw.githubusercontent.com/BATERIASWR/bateriaswr/main/assets/baterias/n40.png',
      'N-50':'https://raw.githubusercontent.com/BATERIASWR/bateriaswr/main/assets/baterias/n50.png',
      'N50':'https://raw.githubusercontent.com/BATERIASWR/bateriaswr/main/assets/baterias/n50.png',
      '24':'https://raw.githubusercontent.com/BATERIASWR/bateriaswr/main/assets/baterias/n50.png',
      'N-60':'https://raw.githubusercontent.com/BATERIASWR/bateriaswr/main/assets/baterias/n60.png',
      'N60':'https://raw.githubusercontent.com/BATERIASWR/bateriaswr/main/assets/baterias/n60.png',
      'NS60':'https://raw.githubusercontent.com/BATERIASWR/bateriaswr/main/assets/baterias/n60.png',
      'N-70':'https://raw.githubusercontent.com/BATERIASWR/bateriaswr/main/assets/baterias/n70.png',
      'N70':'https://raw.githubusercontent.com/BATERIASWR/bateriaswr/main/assets/baterias/n70.png',
      '27':'https://raw.githubusercontent.com/BATERIASWR/bateriaswr/main/assets/baterias/n70.png'
    };

    marcas.forEach(marca=>{
      const name=(marca.querySelector('h3,.titulo,h4')?.textContent||'').trim();
      const key=Object.keys(imageByName).find(k=>name.toUpperCase().includes(k));
      if(!key || marca.querySelector('.wr-catalogo-marca-bateria')) return;
      const img=document.createElement('img');
      img.src=imageByName[key];
      img.alt='Batería '+key;
      img.loading='lazy';
      img.onerror=function(){this.style.display='none'};
      const wrap=document.createElement('div'); wrap.className='wr-catalogo-marca-bateria';
      const info=document.createElement('div'); info.className='wr-cat-info';
      while(marca.firstChild) info.appendChild(marca.firstChild);
      wrap.appendChild(img); wrap.appendChild(info); marca.appendChild(wrap);
    });

    const body=document.createElement('div'); body.className='wr-catalogo-verificado-body';
    [aviso,...marcas,fuentes].filter(Boolean).forEach(x=>body.appendChild(x));
    const toggle=document.createElement('button'); toggle.type='button'; toggle.className='wr-catalogo-toggle';
    toggle.innerHTML='<span>📦 <b>Catálogo comercial verificado</b></span><span>⌄</span>';
    toggle.onclick=function(){body.classList.toggle('open');toggle.querySelector('span:last-child').textContent=body.classList.contains('open')?'⌃':'⌄'};
    if(title) title.style.display='none';
    catalogo.insertBefore(toggle,catalogo.firstChild);
    catalogo.appendChild(body);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',initWR); else initWR();
})();
</script>
'''

s = s.replace('</body>', block + '\n</body>', 1)
p.write_text(s, encoding='utf-8')
