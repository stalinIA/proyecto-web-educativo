/* ═══════════════════════════════════════════════════════════
   SLVERA · app.js
═══════════════════════════════════════════════════════════ */

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

/* El formulario de leads es gestionado por el embed oficial de Klaviyo (klaviyo-form-QQ4wL4).
   El script de Klaviyo se carga en el <head> vía klaviyo.js y renderiza el form automáticamente. */
