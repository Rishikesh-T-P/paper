# Authoring guide (read fully before writing a chapter)

The book is *Network Engineer Placements 2027*. The full plan is in `plan/00-MASTER-PLAN.md`; the per-pillar detail is in `plan/pillars-*.md` and `plan/cheatcodes-apparatus.md`. One file per chapter goes in `content/NN-slug.md`. Build with `python3 build.py` (≈ 1–3 min), which writes `dist/Network-Engineer-Placements-2027.pdf`.

## 1. File skeleton (copy exactly; change the numbers, class and text)

```markdown
::: {.chapter .p3}
::: opener
[Part I · Pillar 3]{.part-label}

[3]{.num}

# Computer Networks Fundamentals {#ch3}

[Every packet tells a story; we learn to read it, layer by layer.]{.promise}

1. [3.1 Layers and encapsulation]{} [MUST]{}
2. ...
:::

## [3.1]{.sec}Layers and encapsulation [Must · ■□□]{.tag} {#s3-1}

Prose ...

:::
```

- Pillar classes: `.p1` … `.p12`; front/back matter `.p0`. The `#chN` id on the chapter title is required (it builds the contents).
- Every H2 has an id `#sN-M` so others can cross-reference it as `[text](#s3-4){.ref}`, which prints "(p. 37)".
- Tags: `[Must · ■□□]{.tag}`, `[Should · ■■□]{.tag}`, `[Optional · ■■■]{.tag}`.

## 2. The six learning elements (fenced divs only; no other boxes)

```markdown
::: bigidea
One sentence, with its cause.
:::

::: example
**Subnet 192.168.10.0/24 into six subnets.**

1. Step with reasoning ...
2. ...

[Result: /27, block size 32, ...]{.result}
:::

::: trap
*Claim:* ... *Why it is wrong:* ... *Correct statement:* ...
:::

::: lens
[CISCO · JUNIPER · AMAZON]{.co}

What is asked, what a strong answer contains, likely follow-ups.
:::

::: lab
`LAB 3.2 · 15 MIN` then commands in a fenced code block, then the key output lines, then **What you should notice:** ...
:::

::: check
1. Question? [^c3-1]
2. Question? [^c3-2]
:::

[^c3-1]: One-line answer.
```

Also allowed: `::: deep` (skippable rigour, sparingly) and margin notes `[**Term** — definition, analogy, mnemonic or speed trick.]{.margin}` placed at the start of a paragraph (≤ 2 per page).

## 3. Figures (inline SVG, minimalist)

```html
<figure>
<svg viewBox="0 0 480 160" width="480">
  <rect class="box" x="20" y="60" width="70" height="34" rx="2"/>
  <text class="lbl" x="55" y="81" text-anchor="middle">Host A</text>
  <line class="ln" x1="90" y1="77" x2="200" y2="77"/>
  <path class="acc" d="..."/>  <!-- the one thing to notice -->
</svg>
<figcaption><b>Figure 3.2</b> One descriptive phrase.</figcaption>
</figure>
```

Classes: `box` (white, ink stroke), `fill` (light grey), `ln` (ink line), `lg` (grey line), `acc` (accent stroke, once per figure), `accf`/`acct` (accent fill/text), `hl` (yellow highlight), `dash`; text `lbl` (9 px), `sm` (7.5 px grey), `mono`. Arrowheads: define `<marker id="aN" ...>` with a unique id per figure. Conventions: router = circle with a cross; switch = rectangle with two opposing arrows; host = small rectangle; cloud = rounded path; no 3-D, no gradients, no logos, no emoji. Keep widths ≤ 480. Use figures generously: ladder diagrams, header bit-layouts, state machines, topologies, memory diagrams. Every figure must be correct.

## 4. Voice (guide-style, senior era): mandatory

- Plain and sober. No hooks, rhetorical questions, exclamation marks, hype, "let's dive in", "game-changer", emoji. Open sections with a factual claim or "Consider …".
- British spelling (analyse, behaviour, optimise, centre, modelling, queueing).
- "We" for the author and reader working together; "one may/one must" for general claims.
- "Further," (never "Moreover"); "Thus,", "Hence,", "Therefore,"; "Note that"; inline lists "(i) … (ii) …".
- Define terms in passing ("…, termed the *bandwidth-delay product*,") or with an em-dash apposition.
- Every claim gets its cause ("This is because …"). Close a paragraph of reasoning with "Thus," or "Hence,".
- Sentences of 18–27 words on average; short, clear paragraphs. Beginner-friendly: every term is explained before it is used.

## 5. Zero redundancy (hard rules)

- Teach each concept only at its canonical home (see the table in plan/00-MASTER-PLAN.md §2A). Elsewhere write one sentence and a cross-reference.
- Each question is solved once, in its chapter's Problem Set. Compare with tables, not prose. Lab output: only the lines that matter.
- Respect the page budget in §2A (≈ 0.5 page per 300 words of prose; figures ≈ 0.3 page).

## 6. End of chapter (always, in this order)

```markdown
::: pack
## Problem Set {#ps3}

::: problems
::: q
### Q3.1 Explain the TCP three-way handshake.
[CISCO · GOOGLE · TECH-1 · ■□□ · S]{.meta}

[30-second answer: ...]{.short}

**Approach.** ... **Answer.** ... **Follow-ups.** ... **Mistakes.** ...
:::
:::
:::

::: pack
## Revision Spread {#rv3}

::: revision
::: top
Ten facts and the three figures to remember.
:::
Short notes as dense bullets, key tables, then a flashcard table (| Q | A |).
:::
:::
```

Meta tag: companies · round (OA / TECH-1 / TECH-2 / HM) · difficulty · S (specific question reported by candidates) or T (topic reported; our wording). Omit empty solution fields. Code solutions: C for systems/networking-company problems, C++ for general DSA, Python for scripting; one language only.
