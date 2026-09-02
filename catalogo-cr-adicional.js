/* WR-CATALOGO-CR-ADICIONAL-V2
   Correcciones verificadas de equivalencias y BMW X6 F16 2015.
*/
(function(){
  /* JIS ↔ BCI para tamaños JIS que sí maneja el catálogo WR. */
  window.obtenerGrupoBCI = function(bateria){
    const t=String(bateria||"").toUpperCase().replace(/\s+/g,"");
    if(/N70L|N-70L|N70ZL|N-70ZL/.test(t)) return "BCI 27R";
    if(/N70|N-70|N80|N-80|N70Z|N-70Z|N120|NX120/.test(t)) return "BCI 27";
    if(/N50L|N-50L|N50ZL|N-50ZL/.test(t)) return "BCI 24R";
    if(/N50|N-50|N50Z|N-50Z/.test(t)) return "BCI 24";
    if(/N40L|N-40L/.test(t)) return "BCI 51R";
    if(/N40|N-40|NS40/.test(t)) return "BCI 51/51R";
    if(/NS60/.test(t)) return "BCI 51";
    return "Por confirmar";
  };

  /* BMW X6 F16 2015: no se debe presentar como N-70/N-80.
     Fuentes consultadas muestran H8/L5/BCI 49 AGM como aplicación
     verificada para xDrive35i 3.0L y xDrive50i 4.4L.
     Bosch fitment: 92 Ah, 850 CCA, 354×175×190 mm.
     BMW OEM también lista variantes de 92 Ah y 105 Ah, por lo que
     el tamaño/tipo instalado debe comprobarse antes de vender. */
  const _obtenerRegistroWR = window.obtenerRegistro;
  const _mostrarResultadoWR = window.mostrarResultado;

  window.obtenerRegistro = function(marca,modelo,anio,combustible){
    if(marca==="BMW" && modelo==="X6" && Number(anio)===2015 && (!combustible || combustible==="Gasolina")){
      return {
        desde:2015,
        hasta:2015,
        combustibles:["Gasolina"],
        bateria:"H8 / L5 / BCI 49 AGM",
        nota:"Aplicación verificada para BMW X6 F16 2015. La fuente de fitment muestra 92 Ah, 850 CCA y 354 × 175 × 190 mm. BMW también documenta variantes OEM de 92 Ah y 105 Ah; confirme el tamaño y tipo instalados en el vehículo antes de sustituir.",
        cca:{min:850,rec:850,perfil:"AGM / SUV premium"},
        wrOpciones:[
          "Principal: H8 / L5 / BCI 49 AGM — 92 Ah — 850 CCA — 354 × 175 × 190 mm",
          "Variante OEM documentada por BMW: 105 Ah — confirmar tamaño/tipo instalado",
          "Variante OEM documentada por BMW: 92 Ah AGM — confirmar tamaño/tipo instalado"
        ],
        wrFuente:"Fitment BMW X6 F16 2015 + catálogo OEM BMW"
      };
    }
    return _obtenerRegistroWR ? _obtenerRegistroWR(marca,modelo,anio,combustible) : null;
  };

  window.mostrarResultado = function(marca,modelo,anio,combustible,registro){
    if(marca==="BMW" && modelo==="X6" && Number(anio)===2015 && registro && registro.wrOpciones){
      const mensaje="Hola WRbateriasCr, quiero confirmar la batería para mi BMW X6 2015. Recomendación: H8/L5/BCI 49 AGM. Quiero confirmar capacidad, tipo y dimensiones de la batería instalada.";
      resultado.className="resultado-busqueda mostrar";
      resultado.innerHTML=
        "<h3>🔋 Batería recomendada</h3>"+
        "<p><strong>Vehículo:</strong> BMW X6 2015</p>"+
        "<p><strong>Combustible:</strong> Gasolina</p>"+
        '<div class="bateria-recomendada">H8 / L5 / BCI 49 AGM</div>'+
        '<div class="cca-panel">'+
          '<div class="cca-card"><span>Grupo BCI</span><strong>49</strong><small style="display:block;color:#777;margin-top:5px">H8 / L5</small></div>'+
          '<div class="cca-card"><span>CCA verificado</span><strong>850 CCA</strong></div>'+
          '<div class="cca-card"><span>Capacidad verificada</span><strong>92 Ah</strong></div>'+
          '<div class="cca-card"><span>Tecnología</span><strong style="font-size:17px">AGM</strong></div>'+ 
        '</div>'+ 
        '<p><strong>Opciones documentadas:</strong></p>'+ 
        '<p>• H8 / L5 / BCI 49 AGM — 92 Ah — 850 CCA — 354 × 175 × 190 mm</p>'+ 
        '<p>• BMW también documenta una variante OEM de 105 Ah.</p>'+ 
        '<p class="cca-aviso"><strong>Importante:</strong> el X6 2015 puede llevar distintas configuraciones. No vender solo por año y modelo: confirmar motor, batería instalada, tamaño, tecnología y polaridad antes de instalar.</p>'+ 
        '<p class="nota">La batería BMW debe registrarse en el sistema del vehículo después del reemplazo.</p>'+ 
        '<a class="whatsapp-resultado" href="https://wa.me/50663928294?text='+encodeURIComponent(mensaje)+'" target="_blank" rel="noopener">📲 Confirmar por WhatsApp</a>';
      resultado.scrollIntoView({behavior:"smooth",block:"center"});
      return;
    }
    return _mostrarResultadoWR(marca,modelo,anio,combustible,registro);
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
