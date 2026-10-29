# Design, Pedagogy and Production Plan

**Working title:** *Network Engineer Placements 2027: The Complete Self-Contained Guide* (one book, 12 pillars)
**Short title (spine, running footer):** *NE Placements 2027*
**Audience:** Indian undergraduate and postgraduate students preparing for network-engineering roles at Cisco, Qualcomm, Google, Microsoft, Amazon, Juniper and Arista in the **2027 placement season**.
**Self-contained:** the book is **one PDF**. Every definition, solution, lab output, reference table and mock answer is inside it, so the student never has to search elsewhere (§3.5).
**Target:** **≈ 600 pages**, fully comprehensive; nothing is trimmed for time (§3.1). Readers with less time use the three schedules (6-month full, 3-month, 8-week fast; §3.2) and the Must / Should / Optional navigation tags (§2.15). The 8-week fast plan defines which sections are tagged **Must**; the Must lane is about 260–290 pages, depending on track. The book is PDF first (screen and print) and prints at A4 or at trim size.
**Voice:** plain and sober academic prose (British spelling, "we", "Consider …", terms defined in passing, (i)/(ii) lists, a cause given for every claim). The prose is not asked to be exciting. Readers keep going because of the **design**: the layout, the rhythm of short sections, diagrams on every spread, worked examples, and visible progress against a chosen schedule.

---

## 0. Environment findings (checked 2026-10-29)

| Tool | Status in container | Consequence |
|---|---|---|
| LaTeX (pdflatex/xelatex/lualatex, latexmk, tectonic) | **absent** | A TeX Live install of 2–5 GB would be needed for tcolorbox + TikZ + minted. Ruled out by the "nothing big" constraint. |
| Typst | **absent** | It is a single binary of about 30 MB, so it is the fallback (see §5.6). |
| Pandoc | **3.1.3 present** | Usable as the Markdown → HTML front end, with Lua filters and fenced divs. |
| Chromium | **present** (`/opt/pw-browsers/chromium-1243/chrome-linux64/chrome`) | The PDF engine. |
| Playwright (Node) | **1.63.0 present** (`/opt/node22/lib/node_modules/playwright`) | Drives Chromium headless. The Python binding is not installed and is not needed. |
| Paged.js | not installed. `npm pack pagedjs@0.4.3` worked (≈1 MB). | It gives us paged-media features that Chromium lacks natively. |
| Fonts | **Inter, Inter Display, JetBrains Mono** installed. No Source Serif. | We vendor the remaining OFL fonts into the repository. |
| Graphviz, D2, Mermaid CLI, Inkscape, qpdf, Ghostscript | absent | We generate figures in Python, and use `@hpcc-js/wasm-graphviz` (npm, about 2 MB) for layout only. |
| Python libraries | pypdf 6.17, pypdfium2 5.13, Jinja2 | Enough for post-processing, rendering pages to PNG for review, and QA scripts. matplotlib and Pygments are absent (we install matplotlib if plots are needed; it is moderate in size). |

**Quick tests** (in `/tmp/claude-0/-home-user-paper/67a1eab1-3014-54a1-9e08-cb74ad1814c1/scratchpad/design-test/`):

- (i) `test.html` printed by **plain Chromium** (`build.mjs`). The custom trim size 189 × 246 mm, `@page` margin boxes (running header and folio), callout boxes, inline SVG, a highlighted code block and **PDF bookmarks** (`outline: true`) all worked, and so did a tagged PDF (`tagged: true`). Two things failed: `target-counter()` (so "see p. N" cross-references were blank), and margin notes, which were clipped.
- (ii) The same page via **Paged.js 0.4.3** (`paged.html`, `build2.mjs`). The cross-reference rendered as "longest prefix match (p. 2)", the margin note sat correctly in the outer margin, and bookmarks and fonts (Inter, JetBrains Mono, embedded and subset) carried through. One caveat: a `break-before` written in an inline `style` attribute was ignored, while the same rule in the stylesheet worked. **Rule: all pagination CSS lives in stylesheets, never inline.**

---

## 1. Design system

### 1.1 Page and grid

- **Trim size:** 189 × 246 mm (7.44 × 9.69 in). This is a common technical-trade format, close to the O'Reilly and Head First proportions. It is large enough for a wide text column plus a margin-note column, and it prints cleanly when scaled to A4 at 100 % with white borders.
- **Margins (recto):** top 18 mm, bottom 22 mm, inner 20 mm, outer 52 mm. Verso pages mirror these values (`@page :left`).
- **Text block:** 117 mm wide, so 10 pt serif gives about 66 characters per line. Measure is the main cause of readability, which is why the column is not wider.
- **Margin column:** 40 mm wide, set 6 mm outside the text block. It holds margin notes, mini-definitions, icons and small "see also" pointers.
- **Full-bleed and wide elements:** figures may span text + margin (163 mm, class `.wide`). Chapter openers and cheat sheets use the full page.
- **Baseline:** 10/15 pt body, with a 5 pt sub-grid. All vertical spacing is a multiple of 5 pt (5, 10, 15, 20, 30), which keeps facing pages aligned.
- **Columns:** a 6-column grid across the text block for tables and cheat sheets; cheat-sheet pages use 2 or 3 columns.

### 1.2 Typefaces (all SIL Open Font Licence)

| Role | Face | Setting |
|---|---|---|
| Body text | **Source Serif 4** (Adobe, OFL), with optical sizes | 10 pt / 15 pt, `font-optical-sizing: auto`, old-style figures in running text, lining figures in tables |
| Headings, UI, callout labels, figure labels, tables | **Inter** and **Inter Display** (OFL; already installed) | H1 30 pt Inter Display ExtraBold; H2 15 pt Inter Bold; H3 11 pt Inter SemiBold; labels 7.5 pt Inter Bold, uppercase, +8 % tracking |
| Code, CLI, packet fields, addresses | **JetBrains Mono** (OFL; already installed) | 8.5 pt / 12.5 pt, no ligatures (`font-variant-ligatures: none`), so that `!=` and `->` show exactly what the student must type |
| Mathematics (complexity, queueing, probability) | **KaTeX** fonts (MIT), rendered at build time to HTML+MathML, so no JavaScript runs at print time | |
| Hand-drawn accent (sparingly, in analogies and zine-style margin sketches) | **Caveat** (OFL) | Only in "Analogy" boxes and in arrow annotations on figures. At most one phrase per figure. |

Fonts are vendored into `assets/fonts/` with their licence files. Chromium subsets them on embedding, so file size stays small.

### 1.3 Colour palette

**Neutral base** (shared by every pillar):

| Token | Hex | Use |
|---|---|---|
| `--paper` | `#FBFAF7` | page background on screen (warm off-white; pure white on the print build) |
| `--ink` | `#1C2230` | body text (contrast 15.2:1 on paper) |
| `--muted` | `#5C6370` | captions, margin notes, folios (5.8:1) |
| `--rule` | `#D9D6CE` | hairlines, table rules |
| `--code-bg` | `#F3F1EC` | code and CLI blocks |
| `--hl` | `#FFF3BF` | highlighter marks inside figures and code (the "look here" colour) |

**One accent per pillar.** Every accent passes ≥ 4.5:1 against white, so it can be used for text such as running headers and labels. The tint (10 %) is used for callout backgrounds and the mid tint (22 %) for figure fills and tab blocks.

| # | Pillar | Accent | Tint 10 % | Tint 22 % | Contrast on white |
|---|---|---|---|---|---|
| 1 | Data Structures & Algorithms | `#3B5BDB` cobalt | `#EBEFFB` | `#D4DBF7` | 5.7 |
| 2 | Programming (C & Python) | `#6741D9` violet | `#F0ECFB` | `#DED5F7` | 6.3 |
| 3 | Computer Networks fundamentals | `#0B7285` deep cyan | `#E7F1F3` | `#C9E0E4` | 5.6 |
| 4 | Routing & Switching | `#087F5B` teal | `#E6F2EF` | `#C9E3DB` | 5.0 |
| 5 | Data Centre & Cloud | `#1864AB` steel blue | `#E8F0F7` | `#CCDDED` | 6.1 |
| 6 | Wireless | `#C2255C` raspberry | `#F9E9EF` | `#F2CFDB` | 5.7 |
| 7 | Operating Systems & Sockets | `#C2410C` vermilion | `#F9ECE7` | `#F2D5CA` | 5.2 |
| 8 | Linux Tools | `#4D7C0F` olive | `#EDF2E7` | `#D8E2CA` | 5.0 |
| 9 | Security | `#B91C1C` crimson | `#F8E8E8` | `#F0CDCD` | 6.5 |
| 10 | Automation | `#9C36B5` grape | `#F5EBF8` | `#E9D3EF` | 5.8 |
| 11 | Troubleshooting | `#A16207` ochre | `#F6EFE6` | `#EADCC8` | 4.9 |
| 12 | Supporting Subjects | `#495057` slate | `#EDEEEE` | `#D7D8DA` | 8.2 |

With 12 pillars, some hues are inevitably close (1/5, 7/11). Colour is therefore **never the only identifier**. Every pillar also has (i) a number on the page-edge tab, (ii) its own pillar icon, and (iii) its name in the running header. This also covers colour-blind readers and greyscale printing.

**Semantic colours for learning elements** stay fixed across pillars, so that a "Trap" looks the same everywhere. They are kept apart from the pillar accents by shape and icon as well as hue:

| Element | Stroke | Fill |
|---|---|---|
| Trap / pitfall | `#B91C1C` | `#FDECEC`, plus a hatched left edge so it still reads in greyscale |
| Check Yourself | `#495057` | `#F1F3F5` |
| Try It (lab) | `#1C2230` | `--code-bg`, framed like a terminal window |
| Interview Lens | `#1C2230` | white, with a 1 pt ink border and company pills |
| Big Idea, Worked Example, Analogy | pillar accent | pillar tint |

Implementation: CSS custom properties are set per pillar on `<section class="pillar" data-pillar="4">`, and every component reads `var(--accent)` and `var(--tint)`. A pillar can therefore be re-coloured in one line.

### 1.4 Iconography

