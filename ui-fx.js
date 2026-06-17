/* ──────────────────────────────────────────────────────────────────────────
 * TRR UI FX — shared micro-interactions
 * Include after firebase/glass:  <script src="../ui-fx.js"></script>
 * Provides: click ripple, smooth dark-mode fade, entrance stagger,
 *           skeleton helpers, count-up numbers.  Global: window.TRRfx
 * ────────────────────────────────────────────────────────────────────────── */
(function(){
  // ── Click ripple on buttons / cards / nav items ──
  document.addEventListener('click',function(e){
    var t=e.target.closest('button,.portal-card,.nav-item,.btn,.trr-ripple');
    if(!t||t.classList.contains('no-ripple')||t.disabled)return;
    var cs=getComputedStyle(t);
    if(cs.position==='static')t.style.position='relative';
    if(cs.overflow!=='hidden')t.style.overflow='hidden';
    var r=t.getBoundingClientRect();
    var size=Math.max(r.width,r.height);
    var ink=document.createElement('span');
    ink.className='trr-ripple-ink';
    ink.style.width=ink.style.height=size+'px';
    ink.style.left=(e.clientX-r.left-size/2)+'px';
    ink.style.top=(e.clientY-r.top-size/2)+'px';
    t.appendChild(ink);
    setTimeout(function(){if(ink.parentNode)ink.parentNode.removeChild(ink);},650);
  },true);

  // ── Accent theme: apply saved on load, update live via postMessage ──
  function applyAccent(a){
    if(a&&a!=='ocean')document.documentElement.setAttribute('data-accent',a);
    else document.documentElement.removeAttribute('data-accent');
  }
  try{applyAccent(localStorage.getItem('trr_accent')||'');}catch(e){}
  window.addEventListener('message',function(e){
    if(e.data&&e.data.type==='trr_accent')applyAccent(e.data.accent||'');
  });

  // ── Forward Ctrl/⌘+K to parent portal so command palette opens from any page ──
  document.addEventListener('keydown',function(e){
    if((e.ctrlKey||e.metaKey)&&(e.key==='k'||e.key==='K')){
      if(window.self!==window.top){
        e.preventDefault();
        try{window.parent.postMessage({type:'trr_cmdk'},'*');}catch(_){}
      }
    }
  });

  // ── Smooth dark-mode fade: watch <html> class, animate briefly on toggle ──
  var _hadDark=document.documentElement.classList.contains('dark');
  var _themeT=null;
  try{
    new MutationObserver(function(){
      var d=document.documentElement.classList.contains('dark');
      if(d===_hadDark)return;
      _hadDark=d;
      document.documentElement.classList.add('trr-theme-anim');
      clearTimeout(_themeT);
      _themeT=setTimeout(function(){document.documentElement.classList.remove('trr-theme-anim');},480);
    }).observe(document.documentElement,{attributes:true,attributeFilter:['class']});
  }catch(e){}

  // ── Public helpers ──
  window.TRRfx={
    // Stagger-in elements matching selector (or NodeList/array)
    stagger:function(sel,step){
      var els=typeof sel==='string'?document.querySelectorAll(sel):sel;
      step=step||65;
      Array.prototype.forEach.call(els,function(el,i){
        el.classList.remove('trr-enter');
        void el.offsetWidth; // restart animation
        el.style.animationDelay=(i*step)+'ms';
        el.classList.add('trr-enter');
      });
    },
    // Animate a number from 0 (or current) to `to`
    countUp:function(el,to,opt){
      if(!el)return;opt=opt||{};
      var dur=opt.duration||900;
      var dec=opt.decimals||0;
      var prefix=opt.prefix||'';
      var suffix=opt.suffix||'';
      var sep=opt.sep!==false; // thousands separator
      var from=opt.from||0;
      var start=null;
      function fmt(n){
        var s=n.toFixed(dec);
        if(sep){var p=s.split('.');p[0]=p[0].replace(/\B(?=(\d{3})+(?!\d))/g,',');s=p.join('.');}
        return prefix+s+suffix;
      }
      var done=false;
      function finish(){if(done)return;done=true;el.textContent=fmt(to);}
      function step(ts){
        if(done)return;
        if(!start)start=ts;
        var p=Math.min((ts-start)/dur,1);
        var eased=1-Math.pow(1-p,3); // easeOutCubic
        el.textContent=fmt(from+(to-from)*eased);
        if(p<1)requestAnimationFrame(step);else finish();
      }
      requestAnimationFrame(step);
      // Safety net: if rAF never fires (e.g. tab hidden/throttled), land final value.
      setTimeout(finish,dur+120);
    },
    // Render an animated SVG progress ring into el
    ring:function(el,pct,opt){
      if(!el)return;opt=opt||{};
      var size=opt.size||72, sw=opt.stroke||8, r=(size-sw)/2, c=2*Math.PI*r;
      var color=opt.color||'var(--accent)', track=opt.track||'var(--glass-bg-subtle,rgba(0,0,0,.08))';
      pct=Math.max(0,Math.min(100,pct||0));
      var lbl=opt.noLabel?'':'<div class="trr-ring-lbl">'+(opt.label!=null?opt.label:Math.round(pct)+'%')+'</div>';
      el.style.position='relative';el.style.width=size+'px';el.style.height=size+'px';
      el.innerHTML='<svg width="'+size+'" height="'+size+'" viewBox="0 0 '+size+' '+size+'" style="transform:rotate(-90deg)">'+
        '<circle cx="'+size/2+'" cy="'+size/2+'" r="'+r+'" fill="none" stroke="'+track+'" stroke-width="'+sw+'"/>'+
        '<circle class="trr-ring-arc" cx="'+size/2+'" cy="'+size/2+'" r="'+r+'" fill="none" stroke="'+color+'" stroke-width="'+sw+'" stroke-linecap="round" stroke-dasharray="'+c.toFixed(2)+'" stroke-dashoffset="'+c.toFixed(2)+'"/></svg>'+lbl;
      var arc=el.querySelector('.trr-ring-arc');
      var target=c*(1-pct/100);
      requestAnimationFrame(function(){arc.style.transition='stroke-dashoffset .9s cubic-bezier(.22,1,.36,1)';arc.style.strokeDashoffset=target.toFixed(2);});
      setTimeout(function(){if(arc)arc.style.strokeDashoffset=target.toFixed(2);},1000);
    },
    // Render an animated SVG sparkline into el from a numeric array
    sparkline:function(el,data,opt){
      if(!el)return;opt=opt||{};
      if(!data||data.length<2){el.innerHTML='';return;}
      var w=opt.width||90,h=opt.height||26,p=2;
      var min=Math.min.apply(null,data),max=Math.max.apply(null,data),rng=(max-min)||1;
      var step=(w-2*p)/(data.length-1);
      var pts=data.map(function(v,i){return [p+i*step, h-p-((v-min)/rng)*(h-2*p)];});
      var d=pts.map(function(pt,i){return (i?'L':'M')+pt[0].toFixed(1)+' '+pt[1].toFixed(1);}).join(' ');
      var last=pts[pts.length-1];
      var area=d+' L'+last[0].toFixed(1)+' '+(h-p)+' L'+p+' '+(h-p)+' Z';
      var color=opt.color||'var(--accent)';
      var id='sg'+Math.random().toString(36).slice(2,7);
      el.innerHTML='<svg width="'+w+'" height="'+h+'" viewBox="0 0 '+w+' '+h+'">'+
        '<defs><linearGradient id="'+id+'" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="'+color+'" stop-opacity=".28"/><stop offset="1" stop-color="'+color+'" stop-opacity="0"/></linearGradient></defs>'+
        '<path d="'+area+'" fill="url(#'+id+')"/>'+
        '<path class="trr-spark-line" d="'+d+'" fill="none" stroke="'+color+'" stroke-width="'+(opt.stroke||1.6)+'" stroke-linecap="round" stroke-linejoin="round"/>'+
        (opt.dot===false?'':'<circle cx="'+last[0].toFixed(1)+'" cy="'+last[1].toFixed(1)+'" r="2.2" fill="'+color+'"/>')+'</svg>';
      var line=el.querySelector('.trr-spark-line');
      try{var len=line.getTotalLength();line.style.strokeDasharray=len;line.style.strokeDashoffset=len;
        requestAnimationFrame(function(){line.style.transition='stroke-dashoffset 1s ease';line.style.strokeDashoffset=0;});
        setTimeout(function(){if(line)line.style.strokeDashoffset=0;},1100);
      }catch(e){}
    },
    // Stacked toast notification
    toast:function(msg,opt){
      opt=opt||{};
      var type=opt.type||'info';
      var c=document.getElementById('trr-toast-wrap');
      if(!c){c=document.createElement('div');c.id='trr-toast-wrap';c.className='trr-toast-wrap';document.body.appendChild(c);}
      var icons={success:'✓',error:'✕',warn:'!',info:'i'};
      var t=document.createElement('div');
      t.className='trr-toast '+type;
      t.innerHTML='<span class="tt-ic"></span><span class="tt-msg"></span>';
      t.querySelector('.tt-ic').textContent=opt.icon||icons[type]||'i';
      t.querySelector('.tt-msg').textContent=msg;
      c.appendChild(t);
      requestAnimationFrame(function(){t.classList.add('in');});
      var dur=opt.duration||3200;
      function close(){if(t._closed)return;t._closed=true;t.classList.remove('in');t.classList.add('out');setTimeout(function(){if(t.parentNode)t.parentNode.removeChild(t);},320);}
      t._to=setTimeout(close,dur);
      t.addEventListener('click',function(){clearTimeout(t._to);close();});
      return t;
    },
    // Celebratory confetti burst (DOM particles, auto-cleanup)
    confetti:function(opt){
      opt=opt||{};
      if(window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches)return;
      var n=opt.count||90;
      var colors=opt.colors||['#3b82f6','#22d3ee','#34d399','#fbbf24','#fb7185','#a78bfa'];
      var wrap=document.createElement('div');wrap.className='trr-confetti';document.body.appendChild(wrap);
      var ox=opt.x!=null?opt.x:window.innerWidth/2;
      var oy=opt.y!=null?opt.y:window.innerHeight*0.4;
      for(var i=0;i<n;i++){
        var p=document.createElement('i');
        var ang=Math.random()*Math.PI*2;
        var vel=3+Math.random()*8;
        var dx=Math.cos(ang)*vel*26;
        var dy=Math.sin(ang)*vel*26-90;
        p.style.cssText='left:'+ox+'px;top:'+oy+'px;background:'+colors[i%colors.length]+
          ';--dx:'+dx.toFixed(0)+'px;--dy:'+dy.toFixed(0)+'px;--rot:'+(Math.random()*720-360).toFixed(0)+'deg;animation-delay:'+(Math.random()*80).toFixed(0)+'ms';
        if(i%3===0)p.style.borderRadius='50%';
        wrap.appendChild(p);
      }
      setTimeout(function(){if(wrap.parentNode)wrap.parentNode.removeChild(wrap);},1700);
    },
    // Haptic feedback (mobile)
    haptic:function(pattern){try{if(navigator.vibrate)navigator.vibrate(pattern||30);}catch(e){}},
    // Auto count-up every [data-count] element once when visible
    autoCount:function(root){
      var els=(root||document).querySelectorAll('[data-count]');
      Array.prototype.forEach.call(els,function(el){
        if(el._counted)return;el._counted=true;
        var to=parseFloat(el.getAttribute('data-count'))||0;
        TRRfx.countUp(el,to,{
          decimals:parseInt(el.getAttribute('data-decimals')||'0',10),
          prefix:el.getAttribute('data-prefix')||'',
          suffix:el.getAttribute('data-suffix')||'',
          duration:parseInt(el.getAttribute('data-duration')||'900',10)
        });
      });
    }
  };
})();
