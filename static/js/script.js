// ── NAV — aparece ao sair do hero fullscreen ──
const nav = document.getElementById('nav');
function updateNav() {
  const past = window.scrollY > 10;
  nav.classList.toggle('visible', past);
  nav.classList.toggle('scrolled', past);
}
window.addEventListener('scroll', updateNav, { passive: true });
updateNav();

// ── MOBILE MENU ──
const toggle = document.getElementById('navToggle');
const menu   = document.getElementById('navMenu');
toggle.addEventListener('click', () => menu.classList.toggle('is-open'));
menu.querySelectorAll('.nav__link').forEach(link => {
  link.addEventListener('click', () => menu.classList.remove('is-open'));
});

// ── HERO VIDEO ──
const video       = document.getElementById('heroVideo');
const placeholder = document.getElementById('videoPlaceholder');
const playBtn     = document.getElementById('heroPlayBtn');
const soundBtn    = document.getElementById('heroSoundBtn');
const playIcon    = document.getElementById('playIcon');
const pauseIcon   = document.getElementById('pauseIcon');
const muteIcon    = document.getElementById('muteIcon');
const soundIcon   = document.getElementById('soundIcon');

if (video) {
  // Esconde placeholder assim que o vídeo começa
  video.addEventListener('playing', () => {
    if (placeholder) placeholder.classList.add('hidden');
    playIcon.style.display  = 'none';
    pauseIcon.style.display = '';
  });

  // Se autoplay for bloqueado pelo browser, mostra ícone de play
  video.addEventListener('pause', () => {
    playIcon.style.display  = '';
    pauseIcon.style.display = 'none';
  });

  // Botão play / pause
  playBtn?.addEventListener('click', () => {
    if (video.paused) {
      video.play();
    } else {
      video.pause();
    }
  });

  // Botão mute / unmute — inicia mudo, usuário ativa som
  soundBtn?.addEventListener('click', () => {
    video.muted = !video.muted;
    muteIcon.style.display  = video.muted ? '' : 'none';
    soundIcon.style.display = video.muted ? 'none' : '';
  });
}

// ── REVEAL ON SCROLL ──
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      setTimeout(
        () => entry.target.classList.add('is-visible'),
        Number(entry.target.dataset.delay || 0)
      );
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.reveal').forEach(el => {
  const siblings = el.parentElement.querySelectorAll('.reveal');
  el.dataset.delay = Array.from(siblings).indexOf(el) * 80;
  revealObserver.observe(el);
});


// ── ATUAÇÃO — cards empilháveis com scale ao rolar ──
(function () {
  const items = document.querySelectorAll('.atuacao__stack-item');
  if (!items.length) return;

  function updateStack() {
    const vh = window.innerHeight;
    items.forEach((item, i) => {
      const next = items[i + 1];
      if (!next) return;

      const nextTop  = next.getBoundingClientRect().top;
      // progress: 0 quando o próximo card está embaixo, 1 quando chega ao topo
      const progress = Math.max(0, Math.min(1, (vh - nextTop) / vh));

      item.style.transform = `scale(${1 - progress * 0.05})`;
      item.style.filter    = `brightness(${1 - progress * 0.22})`;
    });
  }

  window.addEventListener('scroll', updateStack, { passive: true });
  updateStack();
})();

// ── AVALIAÇÕES — carrossel ──
(function () {
  const track = document.getElementById('avaliacoesTrack');
  const prev  = document.getElementById('avalPrev');
  const next  = document.getElementById('avalNext');
  if (!track) return;

  function getStep() {
    const card = track.querySelector('.avaliacoes__card');
    return card ? card.offsetWidth + 20 : 300;
  }

  prev?.addEventListener('click', () => { track.scrollBy({ left: -getStep(), behavior: 'smooth' }); });
  next?.addEventListener('click', () => { track.scrollBy({ left:  getStep(), behavior: 'smooth' }); });
})();

// ── EQUIPE: retrato troca a cada 1.3s (Web Worker — não throttled em aba inativa) ──
(function () {
  const retratos = Array.from(document.querySelectorAll('.equipe__retrato-img'));
  const nomeEl   = document.getElementById('equipeNome');
  if (retratos.length < 2 || !nomeEl) return;

  let current = 0;

  let busy = false;
  function show(i) {
    if (busy) return;
    busy = true;
    const from = retratos[current];
    current = i;
    const to = retratos[current];

    // Próxima já aparece embaixo (z-index menor), atual blurs-out por cima
    from.style.zIndex = '2';
    to.style.zIndex   = '1';
    to.classList.add('is-active');
    nomeEl.textContent = to.dataset.nome;

    from.classList.add('equipe--blur-out');

    setTimeout(() => {
      from.classList.remove('is-active', 'equipe--blur-out');
      from.style.zIndex = '';
      to.style.zIndex   = '';
      busy = false;
    }, 420);
  }

  // Worker inline: browsers não limitam setInterval dentro de workers
  const blob   = new Blob([`
    let t;
    onmessage = e => {
      if (e.data === 'start') { clearInterval(t); t = setInterval(() => postMessage(0), 2000); }
      if (e.data === 'stop')  { clearInterval(t); }
    };
  `], { type: 'application/javascript' });
  const worker = new Worker(URL.createObjectURL(blob));

  worker.onmessage = () => show((current + 1) % retratos.length);
  worker.postMessage('start');
})();

// ── CARROSSEL NOSSA ESTRUTURA (coverflow) ──
(function () {
  // ── Liquid Glass gallery ──
  const gallery   = document.getElementById('estruturaGallery');
  if (!gallery) return;

  const stage = document.getElementById('estrutStage');
  const imgs  = Array.from(stage.querySelectorAll('.estrutura__img'));
  if (!imgs.length) return;

  const edgeLeft  = document.getElementById('edgeLeft');
  const edgeRight = document.getElementById('edgeRight');
  const n         = imgs.length;
  let current     = 0;
  let timer       = null;

  function setEdges(idx) {
    edgeLeft.style.backgroundImage  = `url(${imgs[(idx - 1 + n) % n].src})`;
    edgeRight.style.backgroundImage = `url(${imgs[(idx + 1) % n].src})`;
  }

  function go(toIdx) {
    imgs[current].classList.remove('is-active');
    current = (toIdx + n) % n;
    imgs[current].classList.add('is-active');
    setEdges(current);
  }

  setEdges(0);

  gallery.querySelector('.estrutura__nav--prev')?.addEventListener('click', () => { go(current - 1); restart(); });
  gallery.querySelector('.estrutura__nav--next')?.addEventListener('click', () => { go(current + 1); restart(); });

  function start()   { timer = setInterval(() => go(current + 1), 5000); }
  function stop()    { clearInterval(timer); timer = null; }
  function restart() { stop(); start(); }

  gallery.addEventListener('mouseenter', stop);
  gallery.addEventListener('mouseleave', start);
  start();
})();

// ── FORMULÁRIO DE CONTATO ──
const form = document.getElementById('contactForm');
if (form) {
  form.addEventListener('submit', e => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    btn.textContent       = 'Mensagem enviada';
    btn.style.background  = '#432A35';
    btn.style.borderColor = '#432A35';
    setTimeout(() => {
      btn.textContent       = 'Enviar mensagem';
      btn.style.background  = '';
      btn.style.borderColor = '';
      form.reset();
    }, 3500);
  });
}
