# avedisdakesian.github.io

Avedis Dakesian's portfolio, moved off Framer. Plain HTML and CSS with a few lines of JavaScript. No build step: what's in this repo is exactly what the site serves.

## Pages

| Page | File |
| --- | --- |
| Home | `index.html` |
| About | `about/index.html` |
| Services | `services/index.html` |
| Second Caller case study | `second-caller/index.html` |
| Woods Center case study | `woods-center/index.html` |

## Editing

- **Text:** edit the HTML file for that page. The About and Services pages have placeholder text, experience and prices; replace them with your own.
- **CV:** the Download CV button serves `assets/cv/Avedis-Dakesian-CV.pdf`. Replace that file with your CV (keep the same name).
- **Navigation:** the menu links are repeated at the top of each page (`nav__items` for desktop, `phone-nav__menu` for phone).
- **Max width:** `--max-width` at the top of `assets/css/base.css` (1140px, the same as the Framer site). Every page uses it.
- **Colours and spacing:** `assets/css/base.css` (shared), `assets/css/home.css` (home, plus the nav, contact and footer used everywhere), `assets/css/pages.css` (About and Services), `assets/css/case-study.css` (both case studies).
- **Flipping titles under the name:** the list is in `index.html` (`hero__roles`); timing is the `roles` animation in `home.css`. If you add or remove a title, update the keyframe steps too.
- **Images:** `assets/img`. `scripts/optimize-images.py` made them from the full-size originals in `framer-export/assets`.
- **Videos:** `assets/video`.
- **UX Talks (YouTube):** new uploads on the channel are added to the top of the row automatically. The "Update YouTube videos" GitHub Action checks once a week, on Mondays (or run it by hand from the Actions tab). It only adds videos published after the cutoff date in `scripts/update-talks.py`, skips Shorts, and never moves or removes existing cards. To remove or reorder a video, edit the `talks__list` in `index.html`.

Layout switches to the phone version below 1220px wide, the same breakpoint Framer used.

## Preview locally

```sh
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Hosting

GitHub Pages serves the `main` branch (Settings → Pages → Deploy from a branch → `main`, `/ (root)`). The site lives at https://avedisdakesian.github.io. A custom domain can be added on the same settings page.

## framer-export/

A one-time copy of the original Framer pages and their full-size images, made by `scripts/import-framer.sh`. Kept as the source for the images and for reference; the site doesn't load anything from it.