- **UI and learning-element icons:** **Lucide** (ISC licence; a fork of Feather). We use a 1.5 px stroke at 24 px, scaled to 12–14 pt, as vendored SVG sprites (`assets/icons/sprite.svg`, used via `<use href>`). Fixed mapping: Big Idea = `lightbulb`; Analogy = `shapes`; Worked Example = `pencil-ruler`; Trap = `triangle-alert`; Interview Lens = `briefcase`; Try It = `terminal`; Check Yourself = `circle-check`; Cheat Sheet = `scroll-text`; Deep Dive = `layers`; Historical note = `history`.
- **Pillar icons** (12, custom-drawn on the same 24 px grid with 1.5 px strokes, so they match Lucide): a binary-tree node (DSA), braces (Programming), a stacked-layers glyph (CN), a router disc (R&S), a rack (DC & Cloud), radiating arcs (Wireless), a kernel ring (OS), a prompt `>_` (Linux), a shield (Security), cog plus arrows (Automation), a stethoscope or probe (Troubleshooting), sigma (Supporting).
- **Network device glyphs:** our own flat set (§4.1), not vendor icon libraries. This avoids trademark and licence problems with vendor-branded icons, and it gives a cleaner look than the classic skeuomorphic router "hockey puck".
- **No emoji** anywhere in the book. Emoji render inconsistently across fonts and devices, and they clash with the sober voice.

### 1.5 Chapter (pillar) opener

The opener is a two-page spread, verso + recto, and is always forced to start on a verso (`break-before: left`).

