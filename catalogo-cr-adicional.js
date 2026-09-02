/* WR-CATALOGO-CR-ADICIONAL-V1
   Registro verificado: RECORD RP45-55B24LS.
   Especificaciones tomadas de ficha técnica del producto.
*/
(function(){
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
