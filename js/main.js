// Scroll-reveal: the .js class opts into hidden-until-visible styling,
// so content stays visible when JavaScript is disabled.
document.documentElement.classList.add('js');

const observer = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    }
  },
  { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
);

document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

// Podcast player: progressive enhancement over the native <audio> element
const audio = document.getElementById('podcast');
if (audio) {
  const player = audio.closest('.player');
  const toggle = player.querySelector('.player-toggle');
  const seek = player.querySelector('.player-seek');
  const current = player.querySelector('.time-current');
  const total = player.querySelector('.time-total');
  let seeking = false;

  audio.removeAttribute('controls');

  const fmt = (s) => {
    if (!isFinite(s)) return '–:––';
    const m = Math.floor(s / 60);
    return m + ':' + String(Math.floor(s % 60)).padStart(2, '0');
  };

  const showDuration = () => {
    if (isFinite(audio.duration)) {
      seek.max = audio.duration;
      total.textContent = fmt(audio.duration);
    }
  };
  audio.addEventListener('loadedmetadata', showDuration);
  showDuration();

  toggle.addEventListener('click', () => {
    if (audio.paused) audio.play();
    else audio.pause();
  });

  audio.addEventListener('play', () => {
    player.classList.add('playing');
    toggle.setAttribute('aria-label', 'Pause episode');
  });
  audio.addEventListener('pause', () => {
    player.classList.remove('playing');
    toggle.setAttribute('aria-label', 'Play episode');
  });

  audio.addEventListener('timeupdate', () => {
    current.textContent = fmt(audio.currentTime);
    if (!seeking) seek.value = audio.currentTime;
  });

  seek.addEventListener('input', () => {
    seeking = true;
    current.textContent = fmt(Number(seek.value));
  });
  seek.addEventListener('change', () => {
    audio.currentTime = Number(seek.value);
    seeking = false;
  });

  audio.addEventListener('ended', () => {
    audio.currentTime = 0;
    seek.value = 0;
  });
}