- **Verso (full-bleed image page):** the page is filled with the pillar tint. On it sits one large "hero diagram" drawn in the figure language (for example, R&S shows a packet's path across three routers, with its forwarding-table lookup magnified). The diagram is deliberately beautiful and relevant. It is the 3Blue1Brown-style hook, it is printed again in small at the point in the chapter where it is explained, and a cross-reference points there.
- **Recto:**
  - (i) a large pillar number ("04") in Inter Display Thin at 120 pt, in the accent;
  - (ii) the pillar title in Inter Display ExtraBold at 30 pt;
  - (iii) a two-sentence scope statement in the supervisor voice ("In this pillar we study how a router decides where to send a packet, and how switches learn where hosts are. We begin with …");
  - (iv) **"What you will be able to do"**, a list of 4–6 outcomes written as interview-testable actions;
  - (v) **"Prerequisites"**, given as pillar and section links;
  - (vi) **"Interview weight"**, a small bar row per company family (Software / Infra / Wireless tracks; see §3.2) at three levels (light/medium/heavy). This is editorial guidance and is stated as such, not as data;
  - (vii) the **progress tracker**, a strip of section numbers with empty check-circles for the student to tick (§2.12). Each section shows its navigation tag (§2.15), so the Must sections form a visible fast lane through the strip;
  - (viii) estimated study time per lane (for example "Must 9 h · +Should 14 h · Full 20 h"), and where each schedule places this pillar ("8-week: Days 15–21 · 3-month: Weeks 4–5 · 6-month: Weeks 7–9").

### 1.6 Running elements and margin notes

- **Running header** (in the `@top` margin box): verso shows the pillar number and name; recto shows the current section title via `string-set`. Both are in Inter Medium 7.5 pt, accent colour.
- **Folio:** at the bottom outer corner, Inter SemiBold 8 pt, muted.
- **Page-edge tab:** a 6 × 22 mm accent block bleeding off the outer edge. Its vertical position steps down by pillar number, so the closed book (in print) and the thumbnail sidebar (in a PDF viewer) show where each pillar starts. It is implemented as a positioned element in the page margin box.
- **Margin notes**, of four kinds, all set in Inter 8 pt/11 pt, muted:
  - (i) **definition-in-passing**: the term in bold, then a one-line gloss. Its counterpart is the glossary entry, and a glossary-sync script checks the two agree;
  - (ii) **cross-reference** ("→ §4.3, p. 211");
  - (iii) **command-equivalent** ("Junos: `show route`", next to IOS text);
  - (iv) **tiny sketch**: a 40 mm SVG thumbnail. There are at most two margin notes per page, which keeps the margin from becoming noise.

### 1.7 Body typography details

- Headings are numbered (`4.3.2`), because a reference book is navigated by number.
- Paragraph spacing: 0 between paragraphs, with a 1 em indent (book convention). Space appears only around components, which makes components stand out.
- Lists use (i)/(ii) inline for short enumerations within prose, as the voice requires. Displayed lists use en-dash bullets, or numerals for procedures.
- Tables: horizontal rules only (booktabs style), an Inter 8.5 pt header row in small caps-like uppercase, monospace for values such as addresses and ports, zebra striping in the pillar 10 % tint only for tables longer than 8 rows.
- Inline code in JetBrains Mono at 92 % size on a faint `--code-bg` pill.
- Widows and orphans are controlled with `widows: 2; orphans: 2`; components and figures carry `break-inside: avoid`.

---

## 2. Recurring learning elements

General rules. (i) Each element has a fixed icon, label and frame, so the reader recognises it in under a second. (ii) Labels are nouns, not exclamations ("Trap", not "Watch out!"), which keeps them consistent with the voice. (iii) Every element is a Pandoc fenced div (`::: trap`), so authors never write layout code. (iv) Frequencies are enforced by a lint script (§5.5), which counts elements per section.

| # | Element | Purpose | Visual treatment | Frequency |
|---|---|---|---|---|
| 2.1 | **Big Idea** | The one sentence that the section exists to teach. Stated plainly, with its cause. | Accent left bar of 3 pt, tint background, lightbulb icon, label in accent. Body text 11 pt (one step larger than body). | Exactly 1 per major section (H2); about 4–8 per pillar |
| 2.2 | **Analogy** | Gives a physical intuition before the formal model, followed by a sentence saying **where the analogy fails**, which keeps rigour. Example: "a switch's MAC table is a post-room pigeonhole list … it fails because …". | Tint background with a dashed accent border, a small hand-drawn sketch in Caveat or SVG on the right, `shapes` icon. | At most 1 per H2; used only where a concept is new to most readers |
| 2.3 | **Worked Example** | A full solution with numbered steps, showing the reasoning ("We first note … hence …") and ending with a one-line **Result**. These are the backbone of the book. | Full-width frame: accent header strip with label + example number ("Worked Example 4.7: Longest-prefix match on a 5-entry table"), numbered steps in a narrow left gutter, result in a tinted footer row. It may break across pages, with a "continued" label. | 2–4 per H2; about 15–30 per pillar |
| 2.4 | **Trap** | A misconception or interview pitfall, with the *reason* it is wrong. | Crimson hatched left edge, pale red fill, triangle icon. The format is fixed: "*Claim:* … *Why it is wrong:* … *Correct statement:* …". | 1–3 per H2 |
| 2.5 | **Interview Lens** | How the topic is examined: typical question forms, what a strong answer contains, follow-ups the interviewer is likely to ask, and the depth expected per track. | White box, 1 pt ink border, briefcase icon. **Company pills** sit in the top-right (Inter 6.5 pt, uppercase, outlined, monochrome text tags such as `CISCO` `JUNIPER` `ARISTA`; no logos, so no trademark-artwork use). An optional **track pill** (`SW` / `INFRA` / `WLAN`) and a level pill (`OA`, `TECH-1`, `TECH-2`, `HM`). We describe question *types* and themes, not claimed verbatim leaked questions, and phrase them as "commonly reported" with no fabricated specifics. | 1 per H2, ending each major section |
| 2.6 | **Try It** (lab) | A reproducible hands-on exercise on free tools: Linux namespaces, `ip`, `tcpdump`, Wireshark, FRRouting, Containerlab, GNS3, Python sockets, Scapy, Cisco Packet Tracer where a free licence exists. Each gives the goal, setup, commands, expected output and "what to observe". | Terminal-window frame: a dark title bar `#1C2230` with three neutral dots and a lab ID (`LAB 4.2`), a `--code-bg` body, the prompt in muted and commands in ink bold. Expected output is set at a lighter weight. A clock pill gives estimated time. **Every lab prints its full expected output and a "What you should notice" paragraph**, so a reader without a laptop to hand can still do it on paper ("paper lab"). | 1–2 per H2; about 6–12 per pillar |
| 2.7 | **Check Yourself** | 3–5 short questions at the end of each H2: recall, application, and one "why" question. Answers are at the back of the pillar, so the reader cannot see them at a glance. | Slate frame, check icon, questions numbered `4.3-1`…; each has a difficulty marker. | 1 per H2 |
| 2.8 | **Deep Dive** (optional) | Rigour beyond interview needs (RFC detail, proofs, kernel internals). Skippable, and marked as such. | Indented, 9 pt, a thin accent rule above and below, `layers` icon, label "Deep Dive (may be skipped on first reading)". | 0–2 per pillar section |
| 2.9 | **Cheat Sheet** page | One- or two-page summary at the end of each pillar: tables, key commands, formulae, port numbers, decision flowcharts, plus "top 10 interview checks". Designed to be printed and pinned. | Full-page, 3-column grid, pillar-tint header band, small type (8 pt), heavy use of tables and mini-diagrams. A perforation-style dashed border signals "tear me out". | 1 per pillar (12) + a 2-page master cheat sheet in the back matter |
| 2.10 | **Difficulty markers** | Shows the reader what to tackle on a first pass. | Three small filled or open squares after a heading or question: ■□□ Foundation, ■■□ Core (most interviews), ■■■ Stretch (FAANG-level or niche roles). Squares rather than stars, because stars read as ratings. | On every H2 heading, every exercise and every Check Yourself question |
| 2.11 | **Track markers** | Folded into the navigation tag (§2.15), which shows the tag for each track. | — | — |
| 2.12 | **Progress tracker** | Visible progress, which is a strong reason to keep reading. Three levels: (i) the pillar opener strip of section check-circles; (ii) a two-page **master tracker** in the front matter (grid of 12 pillars × sections, with tick boxes and dates); (iii) a thin progress bar in the footer of each page showing position within the pillar (an accent line whose length is the fraction of pillar pages so far, computed at build time). | — | Continuous |
| 2.13 | **Margin definition** | Defines terms in passing without breaking the flow of the prose (see §1.6). | Margin note with the term in bold. | As needed, at most 2 per page |
| 2.14 | **"Where this shows up"** strip | One line at the end of each Worked Example linking it to a real system (for example, "Linux `fib_trie`, Cisco CEF"). It ties theory to products without hype. | Muted 8 pt line with an arrow glyph. | Optional, on most worked examples |
| 2.15 | **Navigation tag (Must / Should / Optional)** | A **navigation aid only**. It does not change content: every section is written to the same full standard. Each tag maps to a schedule: **Must** means the section is scheduled in the **8-week fast plan** for that track; **Should** means it is added by the **3-month plan**; **Optional** means only the **6-month full plan** covers it (depth, rarer topics, Deep Dives). The 8-week plan is written first, and the tags are generated from it (§5.5 checks the two agree). | A compact badge beside the heading in Inter Bold 6.5 pt: `● MUST`, `◐ SHOULD`, `○ OPTIONAL`. The shape carries the meaning, so it reads in greyscale. Tags are per track and shown for all three: `SW ● INFRA ● WLAN ◐`. A thin solid rule down the outer page edge marks Must pages, so a fast-plan reader flicking through sees the fast lane at a glance. Contents, pillar openers and the master tracker repeat the badges. | Every H2 and H3 (lint-enforced) |
| 2.16 | **Schedule tag** | Ties each section to the schedules, so the reader always knows where today's pages are. | A small muted pill under the heading: `8w D17 · 3m W5 · 6m W9 · 50 min`. | Every H2 |
| 2.17 | **Short note** | A key fact or rule stated in 2–5 lines, for fast revision. It supplements the full explanation and never replaces it. | No frame; Inter SemiBold lead-in phrase, then body text. | Freely |
| 2.18 | **Weekly checkpoint** | A two-page self-test: 10 questions + 1 timed coding problem, with **full solutions on the following page** and a score band ("8–10: continue; 5–7: re-read the listed Must sections on the next buffer day; under 5: move to the next longer schedule if time allows"). The checkpoints follow the 8-week plan (8 of them); the 3-month and 6-month plans reuse them at the points listed in their tables. | Full-page component in slate with a scoring grid and tick boxes. | 8, grouped in Part 0 "The Plans" |

**Rhythm target per spread:** at least one figure, table or component on every two-page spread. The cause is visual pacing: no reader should face more than about 1,000 words of unbroken text. The lint script flags any spread in which more than 85 % of the area is plain prose.

**End-of-pillar sequence (fixed):** Summary in 8–12 bullets → Cheat Sheet → Interview Question Bank (20–40 questions, tagged by company, track, priority and difficulty, **each with a full model answer**) → Check Yourself answers (complete, not hints) → "Sources" (a short list of RFC numbers and standard texts the content was checked against, for credibility only; the reader is told it is not needed for preparation).

---

## 3. Book structure

### 3.1 Page budget (≈ 600 pages, fully comprehensive)

| Part | Pages |
|---|---|
| Front matter, including Part 0 "The Plans" | 38 |
| Pillars 1–12 | 500 |
| Back matter | 68 |
| **Total** | **≈ 606** |

The book is not trimmed for any schedule. The schedules choose a path through it; the content stays complete. How we keep a comprehensive book easy to move through without making it thin:

- (i) every section is self-contained and starts with its Big Idea, so a reader can enter at any tagged section;
- (ii) one canonical explanation per concept, cross-referenced and never repeated, which keeps the page count honest;
- (iii) comparison tables replace comparative prose (for example OSPF vs IS-IS, TCP vs QUIC);
- (iv) Optional material is gathered at the end of each H2 as Deep Dives, so Must readers can skip it cleanly;
- (v) page budgets live in `book.yml`, and the build reports pages against budget per pillar.

### 3.2 Front matter and Part 0 "The Plans" (≈ 38 pp.)

1. Half-title, title (*Network Engineer Placements 2027*), copyright (font and icon licences, trademark notice for vendor names, "information correct as of" date), dedication.
2. **Contents**: two pages, with the pillar colour tabs and Must/Should/Optional badges echoed in the list.
3. **How to use this book** (4 pp.): the anatomy of a page, with an annotated sample spread labelling every learning element; how difficulty markers and navigation tags work; how to choose a schedule; how to do labs on a laptop or on paper; a note on vendor syntax (Cisco IOS/IOS XE is primary, with Junos, EOS and Linux equivalents in the margin).
4. **Three study tracks** (2 pp.), each shown as a "metro map" diagram (stations are sections, lines are tracks):
   - **Software track** (SDE-networking, Google/Microsoft/Amazon SDE, Cisco/Juniper/Arista software engineer): DSA ■■■, Programming ■■■, OS & sockets ■■■, CN ■■■, Automation ■■, Linux ■■, DC & Cloud ■■, R&S ■, Security ■, Troubleshooting ■, Wireless □.
   - **Infrastructure track** (network engineer, Amazon NDE, Google network engineer, Microsoft Azure networking, Cisco TAC/CX, Juniper/Arista systems and customer engineers): CN ■■■, R&S ■■■, DC & Cloud ■■■, Troubleshooting ■■■, Linux ■■■, Security ■■, Automation ■■, DSA ■■, Programming ■■, OS ■, Wireless ■.
   - **Wireless track** (Qualcomm WLAN/modem software, Cisco wireless, embedded networking): Wireless ■■■, Programming (C emphasis) ■■■, OS & sockets ■■■, CN ■■■, Supporting subjects (signals, probability) ■■■, DSA ■■, Linux ■■, Security ■, R&S ■.
5. **Choosing a schedule** (1 p.): a one-page decision chart ("How many weeks until your first OA?") leading to one of three schedules.

   | Schedule | Covers | Hours per week | Daily budget | Total hours |
   |---|---|---|---|---|
   | **6-month full plan** (26 weeks) | the whole book: Must + Should + Optional | ≈ 16 h | Mon–Fri 2 h, Sat 4 h, Sun 2 h | ≈ 420 h |
   | **3-month plan** (13 weeks) | Must + Should | ≈ 23 h | Mon–Fri 3 h, Sat 5 h, Sun 3 h | ≈ 300 h |
   | **8-week fast plan** (56 days) | Must only; this plan *defines* the Must tag | ≈ 30 h | Mon–Fri 4 h, Sat 6 h, Sun 4 h | ≈ 240 h |

   The budgets have a stated cause. We assume about 30–35 minutes per page of dense technical text with worked examples, plus a fixed allowance for daily coding practice, mocks and revision. For example, the Must lane is about 270 pages, which takes about 150 h, and practice adds about 90 h, giving about 240 h over 8 weeks. Sunday is lighter in every plan and includes a buffer slot, because a plan with no slack fails at the first missed day.

6. **The 8-week fast plan, day by day** (4 pp.; defines the Must tag). Every day uses the same 4-hour template on weekdays, which we print once at the head of the plan:

   - Block A, 60 min: **DSA practice**, 2 OA-style problems. It is daily, because coding fluency is built by spaced, repeated practice rather than by a single block.
   - Block B, 120 min: **today's Must sections** (the pages carrying today's `8w Dn` tag).
   - Block C, 40 min: **Try It lab or worked-example redo** (labs can be done on paper from the printed output).
   - Block D, 20 min: **recall**, covering yesterday's Check Yourself and 10 rapid-fire questions.

   Saturdays add a 2-hour block (a second topic, or a mock). Sundays hold the weekly checkpoint, the cheat sheet for the week and a 1-hour buffer for anything missed.

   The common plan is track-neutral except in Week 6, which has three variants. Pillar numbers follow §3.3.

   | Day | Main block (Must sections) | DSA block (P1) | Lab / practice |
   |---|---|---|---|
   | **Week 1** | **Foundations: networks, C, Python** | | |
   | D1 Mon | How to use this book; P3 layering and encapsulation | Complexity, Big-O | Lab setup (or paper-lab orientation) |
   | D2 Tue | P3 Ethernet, MAC addresses, ARP | Arrays, two pointers | Capture ARP with `tcpdump` |
   | D3 Wed | P3 IPv4 addressing, subnetting I | Strings | 20 subnetting drills |
   | D4 Thu | P3 subnetting II (VLSM, summarisation), IPv6 essentials | Hashing I | 20 more drills |
   | D5 Fri | P2 C: pointers, memory, structs, endianness | Hashing II | Parse an IPv4 header in C |
   | D6 Sat | P2 Python: data model, `struct`, `socket`; P3 ICMP, ping, traceroute | Bit manipulation (masks) | Traceroute walkthrough |
   | D7 Sun | **Checkpoint 1**; P3 cheat sheet (part 1); buffer | — | — |
   | **Week 2** | **Transport and applications** | | |
   | D8 | P3 UDP and the TCP header; three-way handshake | Linked lists I | Handshake in `tcpdump` |
   | D9 | P3 TCP state machine, flow control | Linked lists II | `ss -tan` states |
   | D10 | P3 congestion control | Stacks and queues | Worked-example redo |
   | D11 | P3 DNS, DHCP | Monotonic stack, queues | `dig` trace |
   | D12 | P3 HTTP and TLS overview; "what happens when you type a URL" | Sliding window | Explain-aloud drill |
   | D13 Sat | P2 C pitfalls and output prediction; P8 shell, `ip`, `ss` | Binary search | 20 C-output MCQs |
   | D14 Sun | **Checkpoint 2**; P3 cheat sheet; rapid fire (P3); buffer | — | — |
   | **Week 3** | **Routing and switching** | | |
   | D15 | P4 MAC learning, VLANs, trunks | Trees I (traversals) | VLAN lab (Linux bridge) |
   | D16 | P4 STP/RSTP, LACP | Trees II (BST) | STP worked example |
   | D17 | P4 static routing, longest-prefix match, AD vs metric | Tries (links to LPM) | LPM by hand |
   | D18 | P4 OSPF I (neighbours, LSDB, SPF) | Heaps I | — |
   | D19 | P4 OSPF II (areas, LSA types) | Heaps II (top-k) | FRR OSPF lab |
   | D20 Sat | P4 BGP (attributes, best path), FHRP, ACL and NAT | Graphs I (BFS/DFS) | FRR BGP lab |
   | D21 Sun | **Checkpoint 3**; **Mock OA 1** (90 min); P4 cheat sheet | — | — |
   | **Week 4** | **Operating systems, sockets, Linux** | | |
   | D22 | P7 processes and threads | Graphs II (Dijkstra; links to OSPF) | — |
   | D23 | P7 scheduling, synchronisation | Graphs III (Bellman–Ford, topological sort) | Race-condition demo |
   | D24 | P7 memory, paging, virtual memory | Union-find, MST | — |
   | D25 | P7 interrupts and the network receive path | Recursion, backtracking | — |
   | D26 | P7 sockets API; `select`/`poll`/`epoll` | Intervals, sorting | TCP echo server in C and Python |
   | D27 Sat | P8 `tcpdump`, `nftables`, `tc`, namespaces, `strace` | DP I | Namespace two-host lab |
   | D28 Sun | **Checkpoint 4**; P7 and P8 cheat sheets; buffer | — | — |
   | **Week 5** | **Data centre, cloud, security** | | |
   | D29 | P5 Clos/spine-leaf, ECMP | DP II | ECMP hash worked example |
   | D30 | P5 VXLAN/EVPN, overlay vs underlay | DP III | — |
   | D31 | P5 cloud VPC constructs, load balancers | Greedy | — |
   | D32 | P9 cryptography essentials, TLS handshake | Matrix and grid problems | `openssl s_client` |
   | D33 | P9 IPsec, firewalls, AAA | Mixed set | — |
   | D34 Sat | P9 attacks and mitigations; P12 probability, Little's law | Timed mixed set | **Mock OA 2** |
   | D35 Sun | **Checkpoint 5**; P5 and P9 cheat sheets; buffer | — | — |
   | **Week 6** | **Track week** (variants below) | Mixed timed sets daily | |
   | D36–D40 | **SW:** P1 hard patterns, P2 concurrency, P7 `epoll` and zero-copy, P10 basics. **INFRA:** P10 Python for networks, NETCONF/YANG, Ansible; P5 cloud networking; P4 BGP policy. **WLAN:** P6 RF and dB, 802.11 MAC, association and security, Wi-Fi 6/7, cellular overview. | | Track labs |
   | D41 Sat | Non-WLAN tracks: P6 802.11 essentials. WLAN track: P10 basics. | Timed set | — |
   | D42 Sun | **Checkpoint 6**; **Mock OA 3**; track cheat sheets | — | — |
   | **Week 7** | **Troubleshooting and gaps** | | |
   | D43 | P11 method; case files 1–4 | Re-solve wrong answers | — |
   | D44 | P11 case files 5–8 (Layer 2) | Re-solve | — |
   | D45 | P11 case files 9–12 (routing) | Re-solve | — |
   | D46 | P11 case files 13–16 (transport, DNS, applications) | Re-solve | — |
   | D47 | P11 case files 17–20 (hosts, Linux); P12 aptitude basics | Re-solve | — |
   | D48 Sat | **Mock OA 4**; re-read every Trap box in Must sections | — | — |
   | D49 Sun | **Checkpoint 7**; buffer | — | — |
   | **Week 8** | **Revision and company preparation** | | |
   | D50 | Cheat sheets P1–P3; rapid fire 1–35; target company playbook | 1 timed problem | — |
   | D51 | Cheat sheets P4–P6; rapid fire 36–70 | 1 timed problem | — |
   | D52 | Cheat sheets P7–P9; rapid fire 71–100 | 1 timed problem | — |
   | D53 | Cheat sheets P10–P12; all Interview Lens boxes for the track | 1 timed problem | — |
   | D54 | Playbook final checklist; behavioural answers; explain 10 Big Ideas aloud | — | — |
   | D55 Sat | Simulated interview day: re-take the worst mock; two mock technical rounds with a friend, using the Interview Lens follow-ups | — | — |
   | D56 Sun | **Checkpoint 8** (final); light review; rest | — | — |

   **Weekly checkpoints.** The Sunday checkpoint pages (§2.18) carry the score bands and name the exact Must sections to re-read for each wrong answer, so remediation needs no searching.

