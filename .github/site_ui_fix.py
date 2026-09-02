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
/* Este bloque NO toca el buscador ni el chatbot. Solo añade imagen al catálogo. */
.wr-catalogo-categoria-img{
  width:120px;
  height:90px;
  object-fit:contain;
  display:block;
  margin:0 auto 10px;
}
</style>
<script>
(function(){
  function initWR(){
    const catalogo=document.getElementById('catalogo-cr-verificado');
    if(!catalogo) return;

    const marcas=[...catalogo.querySelectorAll('.catalogo-cr-marca')];
    const images={
      n40:'assets/baterias/n40.svg',
      n50:'assets/baterias/n50.svg',
      n60:'assets/baterias/n60.svg',
      n70:'assets/baterias/n70.svg'
    };

    marcas.forEach(marca=>{
      if(marca.querySelector('.wr-catalogo-categoria-img')) return;
      const texto=(marca.textContent||'').toUpperCase();
      let key='';
      if(/N[- ]?40|NS40|51R/.test(texto)) key='n40';
      else if(/N[- ]?50|N50Z|24R?|42R?|R42/.test(texto)) key='n50';
      else if(/N[- ]?60|NS60/.test(texto)) key='n60';
      else if(/N[- ]?70|N70Z|27F?|NX120/.test(texto)) key='n70';
      if(!key) return;
      const img=document.createElement('img');
      img.className='wr-catalogo-categoria-img';
      img.src=images[key];
      img.alt='Batería '+key.toUpperCase();
      img.loading='lazy';
      marca.insertBefore(img,marca.firstChild);
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',initWR); else initWR();
})();
</script>
'''

s = s.replace('</body>', block + '\n</body>', 1)
p.write_text(s, encoding='utf-8')
