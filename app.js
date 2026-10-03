/* ═══════════════════════════════════════════════════════════════════
   SLVERA · app.js (v10)
   ═══════════════════════════════════════════════════════════════════ */

/* ┌─────────────────────────────────────────────────────────────────┐
   │  CONFIGURACIÓN — lo único que tienes que tocar                  │
   └─────────────────────────────────────────────────────────────────┘ */
var CONFIG = {
  /* URL de la Aplicación web de Google Apps Script (termina en /exec).
     Paso a paso en automatizacion/LEEME.md                            */
  ENDPOINT: 'PEGAR_AQUI_LA_URL_DE_GOOGLE_APPS_SCRIPT',

  /* Enlace de invitación al grupo de WhatsApp de la lista de espera
     (https://chat.whatsapp.com/...). Mientras diga PENDIENTE, el botón
     del grupo no aparece.                                              */
  GRUPO_WHATSAPP: 'PENDIENTE',

  /* Cuando la comunidad abra: pon true y la URL de inscripción. Los
     botones de "lista de espera" pasarán a llevar ahí.                 */
  COMUNIDAD_ABIERTA: false,
  COMUNIDAD_URL: 'PENDIENTE',

  PRECIO: 39
};

var CODIGOS = [
  ['593','Ecuador','EC'],['57','Colombia','CO'],['51','Perú','PE'],['52','México','MX'],['54','Argentina','AR'],
  ['56','Chile','CL'],['58','Venezuela','VE'],['591','Bolivia','BO'],['595','Paraguay','PY'],['598','Uruguay','UY'],
  ['55','Brasil','BR'],['507','Panamá','PA'],['506','Costa Rica','CR'],['503','El Salvador','SV'],['502','Guatemala','GT'],
  ['504','Honduras','HN'],['505','Nicaragua','NI'],['53','Cuba','CU'],['1809','Rep. Dominicana','DO'],
  ['1','EE. UU. / Canadá','US'],['34','España','ES'],['39','Italia','IT'],['49','Alemania','DE']
];

var PAISES = {
  'Australia': {slug:'australia', code:'AU',
    por:'Estudias y trabajas a la vez: 48 horas por quincena y el salario mínimo más alto de los cinco destinos, A$26,44 la hora.'},
  'Malta':     {slug:'malta', code:'MT',
    por:'Es el arranque ideal para el inglés: cursos cortos, clima mediterráneo, hasta 20 horas de trabajo por semana y transporte gratis.'},
  'Alemania':  {slug:'alemania', code:'DE',
    por:'Si piensas en una carrera completa: universidades públicas casi sin matrícula, €13,90 la hora mínima y transporte de estudiante por €37,80 al mes.'},
  'Dubái':     {slug:'dubai', code:'AE',
    por:'Si buscas un hub internacional: campus de universidades extranjeras y un mercado laboral que no para de crecer.'},
  'España':    {slug:'espana', code:'ES',
    por:'Tu puerta a Europa sin pelearte con el idioma: puedes trabajar hasta 30 horas por semana y en Madrid te mueves con el Abono Joven por €10 al mes.'}
};

function miles(n){return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g,'.');}
function $(s,c){return (c||document).querySelector(s);}
function $$(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s));}
function configurado(v){return typeof v==='string' && v.indexOf('http')===0;}

/* ═══════════ COOKIES ═══════════ */
function getCookie(n){var m=document.cookie.match('(^|;)\\s*'+n+'\\s*=\\s*([^;]+)');return m?m.pop():'';}
function setCookie(n,v,d){var e=new Date();e.setTime(e.getTime()+d*864e5);document.cookie=n+'='+v+';expires='+e.toUTCString()+';path=/;SameSite=Lax';}
function hideCookie(){var b=$('#cookie');if(b)b.hidden=true;}
function acceptCookies(){setCookie('slvera_consent','accepted',395);hideCookie();cargarAnalitica();}
function rejectCookies(){setCookie('slvera_consent','rejected',395);hideCookie();}

/* La analítica SOLO carga con consentimiento expreso. Es lo que dice la
   política de cookies, así que es lo que tiene que hacer el código. */
