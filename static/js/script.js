// ── HERO — logo cresce e frase encolhe ao rolar ──
(function () {
  const heroSection = document.getElementById('home');
  const logoImg     = document.querySelector('.hero__logo-overlay-img');
  const headline    = document.querySelector('.hero__headline');
  const scrollHint  = document.querySelector('.hero__scroll-hint');
  if (!heroSection || !logoImg || !headline) return;

  function updateHeroScale() {
    const heroHeight = heroSection.offsetHeight;
    const progress = Math.max(0, Math.min(1, window.scrollY / (heroHeight * 0.7)));

    logoImg.style.transform  = `scale(${1 + progress * 0.6})`;
    headline.style.transform = `scale(${1 - progress * 0.35})`;
    headline.style.opacity   = String(Math.max(0, 1 - progress * 1.3));

    if (scrollHint) scrollHint.style.opacity = String(Math.max(0, 1 - progress * 3));
  }

  window.addEventListener('scroll', updateHeroScale, { passive: true });
  updateHeroScale();
})();

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
toggle.addEventListener('click', () => {
  const isOpen = menu.classList.toggle('is-open');
  toggle.setAttribute('aria-expanded', String(isOpen));
});
menu.querySelectorAll('.nav__link').forEach(link => {
  link.addEventListener('click', () => {
    menu.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  });
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
  // Esconde placeholder assim que o vídeo pode tocar (canplay = mais rápido)
  video.addEventListener('canplay', () => {
    if (placeholder) placeholder.classList.add('hidden');
  });
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

  // Efeito sticky/scale é exclusivo do layout desktop — cards mobile são estáticos
  const mq = window.matchMedia('(max-width: 900px)');
  if (mq.matches) return;

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

  // Respeita prefers-reduced-motion: mantém a primeira foto parada, sem troca automática
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

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
  const gallery = document.getElementById('estruturaGallery');
  if (!gallery) return;

  const stage  = document.getElementById('estrutStage');
  const slides = Array.from(stage.querySelectorAll('.estrutura__slide'));
  if (!slides.length) return;

  const n = slides.length;
  let current = 0;
  let timer   = null;

  // Espaçamento/rotação/escala de cada card conforme a distância do centro
  const STEP_X   = 92;   // % da largura do card por passo lateral — cards com espaço entre si, em leque
  const STEP_ROT = 42;   // graus por passo lateral — tilt pronunciado, como a referência
  const SCALE_DROP = 0.1;
  const MAX_VISIBLE = 2; // 2 cards de cada lado = 5 cards visíveis no total, como a referência

  function render() {
    slides.forEach((slide, i) => {
      let offset = i - current;
      // caminho mais curto no loop (ex: última foto fica "à esquerda" da primeira)
      if (offset > n / 2)  offset -= n;
      if (offset < -n / 2) offset += n;

      const abs = Math.abs(offset);
      const scale   = Math.max(1 - abs * SCALE_DROP, 0.55);
      const opacity = abs > MAX_VISIBLE ? 0 : 1 - (abs / (MAX_VISIBLE + 1)) * 0.35;
      const zIndex  = 100 - abs;

      slide.style.transform =
        `translate(-50%, -50%) translateX(${offset * STEP_X}%) rotateY(${-offset * STEP_ROT}deg) scale(${scale})`;
      slide.style.opacity      = opacity.toFixed(2);
      slide.style.zIndex       = zIndex;
      slide.style.pointerEvents = abs > MAX_VISIBLE ? 'none' : 'auto';
    });
  }

  function go(toIdx) {
    current = (toIdx + n) % n;
    render();
  }

  slides.forEach((slide, i) => slide.addEventListener('click', () => { go(i); restart(); }));

  gallery.querySelector('.estrutura__nav--prev')?.addEventListener('click', () => { go(current - 1); restart(); });
  gallery.querySelector('.estrutura__nav--next')?.addEventListener('click', () => { go(current + 1); restart(); });

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function start()   { if (reduceMotion) return; timer = setInterval(() => go(current + 1), 3500); }
  function stop()    { clearInterval(timer); timer = null; }
  function restart() { stop(); start(); }

  gallery.addEventListener('mouseenter', stop);
  gallery.addEventListener('mouseleave', start);

  render();
  start();
})();

// ── FORMULÁRIO DE CONTATO ──
const form = document.getElementById('contactForm');
if (form) {
  form.addEventListener('submit', e => {
    e.preventDefault();
    const nome      = document.getElementById('nome').value.trim();
    const email     = document.getElementById('email').value.trim();
    const telefone  = document.getElementById('telefone').value.trim();
    const mensagem  = document.getElementById('mensagem').value.trim();

    const texto = [
      `Olá, Cláudia! Vim pelo site e gostaria de agendar uma consulta.`,
      ``,
      `*Nome:* ${nome}`,
      email    ? `*E-mail:* ${email}`    : '',
      telefone ? `*Telefone:* ${telefone}` : '',
      ``,
      `*Mensagem:*`,
      mensagem,
    ].filter(l => l !== null).join('\n');

    const numero = '5516991120865';
    const url    = `https://wa.me/${numero}?text=${encodeURIComponent(texto)}`;
    window.open(url, '_blank');
  });
}