7. **The 3-month plan** (2 pp.): 13 weeks covering Must + Should for the chosen track, laid out as a week-by-week table with daily themes. The rhythm is the same as the 8-week plan, with 3-hour weekdays (DSA 50 min · sections 90 min · lab/recall 40 min). Weeks 1–10 run in the same pillar order as the 8-week plan, at about 1.6 times its span, so Should sections fall next to their Must neighbours. Checkpoints 1–8 come at the ends of weeks 2, 3, 5, 6, 7, 8, 10 and 12. Mock OAs are in weeks 5, 8, 10 and 11. Weeks 11–13 are troubleshooting case files, cheat sheets, rapid fire and playbooks. Week 13 has a lighter final 3 days.
8. **The 6-month full plan** (2 pp.): 26 weeks covering the whole book, including Optional sections and Deep Dives, with 2-hour weekdays. The phases are:
   - (i) weeks 1–4: P12 supporting subjects and P2 programming foundations first, because they underpin everything else when there is time;
   - (ii) weeks 5–18: pillars in track order, at about 1.5 weeks per pillar, with DSA running daily throughout;
   - (iii) weeks 19–22: projects (a small routing lab portfolio, or a socket server, for the CV) and Deep Dives;
   - (iv) weeks 23–26: mocks, rapid fire, playbooks and the same final-fortnight sequence as Week 8 above.

   Checkpoints are reused at the end of each phase-(ii) pillar block.
9. **Master progress tracker** (2 pp.): a grid of 12 pillars × sections showing Must/Should/Optional badges, with tick boxes and three columns of dates (one per schedule), plus a 56-day strip for the fast plan.
10. **Weekly checkpoints 1–8** (16 pp.; §2.18), grouped here, with solutions on the facing or following page.
11. **Lab setup** (3 pp.): one Ubuntu VM or WSL2 install, Containerlab + FRRouting, Wireshark, Python 3.12, GCC. Exact commands and pinned versions are printed in full. Every lab runs on an 8 GB laptop with free software, and every lab can also be done on paper from its printed output.
12. **Notation and conventions** (1 p.): typography of commands, placeholders `<iface>`, hex/binary notation, units (SI and IEC: kB vs KiB, and Mb/s vs MB/s, which are distinguished because students often confuse them).

### 3.3 The 12 pillars (≈ 500 pp.)