function cargarAnalitica(){
  if(window.__slvAnalytics) return;
  window.__slvAnalytics=true;
  /* Google Analytics / Meta Pixel van AQUÍ, nunca en el <head>. */
}
function evento(nombre,datos){
  if(window.__slvAnalytics && window.gtag) window.gtag('event',nombre,datos||{});
}

/* ═══════════ NAV MÓVIL ═══════════ */
function toggleNav(forzar){
  var m=$('#mnav'), b=$('#burger');
  if(!m) return;
  var abrir = typeof forzar==='boolean' ? forzar : !m.classList.contains('open');
  m.classList.toggle('open',abrir);
  document.body.classList.toggle('nav-abierto',abrir);
  if(b){b.classList.toggle('x',abrir);b.setAttribute('aria-expanded',abrir);b.setAttribute('aria-label',abrir?'Cerrar menú':'Abrir menú');}
  document.body.style.overflow=abrir?'hidden':'';
}
document.addEventListener('keydown',function(e){if(e.key==='Escape')toggleNav(false);});

/* ═══════════ SCROLL SUAVE CON COMPENSACIÓN DEL NAV ═══════════ */
function irA(sel){
  var t=typeof sel==='string'?$(sel):sel;
  if(!t) return;
  window.scrollTo({top:t.getBoundingClientRect().top+window.scrollY-74,behavior:'smooth'});
}
document.addEventListener('click',function(e){
  var a=e.target.closest('a[href*="#"]');
  if(!a) return;
  var url=new URL(a.href,location.href);
  if(url.pathname!==location.pathname||!url.hash||url.hash==='#') return;
  var t=$(url.hash);
  if(!t) return;
  e.preventDefault();
  toggleNav(false);
  irA(t);
  history.replaceState(null,'',url.hash);
});

/* ═══════════ PROGRESO, NAV Y DOCK ═══════════ */
(function(){
  var barra=$('#progreso'), nav=$('#nav'), dock=$('#dock'), guia=$('#guia'), pedido=false;
  function pintar(){
    pedido=false;
    var y=window.scrollY, h=document.documentElement.scrollHeight-window.innerHeight;
    if(barra) barra.style.transform='scaleX('+(h>0?Math.min(1,y/h):0)+')';
    if(nav) nav.classList.toggle('scrolled',y>30);
    if(dock){
      var enGuia=false;
      if(guia){var r=guia.getBoundingClientRect();enGuia=r.top<window.innerHeight*.9&&r.bottom>0;}
      dock.classList.toggle('up',y>560&&!enGuia);
    }
  }
  function alScroll(){if(!pedido){pedido=true;requestAnimationFrame(pintar);}}
  window.addEventListener('scroll',alScroll,{passive:true});
  window.addEventListener('resize',alScroll,{passive:true});
  pintar();
})();

/* ═══════════ REVEAL + CONTADORES ═══════════ */
(function(){
  var els=$$('.reveal'), cont=$$('[data-count]');
  if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in')});return;}
  var io=new IntersectionObserver(function(en){
    en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}});
  },{threshold:.08,rootMargin:'0px 0px -40px 0px'});
  els.forEach(function(e){io.observe(e)});

  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ioc=new IntersectionObserver(function(en){
    en.forEach(function(x){
      if(!x.isIntersecting) return;
      ioc.unobserve(x.target);
      if(reduce) return;
      var el=x.target, fin=+el.dataset.count, pre=el.dataset.pre||'', post=el.dataset.post||'', t0=null, dur=1300;
      function paso(t){
        if(!t0) t0=t;
        var p=Math.min(1,(t-t0)/dur), e=1-Math.pow(1-p,3);
        el.textContent=pre+miles(fin*e)+post;
        if(p<1) requestAnimationFrame(paso);
      }
      el.textContent=pre+'0'+post;
      requestAnimationFrame(paso);
    });
  },{threshold:.6});
  cont.forEach(function(c){ioc.observe(c)});
})();

