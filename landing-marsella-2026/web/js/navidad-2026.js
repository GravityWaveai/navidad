/* Gravitec by Gravity Wave · Navidad 2026 · selector de nivel, tablas plegables, pedido y texto para el correo.
   Sin dependencias. Cargar con defer o al final del body, después del HTML de la sección. */
(function(){
  var PRODUCTS=[{"id": "arbol", "name": "Árboles de Navidad", "short": "Árboles", "unit": "ud", "unitPl": "uds", "moq": 80, "img": "img/productos/arbol/arbol-navidad-marsella-montado-tu-logo.webp", "tiers": [{"min": 80, "max": 200, "prices": [26.4, 27.0, 28.0]}, {"min": 201, "max": 500, "prices": [22.6, 22.9, 23.3]}, {"min": 501, "max": 1000, "prices": [20.7, 21.0, 21.4]}]}, {"id": "estrellas", "name": "Estrellas de Navidad (Pack 2)", "short": "Estrellas", "unit": "pack", "unitPl": "packs", "moq": 80, "img": "img/productos/estrellas/estrellas-navidad-marsella-tu-logo.webp", "tiers": [{"min": 80, "max": 200, "prices": [15.6, 17.0, 18.5]}, {"min": 201, "max": 500, "prices": [14.8, 15.5, 16.3]}, {"min": 501, "max": 1000, "prices": [14.4, 14.9, 15.9]}]}, {"id": "bolas", "name": "Bola de Navidad (Pack 2)", "short": "Bolas", "unit": "pack", "unitPl": "packs", "moq": 80, "img": "img/productos/bolas/bolas-navidad-marsella-tu-logo.webp", "tiers": [{"min": 80, "max": 200, "prices": [15.6, 17.0, 18.5]}, {"min": 201, "max": 500, "prices": [14.8, 15.5, 16.3]}, {"min": 501, "max": 1000, "prices": [14.4, 14.9, 15.9]}]}, {"id": "portamovil", "name": "Portamóviles", "short": "Portamóviles", "unit": "ud", "unitPl": "uds", "moq": 150, "img": "img/productos/portamovil/portamovil-marsella-3d.webp", "tiers": [{"min": 150, "max": 200, "prices": [12.6, 13.0, 13.6]}, {"min": 201, "max": 500, "prices": [10.3, 10.6, 11.1]}, {"min": 501, "max": 1000, "prices": [9.3, 9.6, 10.0]}]}, {"id": "posavasos", "name": "Posavasos (Pack 4)", "short": "Posavasos", "unit": "pack", "unitPl": "packs", "moq": 80, "img": "img/productos/posavasos/posavasos-marsella-tu-logo.webp", "tiers": [{"min": 80, "max": 200, "prices": [18.2, 19.5, 21.5]}, {"min": 201, "max": 500, "prices": [13.1, 14.0, 14.9]}, {"min": 501, "max": 1000, "prices": [12.5, 13.5, 14.4]}]}];


  /* ---- product configurators (level = image view + price) ---- */
  var LEVELS=[['std','Estándar'],['pack','Packaging personalizado'],['full','Packaging + producto personalizado']];
  function fmtInt(n){ var t=String(Math.round(n)); return t.replace(/\B(?=(\d{3})+(?!\d))/g,'.'); }
  function fmt(n){ var f=Math.round(n*100); var i=Math.floor(f/100), d=f%100; return fmtInt(i)+','+(d<10?'0':'')+d; }
  function tierFor(p,q){ for(var i=0;i<p.tiers.length;i++){ var t=p.tiers[i]; if(q>=t.min&&q<=t.max) return t; } return q<p.tiers[0].min?p.tiers[0]:p.tiers[p.tiers.length-1]; }
  function showView(p,k){ p.querySelectorAll('.stage img').forEach(function(im){ var on=im.getAttribute('data-view')===k; if(on){ im.hidden=false; im.classList.add('fade'); requestAnimationFrame(function(){ requestAnimationFrame(function(){ im.classList.remove('fade'); }); }); } else im.hidden=true; }); }
  PRODUCTS.forEach(function(P){
    var p=document.getElementById('gw-prod-'+P.id); if(!p) return;
    var lvlBtns=p.querySelectorAll('.lvl'), qty=p.querySelector('.cfg-qty input'), outU=p.querySelector('.cfg-out .u'), outT=p.querySelector('.cfg-out .tt'), realBtn=p.querySelector('.cfg-real button');
    var cur='full', q=P.moq, view=(P.id==='portamovil' && p.querySelector('.stage img[data-view=real]'))?'real':'full';
    function render(){
      var t=tierFor(P,q), li={std:0,pack:1,full:2}[cur], unit=t.prices[li], base=t.prices[0];
      lvlBtns.forEach(function(b){ b.setAttribute('aria-pressed',b.getAttribute('data-level')===cur?'true':'false'); });
      var lname={std:'Estándar',pack:'Packaging personalizado',full:'Packaging + producto personalizado'}[cur];
      outU.innerHTML=fmt(unit)+' €<small> /'+P.unit+' · '+lname+'</small>';
      outT.innerHTML='Total <b>'+fmt(unit*q)+' €</b> por '+fmtInt(q)+' '+P.unitPl+' · tramo '+fmtInt(t.min)+'-'+fmtInt(t.max)+(cur==='std'?'':' · +'+fmt(unit-base)+' €/'+P.unit+' frente a estándar')+' · sin IVA ni envío';
      p.querySelectorAll('table.prices tbody tr').forEach(function(tr,i){ tr.classList.toggle('is-hot',P.tiers[i]===t); });
      p.querySelectorAll('table.prices th, table.prices td').forEach(function(c){ c.classList.toggle('is-col',c.cellIndex===li+1); });
      showView(p,view);
    }
    lvlBtns.forEach(function(b){ b.addEventListener('click',function(){ cur=b.getAttribute('data-level'); view=cur; render(); }); });
    if(realBtn){ if(view==='real') realBtn.textContent='Ver el pack del nivel elegido'; realBtn.addEventListener('click',function(){ view=(view==='real')?cur:'real'; realBtn.textContent=(view==='real')?'Ver el pack del nivel elegido':'Ver la pieza sola'; showView(p,view); }); }
    qty.addEventListener('input',function(){ var v=parseInt(qty.value,10); if(v>=P.moq&&v<=1000){ q=v; render(); } });
    qty.addEventListener('change',function(){ var v=parseInt(qty.value,10)||P.moq; q=Math.max(P.moq,Math.min(1000,v)); qty.value=q; render(); });
    P._set=function(level){ cur=level; view=level; render(); };
    Object.defineProperty(P,'_cur',{get:function(){return cur;}}); Object.defineProperty(P,'_q',{get:function(){return q;}});
    render();
  });

  /* ---- order builder (several products, each with level and units) ---- */
  var LNAME={std:'Estándar',pack:'Packaging personalizado',full:'Packaging + producto personalizado'};
  var cart=document.getElementById('gw-cart'), reply=document.getElementById('gw-reply-text');
  var toast=document.getElementById('gw-toast'); var tt;
  function say(m){ toast.textContent=m; toast.classList.add('show'); clearTimeout(tt); tt=setTimeout(function(){ toast.classList.remove('show'); },1800); }
  var state={};
  PRODUCTS.forEach(function(P){
    state[P.id]={on:false,level:'full',q:P.moq};
    var el=document.createElement('div'); el.className='cart-item'; el.id='gw-cart-'+P.id;
    el.innerHTML='<div class="ci-pic"><img src="'+P.img+'" alt=""></div>'
      +'<div class="ci-top"><div class="ci-name">'+P.name+'<small>Mínimo '+fmtInt(P.moq)+' '+P.unitPl+' · desde '+fmt(P.tiers[P.tiers.length-1].prices[0])+' €/'+P.unit+'</small></div><button type="button" class="ci-add">Añadir</button></div>'
      +'<div class="ci-body"><div class="ci-lv" role="group" aria-label="Nivel de personalización de '+P.name+'"></div>'
      +'<div class="ci-row"><label for="gw-cq-'+P.id+'">Unidades ('+P.unitPl+')</label><input id="gw-cq-'+P.id+'" type="number" min="'+P.moq+'" max="1000" step="1" value="'+P.moq+'" inputmode="numeric"><span class="ci-price"></span></div></div>';
    cart.appendChild(el);
    var st=state[P.id], add=el.querySelector('.ci-add'), lv=el.querySelector('.ci-lv'), inp=el.querySelector('input'), pr=el.querySelector('.ci-price');
    add.addEventListener('click',function(){ st.on=!st.on; renderAll(); });
    LEVELS.forEach(function(l){ var b=document.createElement('button'); b.type='button'; b.className='pill'; b.textContent=l[1]; b.setAttribute('data-l',l[0]); b.addEventListener('click',function(){ st.level=l[0]; renderAll(); }); lv.appendChild(b); });
    inp.addEventListener('input',function(){ var v=parseInt(inp.value,10); if(v>=P.moq&&v<=1000){ st.q=v; renderAll(); } });
    inp.addEventListener('change',function(){ var v=parseInt(inp.value,10)||P.moq; st.q=Math.max(P.moq,Math.min(1000,v)); inp.value=st.q; renderAll(); });
    P._el=el; P._pr=pr; P._lv=lv; P._add=add; P._inp=inp;
  });
  function lineFor(P){ var st=state[P.id], t=tierFor(P,st.q), li={std:0,pack:1,full:2}[st.level], unit=t.prices[li]; return {t:t,unit:unit,total:unit*st.q}; }
  function renderAll(){
    var count=0, units=0, total=0, lines=[];
    PRODUCTS.forEach(function(P){
      var st=state[P.id]; P._el.classList.toggle('on',st.on); P._add.textContent=st.on?'Quitar':'Añadir';
      P._lv.querySelectorAll('.pill').forEach(function(b){ b.setAttribute('aria-pressed',b.getAttribute('data-l')===st.level?'true':'false'); });
      var L=lineFor(P);
      P._pr.innerHTML=fmt(L.unit)+' €/'+P.unit+' · <b>'+fmt(L.total)+' €</b>';
      if(st.on){ count++; units+=st.q; total+=L.total; lines.push('- '+P.name+': '+fmtInt(st.q)+' '+P.unitPl+', '+LNAME[st.level].toLowerCase()+' ('+fmt(L.unit)+' €/'+P.unit+', '+fmt(L.total)+' €)'); }
    });
    document.getElementById('gw-out-count').textContent=count;
    document.getElementById('gw-out-units').textContent=fmtInt(units);
    document.getElementById('gw-out-total').textContent=fmt(total)+' €';
    document.getElementById('gw-out-cap').textContent=count?'Sin IVA ni gastos de envío':'Añade productos para ver el total';
    var txt;
    if(count){ txt='Hola,\n\nHe visto el catálogo de regalos de Navidad 2026 en acabado Marsella y me interesa:\n'+lines.join('\n')+'\n\nTotal estimado: '+fmt(total)+' € (sin IVA ni envío).\n\n¿Me pasáis una propuesta cerrada con nuestro logo? Os lo adjunto en vectorial.\n\nGracias,\n[Tu nombre] · [Empresa]'; }
    else { txt='Hola,\n\nHe visto el catálogo de regalos de Navidad 2026 en acabado Marsella y me interesa:\n- [Producto]: [unidades], [nivel de personalización]\n\n¿Me pasáis una propuesta cerrada con nuestro logo?\n\nGracias,\n[Tu nombre] · [Empresa]'; }
    if(!reply.dataset.edited) reply.value=txt;
  }
  reply.addEventListener('input',function(){ reply.dataset.edited='1'; });
  renderAll();
  function copyText(txt,ok){ function fallback(){ reply.focus(); reply.select(); say('Selecciona y copia el texto'); } if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(txt).then(function(){ say(ok); },fallback); } else fallback(); }
  document.getElementById('gw-copy-reply').addEventListener('click',function(){ copyText(reply.value,'Texto copiado. Pégalo en tu respuesta al correo.'); });
  /* product buttons → add that product to the order and jump */
  function addProduct(id,level,q){ PRODUCTS.forEach(function(P){ if(P.id===id){ var st=state[id]; st.on=true; if(level) st.level=level; if(q) { st.q=Math.max(P.moq,Math.min(1000,q)); P._inp.value=st.q; } } }); reply.dataset.edited=''; renderAll(); }
  document.querySelectorAll('[data-choose]').forEach(function(a){ a.addEventListener('click',function(){ /* just navigate */ }); });
  document.querySelectorAll('[data-calc]').forEach(function(b){ b.addEventListener('click',function(){ var id=b.getAttribute('data-calc'); var P=PRODUCTS.filter(function(p){return p.id===id;})[0]; addProduct(id,P&&P._cur,P&&P._q); }); });
  /* collapsible price tables */
  document.querySelectorAll('.pricing-toggle').forEach(function(b){ b.addEventListener('click',function(){ var open=b.getAttribute('aria-expanded')==='true'; b.setAttribute('aria-expanded',open?'false':'true'); var body=document.getElementById(b.getAttribute('aria-controls')); body.hidden=open; b.querySelector('span').textContent=open?'Ver toda la tabla de precios':'Ocultar la tabla de precios'; }); });

  /* ---- copy email ---- */
  document.getElementById('gw-copy-email').addEventListener('click',function(){
    var txt=document.getElementById('gw-email').textContent;
    function fallback(){ var r=document.createRange(); r.selectNodeContents(document.getElementById('gw-email')); var s=window.getSelection(); s.removeAllRanges(); s.addRange(r); say('Selecciona y copia el correo'); }
    if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(txt).then(function(){ say('Correo copiado'); },fallback); } else fallback();
  });
})();
