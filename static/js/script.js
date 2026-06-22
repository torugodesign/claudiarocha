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