/* ═══════════ CALCULADORA ═══════════ */
(function(){
  var rAg=$('#rAg'), rMe=$('#rMe');
  if(!rAg||!rMe) return;
  var msgBase=$('#oMsg').textContent;
  function relleno(r){r.style.setProperty('--p',((r.value-r.min)/(r.max-r.min)*100)+'%');}
  function calcular(){
    var ag=+rAg.value, me=+rMe.value, sv=CONFIG.PRECIO*me, ahorro=ag-sv, max=Math.max(ag,sv);
    $('#oAg').textContent='$'+miles(ag);
    $('#oMe').textContent=me+(me===1?' mes':' meses');
    $('#bAgT').textContent='$'+miles(ag);
    $('#bSvT').textContent='$'+miles(sv);
    $('#bAg').style.width=(ag/max*100)+'%';
    $('#bSv').style.width=(sv/max*100)+'%';
    $('#oAhorro').textContent='$'+miles(Math.max(0,ahorro));
    $('#oMsg').textContent = ahorro>0 ? msgBase :
      'Con estos números la agencia no te sale más cara. Si crees que vas a necesitar tanto acompañamiento, escríbenos y vemos tu caso.';
    relleno(rAg); relleno(rMe);
  }
  rAg.addEventListener('input',calcular);
  rMe.addEventListener('input',calcular);
  calcular();
})();

/* ═══════════ TEST DE DESTINO ═══════════ */
(function(){
  var cuerpo=$('#qBody'), barra=$('#qBar'), num=$('#qNum');
  if(!cuerpo) return;
  var P=[
    {t:'¿Qué es lo que más te mueve a salir?', o:[
      ['Estudiar y trabajar a la vez',{'Australia':3}],
      ['Pagar la matrícula más baja posible',{'Alemania':3}],
      ['No pelearme con otro idioma',{'España':3}],
      ['Estar en un hub internacional',{'Dubái':3}],
      ['Mejorar mi inglés rápido',{'Malta':3}]]},
    {t:'¿Cuánto podrías tener ahorrado para arrancar?', o:[
      ['Menos de $5.000',{'España':2,'Malta':2}],
      ['Entre $5.000 y $15.000',{'Alemania':2,'España':1,'Malta':1}],
      ['Entre $15.000 y $30.000',{'Dubái':2,'Alemania':1,'Australia':1}],
      ['Más de $30.000',{'Australia':2,'Dubái':1}]]},
    {t:'¿Cuánto tiempo te quieres quedar?', o:[
      ['Unos meses, para aprender inglés',{'Malta':2}],
      ['Uno o dos años',{'Australia':1,'Dubái':1,'España':1,'Malta':1}],
      ['Una carrera completa o una maestría',{'Alemania':2,'España':1,'Australia':1,'Dubái':1}]]}
  ];
  var resp=[];

  function pintar(i){
    barra.style.width=((i+1)/P.length*100)+'%';
    num.textContent=(i+1)+' de '+P.length;
    var q=P[i], h='<p class="q-title">'+q.t+'</p><div class="q-opts">';
    q.o.forEach(function(o,k){h+='<button class="q-opt" type="button" data-k="'+k+'"><span class="k">'+String.fromCharCode(65+k)+'</span>'+o[0]+'</button>';});
    h+='</div><div class="q-foot">'+(i>0?'<button class="q-back" type="button">← Pregunta anterior</button>':'<span></span>')+'</div>';
    cuerpo.innerHTML=h;
    $$('.q-opt',cuerpo).forEach(function(b){
      b.addEventListener('click',function(){
        resp[i]=+b.dataset.k;
        if(i<P.length-1) pintar(i+1); else resultado();
      });
    });
    var back=$('.q-back',cuerpo);
    if(back) back.addEventListener('click',function(){pintar(i-1);});
  }

  function resultado(){
    var pts={};
    resp.forEach(function(k,i){var s=P[i].o[k][1];for(var p in s)pts[p]=(pts[p]||0)+s[p];});
    var primero=Object.keys(P[0].o[resp[0]][1])[0];
    var gana=Object.keys(pts).sort(function(a,b){return (pts[b]-pts[a])||(a===primero?-1:b===primero?1:0);})[0];
    var d=PAISES[gana];
    barra.style.width='100%';
    num.textContent='Resultado';
    cuerpo.innerHTML=
      '<div class="q-res">'+
        '<div class="flag">'+d.code+'</div>'+
        '<p class="label" style="justify-content:center;margin-bottom:.6rem">Tu destino para empezar</p>'+
        '<h3>'+gana+'</h3>'+
        '<p class="muted">'+d.por+'</p>'+
        '<div class="btns">'+
          '<button type="button" class="btn btn-primary" id="qGuia">Descargar la guía de '+gana+' <span class="ar">→</span></button>'+
          '<a class="btn btn-ghost" href="destinos/'+d.slug+'.html">Ver '+gana+'</a>'+
        '</div>'+
        '<p class="q-alt">¿No te convence? <button type="button" id="qOtra">Repetir el test</button></p>'+
      '</div>';
    $('#qGuia').addEventListener('click',function(){elegirPais(gana,'test');irA('#guia');});
    $('#qOtra').addEventListener('click',function(){resp=[];pintar(0);});
    evento('quiz_resultado',{destino:gana});
  }

  pintar(0);
})();

