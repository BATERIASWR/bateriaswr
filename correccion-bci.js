/* Corrección de equivalencias JIS ↔ BCI
   N-70 / N-80 = BCI 27 para la presentación del buscador.
   Se mantienen intactos los demás datos de la página. */
(function(){
  window.obtenerGrupoBCI = function(bateria){
    const t=String(bateria||"").toUpperCase().replace(/\s+/g,"");

    if(/N70L|N-70L|N70ZL|N-70ZL|N120-7L|NX120-7L/.test(t)) return "BCI 27R";
    if(/N70|N-70|N80|N-80|N70Z|N-70Z|N120|NX120/.test(t)) return "BCI 27";

    if(/N50L|N-50L|N50ZL|N-50ZL/.test(t)) return "BCI 24R";
    if(/N50|N-50|N50Z|N-50Z/.test(t)) return "BCI 24";

    if(/N40L|N-40L/.test(t)) return "BCI 51R";
    if(/N40|N-40|NS40/.test(t)) return "BCI 51/51R";

    if(/NS60/.test(t)) return "BCI 51";
    return "Por confirmar";
  };
})();