| # | Pillar | Pages | Notes on emphasis |
|---|---|---|---|
| 1 | Data Structures & Algorithms | 56 | Complexity; arrays and strings; hashing; linked lists; stacks and queues; trees, tries (routing tables); heaps (timers, Dijkstra); graphs (BFS/DFS, Dijkstra, Bellman–Ford, MST, which are tied directly to routing protocols); DP; bit manipulation (masks and subnets). Each topic has OA-pattern problem sets. |
| 2 | Programming: C & Python | 50 | C memory model, pointers, structs and packing (packet headers), bitfields, endianness, `htons`; undefined behaviour; Python data model, generators, `struct`, `socket`, `asyncio`; testing. |
| 3 | Computer Networks fundamentals | 54 | Layering and encapsulation; Ethernet; ARP; IPv4/IPv6 and subnetting (with a heavy worked-example density); ICMP; UDP/TCP (state machine, flow and congestion control); DNS, DHCP, HTTP/TLS overview; "what happens when you type a URL". |
| 4 | Routing & Switching | 56 | VLANs, STP/RSTP, LACP; MAC learning; static routing, LPM, administrative distance; RIP (historical), OSPF, IS-IS, BGP (path attributes, best-path); FHRP; MPLS basics; ACL/NAT; QoS basics; config in IOS with Junos/EOS equivalents. |
| 5 | Data Centre & Cloud | 40 | Clos/spine-leaf; ECMP; VXLAN/EVPN; overlay vs underlay; load balancers; AWS/Azure/GCP VPC constructs; SDN; Kubernetes networking basics. |
| 6 | Wireless | 44 | RF basics, dB/dBm, path loss; 802.11 PHY/MAC (CSMA/CA, DCF/EDCA, RTS/CTS); association and security (WPA2/3, 802.1X); Wi-Fi 6/7 features (OFDMA, MU-MIMO, MLO); cellular overview (LTE/5G architecture) for Qualcomm. |
| 7 | Operating Systems & Sockets | 44 | Processes, threads, scheduling, synchronisation, memory and paging; interrupts and the network stack path (NIC → driver → softirq → socket buffer); Berkeley sockets; `select`/`poll`/`epoll`; zero-copy. |
| 8 | Linux Tools | 34 | Shell, `ip`, `ss`, `tcpdump`, `iptables`/`nftables`, `tc`, namespaces, `strace`, `perf` basics, `/proc` and `/sys`, systemd, log reading. |
| 9 | Security | 40 | CIA; cryptography basics; TLS handshake; IPsec; firewalls; AAA/RADIUS/TACACS+; common attacks (ARP spoofing, SYN flood, DNS poisoning, VLAN hopping) and mitigations. |
| 10 | Automation | 34 | Python for networks (Netmiko, NAPALM), NETCONF/YANG, RESTCONF, gNMI/streaming telemetry, Ansible, Git, CI for network config, idempotence. |
| 11 | Troubleshooting | 34 | Method (bottom-up, divide-and-conquer, follow-the-packet); 20 scenario case files ("users on VLAN 20 cannot reach the gateway"), each with symptoms → hypotheses → tests → root cause; written as a Worked Example chain. |
| 12 | Supporting Subjects | 30 | Discrete mathematics, probability (for queueing and wireless), basic queueing (M/M/1, Little's law), digital logic and computer architecture (caches, which matter for lookup performance), signals for wireless, aptitude basics for OAs. |

Every pillar follows the same internal template: Opener spread → numbered H2 sections (each: difficulty and track markers → prose → figures → Worked Examples → Trap(s) → Try It → Interview Lens → Check Yourself) → Summary → Cheat Sheet → Question Bank → Answers → Sources.

**Must lane per track** (pages tagged Must, derived from the 8-week plan; indicative targets that the build checks against the tags):

| Pillar | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | Pillar pages | + cheat sheets and checkpoints | Lane total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SW | 40 | 30 | 36 | 14 | 12 | 4 | 32 | 16 | 12 | 12 | 10 | 6 | 224 | 34 | ≈ 258 |
| INFRA | 30 | 20 | 40 | 40 | 24 | 6 | 14 | 20 | 16 | 16 | 20 | 6 | 252 | 34 | ≈ 286 |
| WLAN | 30 | 34 | 34 | 12 | 6 | 34 | 30 | 14 | 12 | 4 | 10 | 16 | 236 | 34 | ≈ 270 |

### 3.4 Back matter (≈ 68 pp.)

1. **Mock Online Assessments** (20 pp.): 4 timed mocks, each 2 coding problems + 20 MCQs (networking, OS, C output prediction, aptitude). There are 2 Software-flavoured mocks, 1 Infra and 1 Wireless. The format mimics typical OA platforms in structure only; no proprietary questions are reproduced. Full solutions with complexity analysis and marking guidance follow.
2. **100-question Rapid Fire** (8 pp.): one-line questions with answers on the facing page in a two-column grid, grouped by pillar and colour-tabbed. It is designed for the last week before an interview.
3. **Company Playbooks** (21 pp., 3 pp. each for Cisco, Qualcomm, Google, Microsoft, Amazon, Juniper, Arista). Each uses a fixed layout:
   - (i) typical network-related role families and which track maps to each (for example: Amazon Network Development Engineer → Infra; Qualcomm WLAN software → Wireless; Arista Systems Test / Software Engineer → Software + Infra);
   - (ii) the commonly reported process shape (OA → technical rounds → managerial/behavioural), described generally;
   - (iii) a topic heat-map against the 12 pillars (editorial judgement, labelled as such);
   - (iv) the company's own technology to be aware of (Cisco IOS XE/NX-OS, Junos, Arista EOS, Azure/AWS/GCP networking, Qualcomm Wi-Fi/5G platforms);
   - (v) behavioural framing where well known (for example, Amazon's Leadership Principles, which are public);
   - (vi) a 2-week final-preparation checklist;
   - (vii) a **"verify before you apply"** box. Processes change, so the playbook dates its information and points to official careers pages.

   Company names are used nominatively. There are no logos, and no use of brand colours in the company pages, which would imply endorsement.
4. **Answers to selected end-of-pillar exercises** (if they do not fit in the pillars).
5. **Glossary** (8 pp.): about 450 terms. Each gives the term, its expansion, a one-line definition, and the page of first definition. It is generated from the same YAML file that supplies the margin definitions (§5.3).
6. **Index** (8 pp.): two-column, generated (§5.3). Main entries in bold give the defining page.
7. **Port and protocol quick reference, RFC map, IOS ↔ Junos ↔ EOS command table** (3 pp.).

### 3.5 Self-contained by design

The reader must never need another resource to prepare. This is a requirement on content and on QA, not only a promise in the preface. Rules:

- (i) **No required external links.** Body text contains no URLs. URLs appear only in "Sources" lists (for credibility) and in the playbooks' dated "verify before you apply" box, printed as plain text. A lint check enforces this (§5.5).
- (ii) **Every exercise has a full solution in the book**: Check Yourself, question banks, checkpoints, mock OAs and rapid fire. Solutions are full model answers with reasoning, not hints. The lint fails any exercise without a linked solution.
- (iii) **Every lab prints its expected output** and a "What you should notice" paragraph, so labs can be done without a computer.
- (iv) **Reference appendices** in the back matter replace web look-ups: ports and protocols; the IOS ↔ Junos ↔ EOS ↔ Linux command map; C and Python syntax quick references; the complexity table for common data structures; powers of two and the subnet table; ASCII/hex; `tcpdump` and Wireshark filter syntax; `git` and `vim` survival sheets.
- (v) **The glossary covers every term** used anywhere in the book (sync-checked, §5.5).
- (vi) **Behavioural preparation** is included: a STAR-method section with worked answers, inside the company playbooks part, so the student does not need a separate HR guide.

These additions take about 12 extra pages within the back matter budget, by drawing the reference tables compactly.

---

## 4. Figure language specification

The aim is one visual language across about 600 figures. A reader who has learnt the shapes in Pillar 3 can read any figure in Pillar 11 without a legend. This is the main thing that makes the book feel designed rather than assembled.

### 4.1 Element shapes (drawn at 1:1 on a 4 px grid, strokes at 1.5 px for objects, 1 px for links)

| Object | Glyph | Notes |
|---|---|---|
| **Router** | Circle, Ø 32 px, with four short arrows (two in, two out) in a cross. Pillar-neutral: stroke `#1C2230`, fill white. | Label below, in Inter 8 pt bold (`R1`). The interface labels (`Gi0/0`, `.1`) sit at the link ends in JetBrains Mono 7 pt. |
| **Switch (L2)** | Rounded rectangle 44 × 24 px (r = 4), with two parallel opposing arrows inside. | |
| **L3 switch** | Switch rectangle with a small router circle badge at the top-right. | |
| **Host / server** | Host: monitor outline (rectangle 28 × 20 + stand). Server: tall rectangle 22 × 32 with 3 horizontal slots. | |
| **Access point** | Small rounded rectangle 28 × 14 with 3 concentric arcs above. | |
| **Wireless client** | Phone/laptop outline with 1 arc. | |
| **Firewall** | Rectangle with a brick pattern (three rows of offset strokes). | |
| **Load balancer** | Rectangle with one arrow splitting into three. | |
| **Cloud / Internet / WAN** | One standard cloud path (5 arcs), dashed stroke, fill `#F1F3F5`. | It is reserved for "a network we do not show in detail", never decoration. |
| **Subnet / broadcast domain / VLAN / area / AS** | Rounded rectangle (r = 10) with a 10–15 % fill. The label sits in the top-left corner in Inter 7.5 pt uppercase. | Fills use the categorical domain palette: `#E7F5FF`, `#EBFBEE`, `#FFF4E6`, `#F3F0FF`, `#FFF0F6`, `#F8F9FA`. |
| **Process / thread / kernel object** | Rectangle with a square-cornered header band. | Used in OS and socket figures. |
| **Packet / frame** | Envelope-free "segmented bar": a horizontal bar split into header fields, coloured by layer (§4.3). | The same glyph scales from a 30 px icon on a topology link to a full-width header diagram, so one shape means "packet" everywhere. |

All glyphs live in one SVG `<symbol>` library (`figures/lib/glyphs.svg`), so a change propagates to every figure.

### 4.2 Lines and arrows

| Meaning | Style |
|---|---|
| Physical link (copper or fibre) | solid 1 px ink |
| Link speed emphasis | 2 px solid (≥ 40 G) |
| Wireless link | dashed 1 px with 4/3 dash plus small arcs |
| Logical adjacency (OSPF neighbour, BGP session, tunnel) | dashed 1.25 px in the protocol's layer colour, with round caps |
| Tunnel / overlay (VXLAN, GRE, IPsec) | double line (pipe) with a 6 % fill of the layer colour |
| Packet movement | solid 1.5 px with a filled triangular arrowhead (6 px) in the layer colour; sequence numbers in circled numerals ①②③ in Inter Bold 7 pt |
| Control-plane message | dotted 1.25 px with an open arrowhead |
| Data flow in code and OS diagrams | solid 1 px ink, filled arrowhead |
| Pointer (memory diagrams) | 1 px ink from a filled dot (origin) to an arrowhead, routed orthogonally |
| Failure | a red `#B91C1C` cross (2 px) on the link, plus a "✕" label |
| Highlight | `--hl` yellow underlay behind the element, never a change of the element's own colour |

Arrowheads are one shared SVG marker set. Lines are orthogonal or straight; Bézier curves are used only for wireless arcs and hand-annotated callouts.

### 4.3 OSI/TCP-IP layer colour coding (used inside figures only)

| Layer | Colour | Typical use |
|---|---|---|
| L1 Physical | `#795548` brown | bit streams, cables, RF |
| L2 Data link | `#2B8A3E` green | Ethernet header, MAC addresses, VLAN tag, STP BPDU |
| L3 Network | `#1971C2` blue | IP header, routes, OSPF/BGP |
| L4 Transport | `#D9480F` orange | TCP/UDP header, ports |
| L5–7 Application (merged) | `#862E9C` purple | HTTP, DNS, payload |
| Payload / data | `#ADB5BD` grey | user data |

L2 and L4 fall just below 4.5:1 for small text, so layer colours are used for **fills and strokes only**, and labels are always in ink. The colours stay the same in every pillar, independent of the pillar accent. A figure in the Security pillar still draws the IP header blue, which is the cause of cross-pillar readability. For greyscale print each layer also carries a fill pattern at 10 % opacity (none, dots, diagonal, cross-hatch, horizontal).

### 4.4 Typography inside figures

- Labels: Inter 8 pt, ink. Secondary labels: Inter 7 pt, muted. Addresses, fields and commands: JetBrains Mono 7 pt.
- Figure numbers and captions sit below the figure: "**Figure 4.12.** Caption in Source Serif 9 pt italic-free." The first clause of the caption states what the reader should notice.
- No text below 6.5 pt at final size. The figure linter (§5.5) checks this.
- Every figure has alt text, written in its spec file and emitted as `<title>`/`<desc>` and `alt`.

### 4.5 Sample specifications for five key diagrams

Each figure has a YAML spec rendered by our `netfig` library (§5.4). The five below are the reference implementations, built in Phase 0 to freeze the language.

**(1) Figure 3.20: TCP three-way handshake and teardown (ladder/sequence diagram)**
- Layout: two vertical lifelines (Client left, Server right) 110 mm apart, in ink at 1 px, headed by host glyphs with labels `Client 10.0.0.5:51514` and `Server 93.184.216.34:443`. Time runs downward and is labelled in the margin as "time ↓".
- Messages are arrows sloping downward (slope encodes one-way latency, so the RTT is visible as vertical distance). They are orange (L4), labelled above the arrow in JetBrains Mono: `SYN seq=x`, `SYN-ACK seq=y ack=x+1`, `ACK ack=y+1`, then a grey data band, then `FIN`, `ACK`, `FIN`, `ACK`.
- State labels sit beside each lifeline at the instant of change, as pills: `SYN-SENT`, `ESTABLISHED`, `FIN-WAIT-1`, `TIME-WAIT`. Their colour is the TCP state colour from figure (4) below, which links the two figures.
- Annotations: a brace on the client side marks "1 RTT before data can flow", and a hatched block after the final ACK marks "TIME-WAIT = 2 × MSL".
- Variant: Figure 3.21 overlays a lost SYN-ACK (red cross) and a retransmission timer as a dashed bracket.

**(2) Figure 3.9: IPv4 header bit layout**
- A 32-bit-wide grid (each bit column 3.4 mm; total 109 mm, fitting the text block), with bit indices 0–31 across the top in JetBrains Mono 6.5 pt and byte boundaries marked by heavier ticks every 8 bits.
- Rows: word 0 `Version(4) | IHL(4) | DSCP(6) | ECN(2) | Total Length(16)`; word 1 `Identification(16) | Flags(3) | Fragment Offset(13)`; word 2 `TTL(8) | Protocol(8) | Header Checksum(16)`; words 3–4 Source and Destination Address; word 5 Options (variable, drawn with a torn edge).
- Fill: L3 blue at 10 %. Fields asked about in interviews (TTL, Protocol, Flags/Fragment Offset, DSCP) get a 22 % fill and a small margin callout ("TTL: decremented per hop; prevents loops from persisting").
- Right-hand side: the byte offset of each word (0, 4, 8, 12, 16, 20). Under the grid: one real packet's hex dump (`45 00 00 3c 1c 46 40 00 40 06 …`), with leader lines from each byte group to its field. This is the bridge from the abstract layout to Wireshark.
- The same component draws TCP, UDP, Ethernet, 802.1Q, IPv6, VXLAN and 802.11 MAC headers. All of them are one YAML list of `(name, bits, layer, emphasis)`.

**(3) Figure 5.4: Two-tier spine–leaf (Clos) fabric with ECMP**
- Top row: 4 spine switches (L3 switch glyphs), evenly spaced across the wide width (163 mm). Middle row: 6 leaf switches. Bottom row: 2 servers per leaf, as server glyphs.
- Every leaf connects to every spine with 1 px ink links, so there are 24 links. Server–leaf links are dotted grey (out of focus).
- Overlay: one flow from Server A (leaf 1) to Server K (leaf 6), with its 4 equal-cost paths drawn as 1.5 px blue (L3) arrows. A 5-tuple hash box at leaf 1 shows `hash(src,dst,sport,dport,proto) mod 4 = 2`, and the chosen path is solid with the other three at 35 % opacity.
- Domain shading: the "underlay (eBGP, ASN per leaf)" band behind the switches in `#E7F5FF`. A label strip on the left gives tier names and oversubscription ("3:1").
- Variant 5.5 adds VXLAN tunnels as double-line pipes between leaf VTEPs.

**(4) Figure 3.24: TCP connection state machine**
- Layout: 11 states as rounded rectangles (r = 6, 34 × 12 mm), laid out by Graphviz `dot` (top-to-bottom) with fixed ranks: CLOSED top; LISTEN and SYN-SENT; SYN-RCVD; ESTABLISHED centre (drawn 1.3× larger, as the "home" state); the active-close column (FIN-WAIT-1, FIN-WAIT-2, CLOSING, TIME-WAIT) on the left; the passive-close column (CLOSE-WAIT, LAST-ACK) on the right.
- Colour: a state family fill is used (opening = pale blue `#E7F5FF`, established = pale green `#EBFBEE`, closing = pale orange `#FFF4E6`). These are the same pills used in Figure 3.20.
- Edges: client path in solid 1.5 px ink, server path in dashed 1.5 px ink. Labels have the format `event / action` in JetBrains Mono 7 pt (`rcv SYN / snd SYN,ACK`). Unusual transitions (simultaneous open, simultaneous close) are drawn in muted grey and marked with a Deep Dive icon.
- Margin note: "Interview favourite: why TIME-WAIT exists (two reasons)" points to the Trap box.

**(5) Figure 7.6: Process address space and the socket receive path (memory diagram)**
- Left half: a vertical address-space column 40 mm wide, high addresses at the top. Regions (kernel space, stack ↓, mmap region, heap ↑, BSS, data, text) are drawn as stacked rectangles with heights not to scale, a "not to scale" note, and addresses in JetBrains Mono (`0x7ffd…`, `0x5555…`). Kernel space is hatched grey, above a dashed line marked "user/kernel boundary".
- Right half: the receive path as a left-to-right flow. NIC (with a ring-buffer drawn as a circular array of 8 slots, 3 filled) → DMA arrow → `sk_buff` (process/kernel object glyph) → protocol stack (stacked L2/L3/L4 bars in layer colours) → socket receive queue (a queue of 3 packet bars) → `recv()` copy arrow crossing the boundary into a `char buf[2048]` on the stack (pointer arrow from the variable `buf` to the array cells).
- Numbered steps ①–⑥ in L4 orange. Copy operations are drawn with a "two-sheets" glyph, so the reader can count copies (which sets up the zero-copy section).
- Caption first clause: "Data are copied once from kernel to user space on each `recv()` …".

---

## 5. Toolchain recommendation and build pipeline

### 5.1 Recommendation: **Pandoc Markdown → HTML/CSS → Paged.js → Chromium (Playwright) → PDF**, with Python post-processing

**Justification, criterion by criterion:**

| Requirement | How the chosen chain meets it | Comparison |
|---|---|---|
| Callout boxes | CSS components from Pandoc fenced divs (`::: worked-example`). Rounded corners, tints, icons and hatches take a few lines of CSS each. | tcolorbox is equally capable but needs TeX Live. Typst is capable too. |
| Code with syntax highlighting | Pandoc's skylighting at build time, with a custom theme JSON matched to the palette. A custom KDE-XML syntax file (`--syntax-definition`) covers **Cisco IOS / Junos / EOS CLI**, which no common highlighter supports well. | minted needs Pygments plus shell-escape. |
| Vector network diagrams | **Native SVG** is the browser's own format. Fonts in figures are the same Inter/JetBrains Mono as the text, with no conversion step. Alt text is native. | TikZ is the strongest diagram language, but authoring 600 consistent figures in TikZ is slow and most contributors do not know it. |
| Tables | HTML tables + CSS; page-spanning tables repeat their header row (`thead`). | |
| Cross-references (page numbers) | Paged.js `target-counter(attr(href), page)` was **verified** in the test. Section and figure numbers come from a Lua filter (pre-numbered at build time, so no CSS counters across chunks). | |
| Index | Pandoc span `[term]{.ix}` → anchors. A generated index page of links with `target-counter` gives page numbers. Ranges are merged, and duplicates on one page collapsed, in a post-pass (§5.3). | LaTeX's makeindex is more mature; ours is about 150 lines of Python. |
| Bookmarks | Chromium `outline: true` turns H1–H3 into PDF bookmarks (**verified**). | |
| Consistent icons | One SVG sprite. CSS colours it via `currentColor`. | |
| Margin notes, running heads, mirrored margins, page-edge tabs | Paged.js margin boxes, `string-set`, `@page :left/:right`, named pages (`page: opener`) (**verified** for heads and margin notes). | |
| Design iteration speed | Edit CSS → see the change in a browser in seconds (Paged.js runs live in Chromium), with dev tools. This is the decisive advantage for an "extremely aesthetic" book: a design cycle measured in seconds, not in compile runs. | |
| Install footprint | Everything needed is present except Paged.js (1 MB) and the vendored fonts (about 5 MB). | TeX Live: several GB. |
| Future outputs | The same HTML can give an EPUB/web edition with little extra work. | |

**Known weaknesses and mitigations:**

- (i) Paged.js is slow and memory-hungry on very long documents, and has layout bugs with complex floats. *Mitigation:* we build **one HTML file per pillar** (about 50 pages each) and run a two-pass page-number resolution across the whole book (§5.3). This also parallelises the build across 12 Chromium processes. We pin `pagedjs@0.4.3`, and we keep floats simple: margin notes are the only floats, and figures are placed in-flow.
- (ii) There is no automatic line-breaking quality warning (no TeX "overfull hbox"). *Mitigation:* a DOM overflow checker (§5.5), plus `hyphens: auto` with `lang="en-GB"`, and `text-wrap: pretty` (supported in current Chromium) for better paragraph breaks.
- (iii) Justified text looks worse than TeX's. *Mitigation:* the body is set **ragged-right**, which also suits the plain voice and the Julia Evans / Stripe Press visual register.

**Why not the others:**

- **LaTeX + tcolorbox + TikZ** gives the best typography and the most powerful diagrams. It is not installed, it needs a multi-GB install, iteration is slow, and contributor ramp-up is steep. We would pick it if TeX Live were already present.
- **Typst** is fast, modern and small, with good boxes and cross-references. But it is not installed, its diagram ecosystem (CeTZ, fletcher) is younger and less flexible than SVG for our glyph library, and its paged-media features (margin notes, bleed tabs) need more custom code. It remains **the fallback** if Paged.js proves unstable (§6.4). Authoring in Pandoc Markdown keeps that switch possible, because Pandoc has a Typst writer.
- **Markdown/Pandoc alone** (via its default LaTeX or HTML route) does not give the design control we need. It is our *front end*, not our layout engine.

### 5.2 Repository layout

```
placement-book/
├── book.yml                 # metadata, pillar order, colours, page budgets
├── plans/                   # 8w.yml (day → section ids per track; source of Must tags),
│                            #   3m.yml, 6m.yml, checkpoints.yml → rendered into Part 0
├── Makefile                 # entry points (see 5.3)
├── content/
│   ├── 00-front/            # how-to-use.md, tracks.md, schedules.md, tracker.md, lab-setup.md
│   ├── 01-dsa/
│   │   ├── _pillar.yml      # title, accent, opener hero figure, outcomes, prerequisites
│   │   ├── 01-complexity.md
│   │   ├── 02-arrays-strings.md
│   │   ├── …
│   │   ├── cheatsheet.md
│   │   ├── questions.yml    # question bank (company, track, difficulty, answer)
│   │   └── figures/         # *.fig.yml specs + any hand-authored *.svg
│   ├── 02-programming/ … 12-supporting/
│   └── 99-back/             # mocks/, rapid-fire.yml, playbooks/*.md, glossary.yml
├── code/                    # every code listing as a real, tested file
│   ├── 01-dsa/lpm_trie.py   #   included via ```{.python include="…" lines="10-34"}
│   └── tests/               # pytest + a C test runner: listings must compile and pass
├── labs/                    # containerlab topologies + expected-output snapshots for Try It
├── figures/
│   ├── lib/                 # netfig (Python): glyphs.svg, markers.svg, tokens.py
│   ├── templates/           # topology, ladder, bitfield, statemachine, memory, flow, plot
│   └── build/               # generated SVG (git-ignored)
├── style/
│   ├── tokens.css           # palette, type scale, spacing (generated from book.yml)
│   ├── base.css  page.css  components.css  figures.css  print.css  screen.css
│   └── skylighting-theme.json, syntax/cisco-ios.xml, junos.xml, eos.xml
├── assets/fonts/  assets/icons/sprite.svg
├── filters/                 # Pandoc Lua: callouts.lua, numbering.lua, xref.lua,
│                            #   index.lua, glossary.lua, include-code.lua, figure.lua
├── tools/
│   ├── render.mjs           # Playwright + Paged.js: HTML → PDF per pillar, dumps id→page map
│   ├── assemble.py          # merge PDFs, outlines, page labels, metadata (pypdf)
│   ├── qa/                  # linkcheck.py, overflow.mjs, figlint.py, prose_lint.py,
│   │                        #   spelling (en-GB), a11y.py, size.py, proof.py (PNG contact sheets)
│   └── vendor/pagedjs-0.4.3/
└── dist/                    # book.pdf, book-print.pdf, proofs/
```

### 5.3 Build pipeline

`make book` (or `make pillar P=04` for one pillar; `make watch P=04` for a live browser preview):

1. **Tokens.** `book.yml` generates `tokens.css` and `figures/lib/tokens.py`, so CSS and figures share one palette.
2. **Figures.** `netfig` renders every `*.fig.yml` to SVG. Graphviz layout runs through `@hpcc-js/wasm-graphviz` in Node for state machines and trees: we take only the node coordinates and edge routes, and draw them with our own glyphs and markers. matplotlib plots (queueing curves, path-loss, complexity growth) use a style sheet derived from the tokens, exported as SVG with fonts as text (`svg.fonttype: none`). The step is cached by spec hash.
3. **Code.** `pytest` + `gcc -Wall -Wextra -Werror` run every listing in `code/`. The build fails if any listing does not compile or its test fails, because a wrong listing in a placement book costs the reader an interview.
4. **Markdown → HTML.** For each pillar, Pandoc runs with Lua filters:
   - `numbering.lua` (sections, figures, tables, examples, labs);
   - `callouts.lua` (fenced divs → component HTML with icons and labels);
   - `xref.lua` (`@fig:ipv4-header` → link + number);
   - `index.lua` / `glossary.lua` (index anchors; margin definitions pulled from `glossary.yml`);
   - `include-code.lua`;
   - skylighting for highlighting;
   - KaTeX for mathematics.

   Each pillar gets its own HTML, wrapped in a Jinja template with the opener spread.
5. **Pass 1 layout.** `render.mjs` opens each pillar HTML in Chromium with Paged.js (12 in parallel). After pagination it records the pillar page count and an `id → page` map for every anchor (taken from the DOM: `.pagedjs_page` index of each element).
6. **Resolve.** It computes global page offsets, rewrites cross-pillar references to literal page numbers (`p. 211`), and generates the index and contents pages from the merged maps (merging ranges such as 211–213 and sorting with an en-GB collator).
7. **Pass 2 layout.** It re-renders with `counter-reset: page <offset>`, then prints each pillar to PDF (`preferCSSPageSize`, `printBackground`, `outline`, `tagged`). It checks that page counts did not change between passes; if they did (rare), it iterates once more.
8. **Assemble.** `assemble.py` (pypdf):
   - merges the PDFs in order;
   - builds a 3-level outline (Part → Pillar → Section), which keeps per-file outlines but nests them under the pillars;
   - sets page labels (roman for front matter, arabic from Pillar 1);
   - sets document metadata (title, author, `lang=en-GB`, XMP);
   - rewrites cross-file links to internal `GoTo` destinations;
   - compresses streams.

   It outputs `dist/book.pdf` (screen: off-white paper, internal links coloured) and `dist/book-print.pdf` (white paper, 3 mm bleed, links in ink, crop marks via Paged.js `marks: crop`).
9. **QA** (§5.5), then **proofs**: pypdfium2 renders every spread to PNG at 100 dpi, and `proof.py` lays them out in contact sheets per pillar (`dist/proofs/04.png`) for visual review.

### 5.4 Figure production approach

- **Primary: `netfig`**, a small in-house Python library (≈ 1,500 lines), emitting SVG from YAML specs, with seven templates: `topology`, `ladder`, `bitfield`, `statemachine`, `memory`, `flow` (pipeline/flowchart), `stack` (encapsulation and layers). Authors describe *content* (nodes, links, messages, fields); the library owns *style*. This is the cause of consistency across 600 figures and several authors.
- **Hand-authored SVG** (in Inkscape or Figma, exported to plain SVG and then normalised by `figlint`, which re-maps colours to tokens and fonts to the book set) for at most about 10 % of figures. These are the opener hero diagrams, analogy sketches and one-off explanatory art. They must reuse `glyphs.svg` symbols.
- **matplotlib** for data plots only, with a shared `book.mplstyle`.
- **Graphviz (WASM)** is a layout engine inside `netfig`, never a stand-alone source of styled figures.
- **Mermaid and D2** are *allowed for drafts only*. Authors may sketch in Mermaid in a draft. The figure editor converts every sketch to a `netfig` spec before copy-edit, because Mermaid's styling cannot be made to match the language reliably.
- **Screenshots** (Wireshark, terminal) are avoided. Terminal output is set as text in Try It boxes. Wireshark views are redrawn as `bitfield` + packet-list tables, which reproduce better and stay searchable. Unavoidable screenshots are cropped, given 2× PNG and an alt text.

### 5.5 Quality assurance (all in `make qa`; CI fails on errors)

| Check | Tool | Pass criterion |
|---|---|---|
| Internal links and xrefs | `linkcheck.py`: every `#id` link resolves; every PDF link annotation has a valid destination (pypdf); no "p. ??" placeholders | 0 broken |
| External URLs (further reading, RFCs) | HEAD requests with a cache, run weekly | report only |
| Overflow (the "overfull box" analogue) | `overflow.mjs` in Chromium after pagination flags any element whose `scrollWidth > clientWidth`, code lines over 78 columns, tables wider than the text block, figures over the wide width, SVG text under 6.5 pt, and margin notes colliding or running off-page | 0 errors |
| Pagination | empty pages, a heading in the last 15 % of a page (keep-with-next failure), a component split with under 3 lines either side, widowed figure captions, more than 2 margin notes on a page | 0 errors / warnings reviewed |
| Element density | `prose_lint.py` counts Big Idea (exactly 1 per H2), Interview Lens and Check Yourself (1 per H2), and spreads with more than 85 % prose | warnings |
| Voice and spelling | en-GB spelling via Hunspell `en_GB` plus a custom tech wordlist; a US-spelling deny-list (`-ize` policy decided once: we use *-ise*); a banned-hype list ("simply", "just", "amazing", "game-changer", "!") | 0 errors |
| Technical correctness | code tests (§5.3 step 3); lab expected outputs re-run on Containerlab images; numeric claims in worked examples recomputed by small scripts where possible | 0 failures |
| Self-contained | `selfcontained.py`: no URLs in body text outside Sources and playbook verify boxes; every exercise, checkpoint, mock and bank question has a linked full solution; every Try It has printed expected output | 0 errors |
| Plan and tag consistency | `plans.py`: every section in `8w.yml` is tagged Must for that track, and no Must section is missing from it; Should sections appear in `3m.yml`; daily Block B load in the 8-week plan stays at ≤ 130 min, estimated from the page count at 32 min/page; schedule tags (§2.16) match the plans | 0 errors |
| Glossary sync | every margin definition matches `glossary.yml`; every glossary term is used at least once | 0 mismatches |
| Accessibility | tagged PDF (Chromium `tagged: true`); document language en-GB; every figure has alt text (figlint); heading levels in sequence; colour contrast of all tokens ≥ 4.5:1 for text and ≥ 3:1 for graphics (scripted, as in this plan's table); colour never the only cue (checked by greyscale proof review); optional veraPDF PDF/UA report if Java is available | 0 errors on scripted checks |
| File size | `size.py`: screen PDF ≤ 40 MB target (vector figures; fonts subset; images ≤ 200 dpi at print size, JPEG q85 or PNG-8 where possible); print PDF ≤ 120 MB | report + threshold |
| Fonts | all fonts embedded and subset, no fallback faces (`DejaVu`, `Liberation`) present in the PDF font list | 0 fallbacks |
| Visual regression | per-page PNG diff against the last approved proof; changes over 2 % of pixels are listed for review | review list |

---

## 6. Production plan

### 6.1 Phases

| Phase | Duration | Work | Exit criterion |
|---|---|---|---|
| **0. Foundation** | weeks 1–3 | Vendor fonts and icons; tokens; CSS components; Lua filters; `render.mjs`/`assemble.py`; `netfig` with the 7 templates; the **five reference figures** of §4.5; the style guide (voice rules + component usage + figure language) as a short contributor handbook. | A 12-page **specimen** PDF (opener spread, one full H2 section with every component, a cheat sheet, a playbook page) is approved. Build time per pillar is under 60 s. |
| **1. Pilot pillar** | weeks 3–6 | Write **Pillar 3 (CN fundamentals)** in full, since every other pillar depends on its terms and figures. Include all labs, tests and the question bank. Run full QA. Test with 5 student beta readers. | Pilot reviewed. Template and element frequencies adjusted from reader feedback (where did they stop reading, and why?). **In parallel:** outlines for all 12 pillars plus `plans/8w.yml`, so that Must/Should/Optional tags are fixed before drafting starts (the 8-week plan defines Must). Two or three recent placement candidates per track review the plan for realism. |
| **2. Parallel drafting** | weeks 6–16 | Remaining 11 pillars in three waves of about 4, ordered by dependency (wave A: 1, 2, 4, 7; wave B: 5, 6, 8, 9; wave C: 10, 11, 12). Front matter is drafted after wave A, once the tracks are concrete. | Each pillar passes the "draft complete" gate (below). |
| **3. Figures** | weeks 7–18, overlapping | Figure editor converts draft sketches to `netfig` specs; commissions hero diagrams per pillar. | All figures pass figlint; none are drafts. |
| **4. Back matter** | weeks 14–19 | Mock OAs (with solutions tested in code), 100 rapid-fire questions (drawn from pillar question banks), 7 company playbooks (each dated, with sources), glossary consolidation, index tagging pass. | Back matter passes technical review. |
| **5. Integration and copy-edit** | weeks 17–21 | One copy-editor for voice consistency across all pillars; index pass (a single person tags index terms, for consistency); cross-reference pass; full-book build. | Whole-book QA green. |
| **6. Proof and beta** | weeks 21–24 | Two proof rounds on contact sheets and print-outs (one A4 print-out per pillar, since printed pages reveal problems that screens hide); 15–20 beta readers across the three tracks; errata fixes. | Errata below a threshold; sign-off. |
| **7. Release** | week 25 | v1.0 PDF (screen + print); errata page; a changelog. | — |

**Calendar for the 2027 season.** Starting on 2 November 2026, week 25 is late April 2027. Indian campus placement drives for 2027 run from roughly July (many NITs and private universities) to December (IIT Phase 1). A student starting the 8-week plan in May 2027 therefore has the book in time, but a student on the 6-month plan would need it by January 2027. We therefore release in two stages, each a complete, self-contained PDF:

- (i) **v0.9 "Plans + Must lane"** at about week 14 (early February 2027): all Must sections for all tracks, Part 0, cheat sheets and checkpoints, with Should and Optional sections marked "coming in v1.0". Drafting waves are ordered by Must density for this reason.
- (ii) **v1.0 complete** at week 25.

The cover, the running footer and the metadata carry "2027" and an "information correct as of" date.

### 6.2 Parallel drafting and review workflow

- **One branch per pillar** (`pillar/04-routing`). Authors work only in `content/04-*`, `code/04-*`, `labs/04-*`, which keeps merge conflicts close to zero. Shared files (`glossary.yml`, `book.yml`, style) change only through a small "shared" pull request reviewed by the design lead.
- **Each section's lifecycle** (tracked as labels on GitHub issues):

  `outline` → `draft` → `tech-review` → `revise` → `figures-final` → `copy-edit` → `laid-out` → `proofed`

  - **Outline:** H2 list, the Big Idea sentence for each H2, the worked examples planned, and the figures planned (as one-line specs). Reviewing outlines before prose prevents large rewrites.
  - **Tech review:** a second subject-matter person checks every claim has a cause, all numbers, and all CLI syntax against a real or emulated device. Labs are re-run.
  - **Copy-edit:** voice (supervisor style), British spelling, terms defined in passing, (i)/(ii) lists.
  - **Design review:** on the rendered PDF, not on the Markdown, checking spread rhythm, component density and figure placement.
- **CI on every pull request:** build the pillar, run QA, and post a contact-sheet PNG of changed spreads as a PR comment, so reviewers see the page, not only the diff.
- **Use of AI drafting assistants (if used):** each pillar is drafted by a separate agent session from its outline plus the style guide and a shared glossary. A different session does the technical review, with the explicit task of finding unsupported claims and wrong commands. All output still goes through human tech review and the code and lab tests, because fluent but wrong networking detail is the most likely defect.
- **The "draft complete" gate** for a pillar: all H2s drafted; element frequencies met; all listings tested; all labs reproducible; question bank of 20 or more items; cheat sheet drafted; figure specs in place.

### 6.3 Effort estimate

Assumptions: about 600 pages; about 600 figures; about 250 worked examples; about 100 labs; about 400 bank questions.

| Work item | Unit effort | Total (person-days) |
|---|---|---|
| Foundation (design system, pipeline, `netfig`, specimen) | — | 25 |
| Writing (first draft) | 0.6 pd/page | 330 |
| Technical review | 0.15 pd/page | 85 |
| Revision after review | 0.2 pd/page | 110 |
| Figures (netfig spec + polish) | 0.25 pd/figure avg (hero diagrams ≈ 2 pd each) | 170 |
| Code listings + tests | 0.3 pd/listing × 300 | 90 |
| Labs (build, test, expected output) | 0.75 pd/lab | 75 |
| Question banks, mocks, rapid fire, solutions | — | 45 |
| Company playbooks (research, sourcing, dating) | 3 pd each × 7 | 21 |
| Copy-edit (voice + spelling) | 0.08 pd/page | 47 |
| Index + glossary | — | 18 |
| Layout tuning + proof rounds | — | 35 |
| Beta coordination + errata | — | 15 |
| Project management (≈ 8 %) | — | 85 |
| Plans (8-week day plan, 3-month, 6-month), tags, 8 checkpoints with solutions | — | 15 |
| **Total** | | **≈ 1,165 person-days** |

At 120 working days in 24 weeks, this is about **10 full-time people**: 5 subject-matter authors, 2 technical reviewers, 1.5 figure designers, 1 design/build lead and 0.5 copy-editor. With heavy AI-assisted drafting, the writing and figure-spec lines might fall by 40–50 %. Review, testing and proofing do not shrink, which gives a realistic floor of about **770 person-days**, or about 6.5 people. A smaller team should keep the v0.9 Must-lane date and let v1.0 slip, rather than compress review.

### 6.4 Risks and mitigations

| Risk | Likelihood / impact | Mitigation |
|---|---|---|
| Paged.js performance or layout bugs at this scale | Medium / High | Per-pillar builds; pinned version; simple floats; Phase-0 stress test with a synthetic 80-page pillar. **Fallback:** Pandoc → Typst writer, with components re-implemented in Typst. Because content is Markdown and figures are SVG, the switch costs about 3 weeks, not a rewrite. |
| Technical errors (wrong commands, outdated protocol behaviour) | High / High | Tested listings and labs; a dedicated tech reviewer per wave; claims tied to RFCs or vendor documentation in each pillar's "Sources"; a public errata page. |
| Inconsistent voice across authors | High / Medium | One style guide with before/after examples; prose lint; a single final copy-editor; the pilot pillar used as the reference. |
| Figure inconsistency | Medium / High | All figures via `netfig`; figlint; a single figure editor owns the final pass. |
| Design ambition crowding out rigour ("pretty but shallow") | Medium / High | Element-frequency rules cap decoration. Every Analogy ends with "where it fails", and every Big Idea states its cause. Deep Dives carry the rigour without blocking beginners. |
| Interview content seen as fabricated or as leaked proprietary questions | Medium / High | Describe question *types* and themes only; label editorial judgements as such; date the playbooks; no claims of "actual questions asked at X". |
| Trademark/branding issues (vendor names, icons, CLI) | Low / Medium | Nominative use only; no logos or brand colours; own device glyphs; a trademark notice on the copyright page. |
| Tags mis-calibrated (a Must topic tagged Should, so fast-plan readers miss it) | Medium / High | Tags derived from one source (`8w.yml`); review by recent candidates per track; beta readers on the 8-week plan report gaps; v1.0 adjusts. |
| 2027 timing slips | Medium / High | Two-stage release (v0.9 Must lane first); waves ordered by Must density. |
| Scope creep (page count drifts beyond 600) | High / Medium | Page budgets in `book.yml`. The build reports pages versus budget per pillar, and over-budget sections move content to Deep Dives or cut it. |
| Content staleness (Wi-Fi 7, cloud services, hiring processes) | Medium / Medium | Date-stamped sections; playbooks isolated in back matter for easy update; a versioned PDF with a changelog. |
| Print fidelity (tints too pale, hairlines vanish) | Medium / Low | Minimum line weight 0.5 pt; tints of at least 8 %; a test print of the specimen on an office laser printer and at a print shop in Phase 0. |
| Large PDF hurts mobile readers | Low / Medium | Vector-first; a size budget checked in QA; an optional "lite" build without hero spreads. |

---

### Appendix A: component authoring syntax (what authors write)

```markdown
## Longest-prefix match {#sec:lpm difficulty=2 tag="sw:should infra:must wlan:optional" minutes=50}

::: big-idea
A router forwards on the most specific matching prefix, because a longer mask
describes a smaller, and therefore more precise, set of destinations.
:::

Consider a table with the entries 10.0.0.0/8 and 10.1.0.0/16 ... A [prefix]{.def}
is ...  see @fig:lpm-trie.

::: worked-example {#ex:lpm-5 title="Longest-prefix match on a five-entry table"}
1. We first write each prefix in binary ...
2. ...

**Result.** The packet leaves via Gi0/2.
:::

::: trap
*Claim:* The router picks the route with the lowest metric.
*Why it is wrong:* Metric is compared only between routes to the *same* prefix ...
*Correct statement:* ...
:::

::: interview-lens {companies="cisco,juniper,arista,amazon" level="tech-1"}
...
:::

![](figures/lpm-trie.fig.yml){#fig:lpm-trie .wide alt="Binary trie of five prefixes ..."}
```

### Appendix B: verified build snippet (from the test)

```js
// tools/render.mjs (core)
import { chromium } from 'playwright';
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(`file://${htmlPath}`);            // HTML includes paged.polyfill.js
await page.waitForFunction(() => document.querySelector('.pagedjs_pages'));
await page.pdf({ path: pdfPath, preferCSSPageSize: true,
                 printBackground: true, outline: true, tagged: true });
```