/* ═══════════ UTILIDADES DE FORMULARIO ═══════════ */
function llenarCodigos(){
  $$('select[data-codigos]').forEach(function(s){
    if(s.options.length) return;
    CODIGOS.forEach(function(c,i){
      var o=document.createElement('option');
      o.value=c[0]; o.textContent=c[2]+' +'+(c[0]==='1809'?'1 809':c[0]); o.setAttribute('data-pais',c[1]);
      if(i===0) o.selected=true;
      s.appendChild(o);
    });
  });
}
llenarCodigos();

function telLimpio(v){return String(v||'').replace(/\D/g,'').replace(/^0+/,'');}   /* 099… → 99…: el 0 local no va en formato internacional */
function emailOk(v){return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(v||'').trim());}
function marcar(el,mal){if(el)el.classList.toggle('bad',mal);return !mal;}
function utm(n){return new URLSearchParams(location.search).get(n)||'';}
function origen(){
  if(utm('utm_source')) return utm('utm_source')+(utm('utm_campaign')?' · '+utm('utm_campaign'):'');
  if(!document.referrer) return 'Directo';
  try{var h=new URL(document.referrer).hostname.replace(/^www\./,'');return h===location.hostname?'Interno':h;}catch(e){return 'Desconocido';}
}
function dispositivo(){return matchMedia('(max-width:767px)').matches?'Móvil':matchMedia('(max-width:1023px)').matches?'Tablet':'Escritorio';}
function contexto(){
  return {origen:origen(), utm_source:utm('utm_source'), utm_medium:utm('utm_medium'), utm_campaign:utm('utm_campaign'),
          pagina:location.pathname+location.search, dispositivo:dispositivo()};
}
function datosPersona(form){
  var cod=form.codigo;
  return {nombre:form.nombre.value.trim(), email:form.email.value.trim().toLowerCase(),
          codigo:cod.value, pais:cod.options[cod.selectedIndex].getAttribute('data-pais')||'',
          telefono:telLimpio(form.telefono.value), empresa:form.empresa.value};
}
function validarPersona(form, ids){
  var a=marcar($(ids[0]),form.nombre.value.trim().length<2),
      b=marcar($(ids[1]),!emailOk(form.email.value)),
      c=marcar($(ids[2]),telLimpio(form.telefono.value).length<6);
  return a&&b&&c;
}
function limpiarAlEscribir(form){
  ['nombre','email','telefono'].forEach(function(n){
    form[n].addEventListener('input',function(){var w=form[n].closest('.f');if(w)w.classList.remove('bad');});
  });
  form.telefono.addEventListener('input',function(){this.value=this.value.replace(/[^\d\s()-]/g,'');});
}
function enviar(datos){
  if(!configurado(CONFIG.ENDPOINT) || CONFIG.ENDPOINT.indexOf('script.google.com')===-1){
    console.warn('[SLVERA] Falta CONFIG.ENDPOINT en app.js — ver automatizacion/LEEME.md');
    return Promise.reject(new Error('sin-endpoint'));
  }
  /* text/plain evita el preflight CORS que Apps Script no responde */
  return fetch(CONFIG.ENDPOINT,{method:'POST',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify(datos)})
    .then(function(r){return r.json();})
    .then(function(r){if(!r||!r.ok) throw new Error(r&&r.error||'desconocido'); return r;});
}
function logErr(err){ if(!err || err.message!=='sin-endpoint') console.error('[SLVERA]',err); }
function mensajeError(err){
  return err && err.message==='sin-endpoint'
    ? 'El formulario todavía no está conectado. Escríbenos a <a href="mailto:sac@slvera.com">sac@slvera.com</a> y te respondemos.'
    : 'No pudimos enviarlo. Inténtalo otra vez o escríbenos a <a href="mailto:sac@slvera.com">sac@slvera.com</a>.';
}
function ocupado(btn,si,texto){
  if(si){btn.dataset.txt=btn.innerHTML;btn.setAttribute('aria-busy','true');btn.textContent=texto||'Enviando…';}
  else{btn.removeAttribute('aria-busy');if(btn.dataset.txt)btn.innerHTML=btn.dataset.txt;}
}

