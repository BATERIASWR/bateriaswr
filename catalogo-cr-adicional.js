/* WR-CATALOGO-CR-ADICIONAL-V1
   Registro verificado: RECORD RP45-55B24LS.
   Especificaciones tomadas de ficha técnica del producto.
*/
(function(){
  /* Corrección de equivalencias JIS ↔ BCI usadas por el buscador.
     N-70 y N-80 corresponden a la caja D31 / BCI 27.
     N-70L corresponde a BCI 27R. */
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

  if(typeof catalogoBateriasWR === "undefined") return;
  const b={
    modelo:"RP45-55B24LS",
    marca:"RECORD",
    categoria:"Automotriz",
    tipo:"Libre de mantenimiento",
    grupoJIS:"B24L",
    grupoBCI:"51R",
    voltaje:12,
    capacidadAh:45,
    cca:460,
    rc:80,
    dimensiones:"238 × 129 × 225 mm",
    polaridad:"(-,+)",
    garantiaCasa:"Grupo D",
    fuente:"Ficha técnica RECORD RP45-55B24LS"
  };
  const lista=catalogoBateriasWR["N-60"] || (catalogoBateriasWR["N-60"]=[]);
  if(!lista.some(x=>String(x.modelo).toUpperCase()==="RP45-55B24LS")) lista.push(b);
  if(typeof opcionesBCIWR !== "undefined" && opcionesBCIWR["N-60"]){
    const g=opcionesBCIWR["N-60"].find(x=>x.bci==="BCI 51R");
    if(g && !g.modelos.includes("RP45-55B24LS")) g.modelos.push("RP45-55B24LS");
  }
})();
