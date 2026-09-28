# A5 Systems Uganda website (afive.cc)

Static website hosted on GitHub Pages. No framework, no build server: plain HTML, one CSS file, one small icon sprite.

## Folder map
- `*.html` - the pages (home, services, products, about, contact, Monitoring, privacy, service-areas-uganda, 404 and the 15 service landing pages). **These are generated** - see below.
- `styles.css` - the only stylesheet (colours are variables at the top).
- `icons.svg` - icon sprite used as `<use href="icons.svg#name">`.
- `images/` - photos (`work-*.webp`, `hero-*.webp`) and the four graphic-only illustrations (`illus-*.svg`, commented inside).
- `tools/build_site.py` - the generator that writes every page, the sitemap and robots.txt.
- `sitemap.xml`, `robots.txt` - search engine files (generated).

## Editing the site (recommended way)
1. Open `tools/build_site.py`. Text, menu links, services, FAQs, phone/email/address and SEO titles/descriptions are all in clearly labelled sections at the top.
2. Change the text, then run: `python3 tools/build_site.py`
3. Commit and push to `main`; GitHub Pages publishes it.

WARNING: the script overwrites the generated .html files, sitemap.xml and robots.txt. Do not hand-edit those pages, or your edits will be lost next run. (For a one-off fix you may edit a page directly, but make the same change in the script.)

The generated HTML contains comments (`<!-- ===== SECTION: ... ===== -->`) marking each part of every page.

## Contact details
Phone/WhatsApp, email and address are defined once in `tools/build_site.py` (BUSINESS section) and used in the header, footer, contact page and search-engine data.

## Images
- Add photos to `images/` as `.webp` (about 1600px wide max, quality ~80) and reference them in the script with width, height and alt text.
- Illustrations (`illus-*.svg`) are shown without captions. Replace the file to change a graphic.

## Adding a page
Add an entry to the services data in the script, run it, and the page, menu/footer links and sitemap entry are created together.

## Search engines
Each page has a unique title, description, canonical URL, hreflang, and JSON-LD data. Submit `https://afive.cc/sitemap.xml` in Google Search Console and Bing Webmaster Tools after each big change.

## Contact form
Uses EmailJS (keys in the contact page script section of the generator).

## Unused legacy files (safe to delete)
`site.css`, `style2.css`, `xindex.html`, the old large `img4`-`img9`, `_img1`, `_kimg3`, `_kkimg2`, `img10`, `iso.jpg`, `Vesa com logo.jpg` and the raw camera photos (`2026*.jpg`, `IMG_*.jpg`) once you no longer need them.