/* ═══════════ GUÍA GRATIS: FORMULARIO EN 2 PASOS ═══════════ */
var origenTest='', ultimaPersona=null;
function elegirPais(nombre,desde){
  var r=$('input[name=destino][value="'+nombre+'"]');
  if(!r) return;
  r.checked=true;
  marcarPaises();
  if(desde==='test') origenTest='Test: '+nombre;
  if(window.__irPaso) window.__irPaso(2);
}
function marcarPaises(){$$('.pais').forEach(function(l){var i=$('input',l);l.classList.toggle('sel',!!(i&&i.checked));});}

(function(){
  var form=$('#leadForm');
  if(!form) return;
  var pasos=$$('.f-paso',form), barras=$$('.f-steps i'), msg=$('#fMsg'), btn=$('#fBtn'), done=$('#fDone'), actual=1;

  function irPaso(n){
    actual=n;
    pasos.forEach(function(p){p.classList.toggle('on',+p.dataset.paso===n);});
    barras.forEach(function(b,i){b.classList.toggle('on',i<n);});
    msg.classList.remove('on');
    if(n===2) setTimeout(function(){form.nombre.focus({preventScroll:true});},350);
  }
  window.__irPaso=irPaso;

  $$('[data-sig]',form).forEach(function(b){b.addEventListener('click',function(){
    var ok=!!$('input[name=destino]:checked',form);
    $('#errPais').classList.toggle('on',!ok);
    if(ok) irPaso(2);
  });});
  $$('[data-ant]',form).forEach(function(b){b.addEventListener('click',function(){irPaso(1);});});
  $$('input[name=destino]',form).forEach(function(r){r.addEventListener('change',function(){marcarPaises();$('#errPais').classList.remove('on');setTimeout(function(){irPaso(2);},220);});});
  limpiarAlEscribir(form);

  /* ?guia=alemania (desde las páginas de destino) preselecciona el país */
  var q=new URLSearchParams(location.search).get('guia');
  if(q){for(var k in PAISES){if(PAISES[k].slug===q){elegirPais(k);break;}}}

  form.addEventListener('submit',function(e){
    e.preventDefault();
    msg.classList.remove('on');
    if(!validarPersona(form,['#w-nombre','#w-email','#w-tel'])){
      var mal=$('.f.bad input',form); if(mal) mal.focus();
      return;
    }
    var destino=$('input[name=destino]:checked',form).value, persona=datosPersona(form), espera=form.espera.checked;
    var datos=Object.assign({tipo:'guia', destino:destino, espera:espera, test:origenTest}, persona, contexto());
    ocupado(btn,true);
    enviar(datos).then(function(){
      ultimaPersona=persona;
      form.hidden=true; $('.f-steps').hidden=true;
      $('#doneT').textContent='Listo, '+persona.nombre.split(' ')[0]+'. Va en camino.';
      $('#doneP').textContent='Tu guía de '+destino+' llega a '+persona.email+' en unos minutos. Si no la ves, revisa spam o promociones.';
      $('#doneDest').href='destinos/'+PAISES[destino].slug+'.html';
      $('#doneDest').textContent='Ver '+destino;
      $('#doneEspera').hidden=espera;
      $('#doneEsperaOk').hidden=!espera;
      if(espera) mostrarGrupo($('#doneEsperaOk'));
      done.classList.add('on');
      irA(done);
      evento('generate_lead',{destino:destino, lista_espera:espera});
    }).catch(function(err){
      logErr(err);
      msg.innerHTML=mensajeError(err); msg.classList.add('on');
      ocupado(btn,false);
    });
  });

  /* Anotarse en la lista de espera con un toque, con los datos que ya dio */
  var uno=$('#doneEsperaBtn');
  if(uno) uno.addEventListener('click',function(){
    if(!ultimaPersona) return;
    ocupado(uno,true,'Anotando…');
    enviar(Object.assign({tipo:'espera', desde:'Pantalla de la guía'}, ultimaPersona, contexto()))
      .then(function(){ $('#doneEspera').hidden=true; $('#doneEsperaOk').hidden=false; mostrarGrupo($('#doneEsperaOk')); evento('lista_espera',{desde:'guia'}); })
      .catch(function(err){ logErr(err); ocupado(uno,false); alertaSuave($('#doneEspera'),mensajeError(err)); });
  });
})();

