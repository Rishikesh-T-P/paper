::: {.p12}

## [12.6]{.sec}Logical reasoning [Must · ■□□]{.tag} {#s12-6}

Reasoning questions test method more than knowledge. Each family has one drawing or one table that turns the puzzle into bookkeeping; the cards below name it. A full eight-person circular puzzle is solved in [Q12.10](#ps12){.ref}.

#### Formula card: series and coding-decoding

- Number series: test differences, then second differences, then ratios, then squares, cubes or primes. Letter series: convert letters to positions (A = 1, …, Z = 26).
- Common patterns: *n*(*n* + 1) gives 2, 6, 12, 20; doubling differences give 2<sup>*n*</sup> + 1; alternating series are two interleaved series.
- Coding: a shift by *k*, a reversal (A ↔ Z, so position *p* becomes 27 − *p*), a positional sum, or a word-to-word map found by comparing sentences that share a word.

**Shortcut.** In a word-map problem, find the word common to two sentences and the code common to the same two; that pair is the match.

::: example
**Complete: (a) 2, 6, 12, 20, 30, ? (b) 3, 5, 9, 17, 33, ? (c) B, D, G, K, ?**

1. (a) The differences are 4, 6, 8, 10, so the next difference is 12: 42. (Also 6 × 7.)
2. (b) The differences are 2, 4, 8, 16, so the next is 32: 33 + 32 = 65.
3. (c) Positions 2, 4, 7, 11; the differences 2, 3, 4 continue with 5, giving 16, which is P.

[Result: 42; 65; P.]{.result}
:::

::: example
**(a) Under a shift of +1, ROUTER is coded as? (b) In a code, "ping the host" is "ka ro mi", "host is up" is "mi ta ne" and "ping is up" is "ka ta ne". Code for "the"?**

1. (a) R, O, U, T, E, R become S, P, V, U, F, S.
2. (b) The first two sentences share "host" and "mi", so host = mi.
3. The first and third share "ping" and "ka", so ping = ka. Hence "the" is the remaining code of the first sentence, "ro".

[Result: SPVUFS; ro.]{.result}
:::

#### Formula card: blood relations and directions

- Draw a family tree, one symbol per person. Parse the sentence from the end, replacing each phrase by a person: "the only daughter of my mother" is *me* (if I am female).
- Directions: put the start at the origin, North up, and add the displacement of every leg. A right turn from North faces East; from East faces South.

<figure>
<svg viewBox="0 0 480 120" width="480">
<rect class="box" x="30" y="20" width="16" height="16"/>
<text class="lbl" x="56" y="32">male</text>
<circle class="box" cx="38" cy="58" r="8"/>
<text class="lbl" x="56" y="62">female</text>
<line class="ln" x1="22" y1="88" x2="46" y2="88"/><line class="ln" x1="22" y1="91" x2="46" y2="91"/>
<text class="lbl" x="56" y="93">married</text>
<line class="ln" x1="32" y1="108" x2="32" y2="118"/>
<text class="lbl" x="56" y="116">child below</text>
<text class="lbl" x="170" y="14">A is B's sister; C is B's mother; D is C's father</text>
<rect class="box" x="230" y="26" width="16" height="16"/><text class="sm" x="238" y="52" text-anchor="middle">D</text>
<line class="ln" x1="238" y1="42" x2="238" y2="62"/>
<circle class="box" cx="238" cy="72" r="8"/><text class="sm" x="238" y="92" text-anchor="middle">C</text>
<line class="ln" x1="238" y1="80" x2="238" y2="90"/>
<line class="ln" x1="200" y1="96" x2="276" y2="96"/>
<line class="ln" x1="200" y1="96" x2="200" y2="104"/><line class="ln" x1="276" y1="96" x2="276" y2="104"/>
<circle class="box" cx="200" cy="112" r="8"/><text class="lbl" x="214" y="115">A</text>
<rect class="box" x="268" y="104" width="16" height="16"/><text class="lbl" x="290" y="116">B</text>
<path class="acc" d="M330 70 H440" />
<text class="lbl" x="335" y="62">A is D's granddaughter</text>
</svg>
<figcaption><b>Figure 12.3</b> The family-tree notation and one solved chain. The sentence is read link by link, never as a whole.</figcaption>
</figure>

::: example
**Pointing to a man, Rekha says, "His mother is the only daughter of my mother." How is the man related to Rekha?**

1. "The only daughter of my mother" is Rekha herself.
2. So the man's mother is Rekha.

[Result: he is her son.]{.result}
:::

::: example
**A walks 5 km north, turns right and walks 3 km, turns right and walks 5 km, then turns left and walks 2 km. Where is he relative to the start?**

1. North 5, then east 3, then south 5: net position 3 km east, 0 north.
2. Facing south, a left turn faces east: 2 km further east.

[Result: 5 km due east of the start.]{.result}
:::

#### Formula card: seating arrangements

- Draw the seats first (a row with numbered places, or a circle). Fix the most definite clue, then place each clue in turn; carry the alternatives forward on the same diagram.
- In a row facing north, left is west. In a circle facing the centre, a person's left is clockwise.
- Count "between" carefully: two seats between A and B puts them three places apart.

::: example
**Five engineers P, Q, R, S, T sit in a row facing north. (i) Q is at one end. (ii) R is two places to the right of Q. (iii) S is not next to R. (iv) T is somewhere to the left of P. Find the order, left to right.**

1. From (ii), R is to Q's right, so Q is at the left end: Q _ R _ _.
2. From (iii), S cannot take seat 2 or 4, so S is in seat 5: Q _ R _ S.
3. T and P fill seats 2 and 4; by (iv) T is the left one.

[Result: Q, T, R, P, S.]{.result}
:::

::: example
**Using the same row, who is third from the right and who sits between T and P?**

1. Reading right to left: S, P, R, T, Q, so the third from the right is R.
2. Between T (seat 2) and P (seat 4) is seat 3.

[Result: R in both cases.]{.result}
:::

#### Formula card: syllogisms and data sufficiency

- Syllogisms: draw Venn circles and keep only conclusions true in *every* drawing. "All A are B" also implies "some A are B" in the usual Indian convention. "No A is B" is symmetrical; "some A are B" is symmetrical; "all A are B" is not.
- A "some" statement never forces a definite conclusion by itself: from "all A are B, some B are C" no relation between A and C follows.
- Data sufficiency options: (A) I alone; (B) II alone; (C) both together, neither alone; (D) each alone; (E) neither, even together. Test each statement alone first, then both.

<figure>
<svg viewBox="0 0 480 120" width="480">
<text class="lbl" x="120" y="14" text-anchor="middle">Case 1: R overlaps S</text>
<circle class="box" cx="100" cy="68" r="40"/><circle class="fill" cx="100" cy="68" r="20" style="opacity:.8"/>
<ellipse class="box" cx="135" cy="68" rx="26" ry="14"/>
<text class="sm" x="82" y="72">S</text><text class="sm" x="62" y="46">D</text><text class="sm" x="142" y="72">R</text>
<text class="lbl" x="360" y="14" text-anchor="middle">Case 2: R outside S</text>
<circle class="box" cx="340" cy="68" r="40"/><circle class="fill" cx="326" cy="68" r="18"/>
<ellipse class="box" cx="368" cy="68" rx="22" ry="14"/>
<text class="sm" x="320" y="72">S</text><text class="sm" x="300" y="46">D</text><text class="sm" x="362" y="72">R</text>
<text class="sm" x="240" y="112" text-anchor="middle">"All S are D; some D are R": both drawings are legal, so "some S are R" does not follow</text>
</svg>
<figcaption><b>Figure 12.4</b> A conclusion is valid only if it holds in every legal drawing; here the second drawing breaks it.</figcaption>
</figure>

::: example
**Statements: All switches are devices. Some devices are routers. Conclusions: I. Some switches are routers. II. Some routers are devices.**

1. Draw switches inside devices; routers overlap devices, and may or may not touch switches (Figure 12.4). So I is not certain.
2. Some devices are routers; the relation is symmetrical, so some routers are devices.

[Result: only II follows.]{.result}
:::

::: example
**(a) Is 10.1.1.130 in the same subnet as 10.1.1.10? I. The mask is 255.255.255.128. II. Both hosts use the same gateway. (b) What is the average speed for a journey? I. The first half of the distance was at 60 km/h. II. The second half was at 40 km/h.**

1. (a) I alone: block size 128, so .10 lies in 0 to 127 and .130 in 128 to 255: different subnets. II alone proves nothing (a gateway can serve several subnets). Answer A.
2. (b) Neither statement alone gives a speed over the whole journey. Together, with equal halves, the average is 2 × 60 × 40/100 = 48 km/h, whatever the distance. Answer C.

[Result: (a) A; (b) C.]{.result}
:::

::: check
1. Next term: 3, 8, 15, 24, 35, ? [^c12c-1]
2. Under reversal (A ↔ Z), the code of CAT. [^c12c-2]
3. "A is B's brother. C is A's mother. D is C's husband." How is D related to B? [^c12c-3]
4. All routers are devices. No device is a cable. Does "No router is a cable" follow? [^c12c-4]
:::

[^c12c-1]: The differences are 5, 7, 9, 11 (each term is n² − 1), so the next is 48.
[^c12c-2]: C is 3, becomes 24 (X); A becomes Z; T is 20, becomes 7 (G): XZG.
[^c12c-3]: D is C's husband and C is the mother of both A and B, so D is B's father.
[^c12c-4]: Yes: every router lies inside devices, and devices lie outside cables.

## [12.7]{.sec}Data interpretation and verbal ability [Should · ■□□]{.tag} {#s12-7}

#### Data interpretation

A data-interpretation question gives a table or chart and asks for growth, ratio or share. Approximation is the whole skill: round to two significant figures, compare fractions by cross-multiplication, and remember that percentage growth is always relative to the earlier value.

| Campus | Peak 2025 (Gb/s) | Peak 2026 (Gb/s) |
|---|---|---|
| North | 12 | 15 |
| Main | 20 | 26 |
| Hostel | 8 | 11 |
| Lab | 15 | 18 |
| Annexe | 5 | 8 |

::: example
**For the table above, find (a) the campus with the highest percentage growth, (b) the highest absolute growth, and (c) the total growth.**

1. Growth: North 3/12 = 25%; Main 6/20 = 30%; Hostel 3/8 = 37.5%; Lab 3/15 = 20%; Annexe 3/5 = 60%.
2. Absolute growth is largest for Main (6 Gb/s).
3. Totals: 60 in 2025 and 78 in 2026, so 18/60 = 30%.

[Result: Annexe (60%); Main (6 Gb/s); 30% overall.]{.result}
:::

#### Verbal ability

#### Formula card: verbal

- Subject–verb agreement: the verb agrees with the head noun, not the nearest noun ("the list of requirements *is* long"). "Each", "every" and "neither" take the singular. With "neither … nor", the verb agrees with the nearer subject.
- Keep tenses consistent and lists parallel ("configure, test and deploy", not "configure, testing and deploy"). Use "a" before a consonant *sound* ("a unit", "an hour").
- Reading comprehension: read the questions first, skim the passage for the opening and closing sentences, then scan for the keywords. The correct option restates the passage; the wrong ones add, exaggerate or reverse it.
- Para-jumbles: the opening sentence introduces a noun without a pronoun; "this", "it", "therefore" and "however" cannot start a paragraph.

::: example
**Correct: (a) "The list of requirements are long." (b) "Neither the router nor the switches was configured." Then order: P. This is why a lost packet is simply sent again. Q. The Internet delivers packets on a best-effort basis. R. It makes no promise that any given packet will arrive. S. Reliability is therefore added by the hosts.**

1. (a) The head noun is "list", so "is". (b) The nearer subject is "switches", so "were".
2. Q is the only sentence with no pronoun or connective, so it opens. R continues with "it". P explains the consequence ("this is why"), and S concludes ("therefore").

[Result: "is"; "were"; order QRPS.]{.result}
:::

::: example
**Passage: "A route flap occurs when a prefix is repeatedly announced and withdrawn. Each change forces neighbouring routers to recompute paths, so one unstable link can burden routers far away. Operators therefore apply damping, which penalises a prefix on every flap and suppresses it once the penalty crosses a threshold. Damping protects routers, but it also delays recovery: a prefix that has genuinely returned stays hidden until its penalty decays. Many operators now use it sparingly." Q1. The passage mainly argues that (A) flaps are harmless (B) damping protects routers at a cost to recovery (C) damping should be abolished (D) neighbouring routers cause flaps. Q2. Which is implied? (A) Damping never helps (B) Operators weigh damping's benefit against its delay.**

1. Q1: the third sentence introduces damping and the fourth balances protection against delay. Option A contradicts sentence two; C overstates "sparingly"; D reverses cause and effect. Answer B.
2. Q2: "sparingly" implies that the cost is considered. A is an exaggeration ("never"). Answer B.

[Result: B and B.]{.result}
:::

::: check
1. In the table above, what is the ratio of Main's 2026 peak to Annexe's? [^c12c-5]
2. Choose: "Each of the engineers (is / are) on call." [^c12c-6]
:::

[^c12c-5]: 26 : 8 = 13 : 4.
[^c12c-6]: "Each" is singular, so "is".

:::
