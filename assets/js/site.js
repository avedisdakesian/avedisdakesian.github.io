// Small bits of behaviour for the site. No libraries.

// Phone menu
document.querySelectorAll('[data-menu]').forEach((header) => {
  const toggle = header.querySelector('button');
  toggle.addEventListener('click', () => {
    const open = header.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
  });
});

// YouTube: show the thumbnail first and only load the player when clicked.
const PLAY_ICON =
  '<svg viewBox="0 0 68 48" width="100%" height="100%" aria-hidden="true">' +
  '<path d="M66.52,7.74c-0.78-2.93-2.49-5.41-5.42-6.19C55.79,.13,34,0,34,0S12.21,.13,6.9,1.55 C3.97,2.33,2.27,4.81,1.48,7.74C0.06,13.05,0,24,0,24s0.06,10.95,1.48,16.26c0.78,2.93,2.49,5.41,5.42,6.19 C12.21,47.87,34,48,34,48s21.79-0.13,27.1-1.55c2.93-0.78,4.64-3.26,5.42-6.19C67.94,34.95,68,24,68,24S67.94,13.05,66.52,7.74z"/>' +
  '<path d="M 45,24 27,14 27,34" fill="#fff"/></svg>';

document.querySelectorAll('.yt[data-yt]').forEach((el) => {
  const id = el.dataset.yt;
  const title = el.dataset.title || 'YouTube video';
  el.innerHTML =
    `<img src="https://i.ytimg.com/vi_webp/${id}/maxresdefault.webp" alt="" loading="lazy" decoding="async">` +
    `<button type="button" aria-label="Play: ${title}">${PLAY_ICON}</button>`;
  el.addEventListener('click', () => {
    el.innerHTML =
      `<iframe src="https://www.youtube.com/embed/${id}?autoplay=1&rel=0&modestbranding=1&playsinline=1&iv_load_policy=3" ` +
      `title="${title}" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen></iframe>`;
  }, { once: true });
});

// Horizontal video row with arrow buttons and edge fades
document.querySelectorAll('[data-scroller]').forEach((box) => {
  const track = box.querySelector('[data-scroller-track]');
  const prev = box.querySelector('[data-scroller-prev]');
  const next = box.querySelector('[data-scroller-next]');
  const step = () => {
    const card = track.firstElementChild;
    const gap = parseFloat(getComputedStyle(track).columnGap) || 0;
    return card ? card.getBoundingClientRect().width + gap : track.clientWidth;
  };
  const update = () => {
    const max = track.scrollWidth - track.clientWidth - 2;
    const scrolled = track.scrollLeft > 2;
    const atEnd = track.scrollLeft >= max;
    box.classList.toggle('is-scrolled', scrolled);
    box.classList.toggle('is-at-end', atEnd);
    prev.hidden = !scrolled;
    next.hidden = atEnd;
  };
  prev.addEventListener('click', () => track.scrollBy({ left: -step() }));
  next.addEventListener('click', () => track.scrollBy({ left: step() }));
  track.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
});