function alertaSuave(cont,html){
  var m=$('.f-msg',cont);
  if(!m){m=document.createElement('div');m.className='f-msg';m.setAttribute('role','alert');cont.insertBefore(m,cont.firstChild);}
  m.innerHTML=html; m.classList.add('on');
}
function mostrarGrupo(despuesDe){
  if(!configurado(CONFIG.GRUPO_WHATSAPP) || !despuesDe || $('.grupo-wa',despuesDe.parentNode)) return;
  var a=document.createElement('a');
  a.className='btn btn-wa btn-block grupo-wa'; a.href=CONFIG.GRUPO_WHATSAPP; a.target='_blank'; a.rel='noopener';
  a.textContent='Entrar al grupo de WhatsApp';
  despuesDe.insertAdjacentElement('afterend',a);
}

/* ═══════════ LISTA DE ESPERA (ventana) ═══════════ */
(function(){
  var dlg=$('#espera');
  if(!dlg) return;
  var form=$('#esperaForm'), msg=$('.f-msg',form), btn=$('button[type=submit]',form);

  function abrir(){
    if(CONFIG.COMUNIDAD_ABIERTA && configurado(CONFIG.COMUNIDAD_URL)){ window.open(CONFIG.COMUNIDAD_URL,'_blank','noopener'); return; }
    toggleNav(false);
    if(typeof dlg.showModal==='function') dlg.showModal(); else dlg.setAttribute('open','');
    document.body.style.overflow='hidden';
    setTimeout(function(){var i=$('#eNombre');if(i&&!$('#esperaDone').classList.contains('on'))i.focus();},60);
    evento('lista_espera_abrir');
  }
  function cerrar(){
    if(typeof dlg.close==='function') dlg.close(); else dlg.removeAttribute('open');
  }
  dlg.addEventListener('close',function(){document.body.style.overflow='';});
  dlg.addEventListener('click',function(e){if(e.target===dlg)cerrar();});          /* clic fuera cierra */
  $$('[data-cerrar]',dlg).forEach(function(b){b.addEventListener('click',cerrar);});
  document.addEventListener('click',function(e){
    var b=e.target.closest('[data-espera]');
    if(!b) return;
    e.preventDefault(); abrir();
  });

  limpiarAlEscribir(form);
  form.addEventListener('submit',function(e){
    e.preventDefault();
    msg.classList.remove('on');
    if(!validarPersona(form,['#e-nombre','#e-email','#e-tel'])){
      var mal=$('.f.bad input',form); if(mal) mal.focus();
      return;
    }
    ocupado(btn,true,'Anotando…');
    enviar(Object.assign({tipo:'espera', desde:'Botón lista de espera'}, datosPersona(form), contexto()))
      .then(function(){
        $('#esperaCuerpo').hidden=true;
        $('#esperaDone').classList.add('on');
        var g=$('#esperaGrupo');
        if(g && configurado(CONFIG.GRUPO_WHATSAPP)){g.href=CONFIG.GRUPO_WHATSAPP;g.hidden=false;}
        evento('lista_espera',{desde:'boton'});
      })
      .catch(function(err){
        logErr(err);
        msg.innerHTML=mensajeError(err); msg.classList.add('on');
        ocupado(btn,false);
      });
  });
})();

/* ═══════════ ARRANQUE ═══════════ */
(function(){
  var a=$('#anio'); if(a) a.textContent=new Date().getFullYear();
  var c=getCookie('slvera_consent');
  if(c==='accepted') cargarAnalitica();
  else if(c!=='rejected'){var b=$('#cookie');if(b)setTimeout(function(){b.hidden=false;},1500);}
})();
