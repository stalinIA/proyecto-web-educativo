/* ═══════════════════════════════════════════════════════════
   SLVERA · app.js
═══════════════════════════════════════════════════════════ */

/* ───────────────────────────────────────────────────────────
   KLAVIYO — CONFIGURACIÓN
   ───────────────────────────────────────────────────────────
   1) COMPANY_ID  → es tu clave pública de Klaviyo (6 caracteres).
                    Ya está puesta: QQ4wL4
   2) LIST_ID     → pega aquí el ID de la lista a la que quieres
                    suscribir los leads. Lo encuentras en Klaviyo:
                    Lists & Segments → (tu lista) → Settings →
                    "List ID"  (ej: "XyAbC2").
   Mientras LIST_ID esté vacío, el formulario funciona en modo
   demostración (muestra éxito y guarda el lead localmente) para
   que puedas verlo. Al pegar tu LIST_ID, queda 100% conectado.
   ─────────────────────────────────────────────────────────── */
const KLAVIYO = {
  COMPANY_ID: 'QQ4wL4',
  LIST_ID: '',                  // ←—— PEGA AQUÍ TU LIST ID DE KLAVIYO
  REVISION: '2024-10-15'
};

/* ── COOKIES ── */
function hasCookie(n){return document.cookie.split(';').some(c=>c.trim().startsWith(n+'='));}
function setCookie(n,v,d){var e=new Date();e.setTime(e.getTime()+(d*864e5));document.cookie=n+'='+v+';expires='+e.toUTCString()+';path=/;SameSite=Lax';}
function acceptCookies(){setCookie('slvera_consent','accepted',395);hideCookie();}
function rejectCookies(){setCookie('slvera_consent','rejected',395);hideCookie();}
function hideCookie(){var b=document.getElementById('cookie');if(b)b.style.display='none';}
if(hasCookie('slvera_consent'))document.addEventListener('DOMContentLoaded',hideCookie);

/* ── MOBILE NAV ── */
function toggleNav(){
  var m=document.getElementById('mnav');
  m.classList.toggle('open');
  document.body.style.overflow=m.classList.contains('open')?'hidden':'';
}

/* ── LEGAL MODALS ── */
function openLegal(p){
  document.querySelectorAll('.modal').forEach(function(m){m.classList.remove('open');});
  var m=document.getElementById('modal-'+p);
  if(m){m.classList.add('open');document.body.style.overflow='hidden';m.scrollTop=0;}
}
function closeLegal(){
  document.querySelectorAll('.modal').forEach(function(m){m.classList.remove('open');});
  document.body.style.overflow='';
}
document.querySelectorAll('.modal').forEach(function(m){
  m.addEventListener('click',function(e){if(e.target===m)closeLegal();});
});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeLegal();});

/* ── FAQ toggle glyph ── */
document.querySelectorAll('#faq details').forEach(function(d){
  d.addEventListener('toggle',function(){
    var t=d.querySelector('.tog');
    if(t)t.textContent=d.open?'+':'+'; // glyph rotates via CSS
  });
});

/* ── SMOOTH SCROLL with nav offset ── */
document.querySelectorAll('a[href^="#"]').forEach(function(a){
  a.addEventListener('click',function(e){
    var href=this.getAttribute('href');
    if(href==='#')return;
    var tgt=document.querySelector(href);
    if(tgt){
      e.preventDefault();
      window.scrollTo({top:tgt.getBoundingClientRect().top+window.scrollY-78,behavior:'smooth'});
      var m=document.getElementById('mnav');
      if(m&&m.classList.contains('open'))toggleNav();
    }
  });
});

/* ── NAV SCROLL EFFECT ── */
var nav=document.getElementById('nav');
window.addEventListener('scroll',function(){
  if(window.scrollY>40)nav.classList.add('scrolled');else nav.classList.remove('scrolled');
},{passive:true});

/* ── REVEAL ON SCROLL ── */
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);}
    });
  },{threshold:0.12,rootMargin:'0px 0px -50px 0px'});
  document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});
}else{
  document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in');});
}

/* ───────────────────────────────────────────────────────────
   LEAD FORM → KLAVIYO
   ─────────────────────────────────────────────────────────── */
(function(){
  var form=document.getElementById('leadForm');
  if(!form)return;
  var btn=document.getElementById('lf-btn');
  var errBox=document.getElementById('lf-err');
  var success=document.getElementById('leadSuccess');
  var btnHTML=btn.innerHTML;

  function showErr(msg){errBox.textContent=msg;errBox.classList.add('err');}
  function clearErr(){errBox.textContent='';errBox.classList.remove('err');}
  function validEmail(e){return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e);}
  function loading(on){
    btn.disabled=on;
    btn.innerHTML=on?'<span class="btn-spin"></span>':btnHTML;
    btn.style.opacity=on?'0.85':'1';
  }
  function done(){
    form.style.display='none';
    success.classList.add('show');
  }

  form.addEventListener('submit',async function(e){
    e.preventDefault();
    clearErr();
    var name=form.name.value.trim();
    var email=form.email.value.trim();
    if(!name){showErr('Por favor escribe tu nombre.');return;}
    if(!validEmail(email)){showErr('Escribe un correo electrónico válido.');return;}

    loading(true);

    // store lead locally as backup
    try{
      var leads=JSON.parse(localStorage.getItem('slvera_leads')||'[]');
      leads.push({name:name,email:email,ts:Date.now()});
      localStorage.setItem('slvera_leads',JSON.stringify(leads));
    }catch(_){}

    // Identify with Klaviyo onsite (analytics) — only once Klaviyo is live-configured
    if(KLAVIYO.LIST_ID){
      try{
        window._klOnsite=window._klOnsite||[];
        window._klOnsite.push(['identify',{'$email':email,'$first_name':name}]);
      }catch(_){}
    }

    // DEMO MODE — no list configured yet
    if(!KLAVIYO.LIST_ID){
      console.warn('[SLVERA] Klaviyo en modo demo: agrega KLAVIYO.LIST_ID en app.js para conectar los leads a tu lista real.');
      setTimeout(function(){loading(false);done();},900);
      return;
    }

    // LIVE — Klaviyo client subscriptions API
    try{
      var res=await fetch('https://a.klaviyo.com/client/subscriptions/?company_id='+encodeURIComponent(KLAVIYO.COMPANY_ID),{
        method:'POST',
        headers:{'Content-Type':'application/json','revision':KLAVIYO.REVISION},
        body:JSON.stringify({
          data:{
            type:'subscription',
            attributes:{
              profile:{data:{type:'profile',attributes:{email:email,first_name:name}}}
            },
            relationships:{list:{data:{type:'list',id:KLAVIYO.LIST_ID}}}
          }
        })
      });
      loading(false);
      if(res.ok||res.status===202){done();}
      else{showErr('No pudimos registrar tu correo ahora mismo. Inténtalo de nuevo o escríbenos a sac@slvera.com.');}
    }catch(err){
      loading(false);
      showErr('Hubo un problema de conexión. Inténtalo de nuevo en unos segundos.');
    }
  });
})();
