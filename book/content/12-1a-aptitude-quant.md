::: {.chapter .p12}
::: opener
[Part I · Pillar 12]{.part-label}

[12]{.num}

# Supporting Subjects {#ch12}

[Everything else that decides the offer: aptitude, the computer-science core, design, behaviour and your own story.]{.promise}

1. [12A · Aptitude and online assessments (12.1 to 12.7)]{} [MUST]{}
2. [12B · Object-oriented programming (12.8)]{} [MUST]{}
3. [12C · Database management systems (12.9)]{} [MUST]{}
4. [12D · Computer organisation (12.10)]{} [SHOULD]{}
5. [12E · Light system design for networking roles (12.11)]{} [MUST]{}
6. [12F · Behavioural interviews, STAR and Amazon principles (12.12)]{} [MUST]{}
7. [12G · Résumé and project deep-dives (12.13)]{} [MUST]{}
:::

Pillars 1 to 11 teach what a network engineer must know. This pillar teaches what stands between that knowledge and the offer: the online assessment that creates the shortlist, the core-computing viva that every campus panel adds, the design conversation, the behavioural round and the document that starts all of them. None of it is difficult in the way BGP is difficult; all of it is lost by the unprepared through speed, vocabulary and structure. We therefore treat each topic as a drill: a formula card, a shortcut, and worked examples that can be redone on paper in two minutes.

Seven sub-chapters follow, lettered 12A to 12G. Aptitude (12A) is the largest, because it is the first filter in nearly every Indian campus drive and the only one that is purely arithmetic. Networking examples recur through the pillar, with the fictional organisation *Campus Net* from earlier pillars appearing wherever a story needs a setting.

## [12.1]{.sec}Online assessments: formats, pacing and guessing [Must · ■□□]{.tag} {#s12-1}

An online assessment, or OA, is a timed test taken on a browser, usually with a webcam running, that decides who is interviewed. The format varies by company and by year, so the table below records what candidates have reported and should be checked with your placement cell before each drive.

| Platform | What is reported | Consequence for you |
|---|---|---|
| HackerRank | Hidden test cases, partial marks per case, language chosen per question, tab switches logged | Practise reading input fast; submit a brute force early |
| AMCAT | Adaptive English, quantitative and logical sections, then coding (Automata) | Early accuracy matters more than speed |
| Mercer Mettl | Employer sets section order, timing, negative marking and locking | Read the instruction screen; a locked section cannot be revisited |
| CoCubes | Modules for aptitude, fundamentals, coding and English; usually no negative marking | Attempt everything |
| Company papers (Cisco, Juniper, Qualcomm, Nokia) | 30 to 40 MCQs on aptitude and core subjects, plus one to three coding problems, in 60 to 90 minutes | Budget about 45 seconds per MCQ |

For the company-by-company papers see Part III; here we need only the consequence, which is that every format rewards the same three habits: a fixed time budget, a two-pass method and sensible guessing.

::: bigidea
An assessment is a time-allocation problem before it is a knowledge problem, because the marks lost to one stubborn question exceed the marks gained by solving it.
:::

### The two-pass method

In pass one we spend at most 45 seconds on each question, answer those that yield, and flag the rest. In pass two we return to the flagged questions in order of how close they felt. A final five minutes fills every remaining blank when there is no penalty. This works because question difficulty is uneven and marks are not: an easy question and a hard one are worth the same.

<figure>
<svg viewBox="0 0 480 132" width="480">
<defs><marker id="a121" viewBox="0 0 6 6" refX="5" refY="3" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L6 3L0 6z" fill="#1A1D23"/></marker></defs>
<text class="lbl" x="20" y="16">One 60-minute paper, 50 questions (72 s average)</text>
<rect class="fill" x="20" y="30" width="24" height="26"/>
<rect class="box" x="44" y="30" width="228" height="26"/>
<rect class="hl" x="272" y="30" width="90" height="26"/>
<rect class="box" x="272" y="30" width="90" height="26"/>
<rect class="fill" x="362" y="30" width="30" height="26"/>
<line class="ln" x1="20" y1="30" x2="20" y2="62"/>
<line class="ln" x1="392" y1="30" x2="392" y2="62"/>
<text class="sm" x="32" y="46" text-anchor="middle">scan</text>
<text class="lbl" x="158" y="46" text-anchor="middle">Pass 1: answer fast, flag the rest</text>
<text class="lbl" x="317" y="46" text-anchor="middle">Pass 2</text>
<text class="sm" x="377" y="46" text-anchor="middle">blanks</text>
<text class="sm" x="20" y="74">0</text>
<text class="sm" x="44" y="74" text-anchor="middle">2</text>
<text class="sm" x="164" y="74" text-anchor="middle">20</text>
<text class="sm" x="272" y="74" text-anchor="middle">38</text>
<text class="sm" x="362" y="74" text-anchor="middle">53</text>
<text class="sm" x="392" y="74" text-anchor="end">60 min</text>
<line class="acc" x1="164" y1="82" x2="164" y2="98" marker-end="url(#a121)"/>
<text class="lbl" x="164" y="110" text-anchor="middle">Checkpoint: Q25 by minute 20</text>
<line class="acc" x1="272" y1="82" x2="272" y2="98" marker-end="url(#a121)"/>
<text class="lbl" x="300" y="110" text-anchor="start">Minute 38: pass 1 ends, about 15 flagged</text>
</svg>
<figcaption><b>Figure 12.1</b> A pacing plan for a 50-question, 60-minute paper. If you are behind a checkpoint, skip faster rather than think harder.</figcaption>
</figure>

### Negative marking and guessing

Suppose a paper has four options and deducts a quarter mark for a wrong answer. A blind guess has expected value 1/4 × 1 − 3/4 × 1/4 = +0.0625, so it is marginally positive. Remove one option you know to be wrong and the value becomes 1/3 × 1 − 2/3 × 1/4 = +0.167. With a penalty of one third, the blind guess is exactly neutral, and one eliminated option again turns it positive. Hence the rule: guess whenever you can eliminate at least one option, and leave a question blank only when the penalty is as large as the reward.

::: trap
*Claim:* "Never guess in a paper with negative marking." *Why it is wrong:* the penalty is usually smaller than the reward, so the expectation of a guess after one elimination is positive. *Correct statement:* compute the expectation once, for the stated penalty, and apply it to every question; do not decide mood by mood.
:::

### The CS-MCQ section

Most company papers add 15 to 25 questions on computing fundamentals. They are fast marks if the rules are fresh, and the rules are taught elsewhere in this book, so the table gives only the one-line rule and its home.

| Topic | One-line rule | Home |
|---|---|---|
| C output | Look first for undefined behaviour, then precedence, then `sizeof` and integer promotion | [§2.15](#s2-15){.ref} |
| Scheduling | Turnaround = completion − arrival; waiting = turnaround − burst | [§7.4](#s7-4){.ref} |
| Page replacement | FIFO evicts oldest, LRU evicts least recently used, Optimal evicts the page used farthest ahead | [§7.7](#s7-7){.ref} |
| Deadlock | Four conditions together: mutual exclusion, hold and wait, no pre-emption, circular wait | [§7.6](#s7-6){.ref} |
| Subnetting | Block size = 256 − mask octet; usable hosts = 2<sup>h</sup> − 2 | [§3.4](#s3-4){.ref} |
| Normal forms, SQL | See this pillar | [§12.9](#s12-9){.ref} |

::: check
1. A paper has five options and a penalty of 1/4 per wrong answer. What is the expected value of a blind guess? [^c12a-1]
2. With the same paper, you eliminate two options. What is the expected value? [^c12a-2]
3. In a 90-minute paper with 40 MCQs and two coding problems, you allot 30 minutes to MCQs. What is the time per MCQ? [^c12a-3]
:::

[^c12a-1]: 1/5 × 1 − 4/5 × 1/4 = 0.2 − 0.2 = 0. A blind guess is neutral.
[^c12a-2]: Three options remain: 1/3 × 1 − 2/3 × 1/4 = 1/3 − 1/6 = +0.167.
[^c12a-3]: 30 × 60 / 40 = 45 seconds.

## [12.2]{.sec}Number system, remainders, HCF and LCM [Must · ■□□]{.tag} {#s12-2}

Number-system questions look like tricks but are applications of three ideas: factorisation, cycles and the remainder. They also overlap with networking, because base conversion and divisibility by powers of two underlie subnet masks ([§3.4](#s3-4){.ref}).

#### Formula card: divisibility and divisors

- Divisible by 2, 5, 10: last digit even, 0 or 5, 0. By 4 and 8: last two and last three digits. By 3 and 9: digit sum. By 11: (sum of odd-place digits) − (sum of even-place digits) is 0 or a multiple of 11.
- By 7: remove the last digit *d*, subtract 2*d* from what remains, repeat; the result is divisible by 7 exactly when the original was.
- If N = p<sup>a</sup> q<sup>b</sup> r<sup>c</sup>, the number of divisors is (a + 1)(b + 1)(c + 1) and their sum is the product of (p<sup>a+1</sup> − 1)/(p − 1) over the primes.
- HCF × LCM = product of the two numbers (two numbers only, not three).

**Shortcut.** To count divisors, write the factorisation once and do not list them; to test 7, run the doubling trick twice at most.

::: example
**Divisors of 360.**

1. Factorise: 360 = 2<sup>3</sup> × 3<sup>2</sup> × 5.
2. Count: (3 + 1)(2 + 1)(1 + 1) = 4 × 3 × 2 = 24 divisors.
3. Sum: (2<sup>4</sup> − 1)/(2 − 1) × (3<sup>3</sup> − 1)/(3 − 1) × (5<sup>2</sup> − 1)/(5 − 1) = 15 × 13 × 6.

[Result: 24 divisors with sum 1,170.]{.result}
:::

::: example
**Is 2,597 divisible by 7?**

1. Last digit 7; the rest is 259. Compute 259 − 2 × 7 = 245.
2. Repeat: last digit 5, rest 24: 24 − 10 = 14.
3. 14 is a multiple of 7.

[Result: yes; 2,597 = 7 × 371.]{.result}
:::

#### Formula card: cycles, remainders, zeros and bases

- Unit digits repeat: 0, 1, 5, 6 never change; 4 and 9 have cycle 2; 2, 3, 7, 8 have cycle 4. Take the exponent mod the cycle length, and read 0 as the full cycle.
- Remainders multiply: (*a* × *b*) mod *n* = ((*a* mod *n*) × (*b* mod *n*)) mod *n*. If a<sup>k</sup> ≡ 1 (mod n) for a small k, reduce the exponent mod k.
- Trailing zeros of *n*! = ⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + …
- Base conversion: group binary digits in fours for hex and in threes for octal, from the right.

**Shortcut.** For a large power, first find the cycle, then reduce the exponent. Never compute the power.

::: example
**Unit digit of 3<sup>47</sup> × 8<sup>22</sup>.**

1. The cycle of 3 is 3, 9, 7, 1. Since 47 mod 4 = 3, 3<sup>47</sup> ends in 7.
2. The cycle of 8 is 8, 4, 2, 6. Since 22 mod 4 = 2, 8<sup>22</sup> ends in 4.
3. Multiply the digits: 7 × 4 = 28.

[Result: unit digit 8.]{.result}
:::

::: example
**(a) Remainder of 2<sup>100</sup> divided by 7. (b) Trailing zeros of 125!. (c) 1101101<sub>2</sub> in hex.**

1. (a) 2<sup>3</sup> = 8 ≡ 1 (mod 7). Since 100 = 3 × 33 + 1, 2<sup>100</sup> ≡ 2<sup>1</sup> = 2.
2. (b) 125/5 = 25, 125/25 = 5, 125/125 = 1, so 25 + 5 + 1 = 31.
3. (c) Pad to 0110 1101 and read each group: 6 and D.

[Result: (a) 2; (b) 31 zeros; (c) 0x6D, which is 109.]{.result}
:::

#### Formula card: HCF and LCM

- HCF is the largest number dividing all the numbers; LCM is the smallest that all divide. Use prime factors: take the lowest powers for HCF and the highest for LCM.
- "Greatest number that divides *a* and *b* leaving remainders *r* and *s*": HCF of (*a* − *r*) and (*b* − *s*), provided the answer exceeds both remainders.
- "Smallest number leaving the same remainder *r* on division by *x*, *y*, *z*": LCM(*x*, *y*, *z*) + *r*.
- Events that repeat every *x*, *y* and *z* units coincide every LCM units.

**Shortcut.** For HCF by hand use Euclid: replace (*a*, *b*) by (*b*, *a* mod *b*) until the remainder is zero.

::: example
**Three timers fire every 12, 18 and 30 seconds. They fire together at 09:00:00. When next, and how often in one hour?**

1. 12 = 2<sup>2</sup>·3, 18 = 2·3<sup>2</sup>, 30 = 2·3·5. The highest powers give LCM = 2<sup>2</sup> × 3<sup>2</sup> × 5 = 180 seconds.
2. They next coincide at 09:03:00.
3. In 3,600 seconds there are 3,600/180 = 20 further coincidences, plus the first at 09:00:00.

[Result: after 3 minutes; 21 times including the start.]{.result}
:::

::: example
**Find the greatest number that divides 414 and 536 leaving remainders 6 and 8.**

1. Subtract the remainders: 414 − 6 = 408 and 536 − 8 = 528.
2. Euclid: 528 mod 408 = 120; 408 mod 120 = 48; 120 mod 48 = 24; 48 mod 24 = 0. The HCF is 24.
3. Check that 24 exceeds both remainders: 24 > 8. Verify: 414 = 17 × 24 + 6 and 536 = 22 × 24 + 8.

[Result: 24.]{.result}
:::

::: check
1. Number of divisors of 720. [^c12a-4]
2. Unit digit of 7<sup>2</sup> × 9<sup>13</sup>. [^c12a-5]
3. Trailing zeros of 200!. [^c12a-6]
4. Smallest number leaving remainder 3 on division by 8, 12 and 20. [^c12a-7]
:::

[^c12a-4]: 720 = 2<sup>4</sup> × 3<sup>2</sup> × 5, so 5 × 3 × 2 = 30.
[^c12a-5]: 7<sup>2</sup> = 49 ends in 9; 9<sup>13</sup> ends in 9 (odd exponent); 9 × 9 = 81, so 1.
[^c12a-6]: 40 + 8 + 1 = 49.
[^c12a-7]: LCM(8, 12, 20) = 120, so 123.

## [12.3]{.sec}Percentages, profit and loss, ratio and averages [Must · ■□□]{.tag} {#s12-3}

These four topics are one family: each compares a quantity with a base. Most errors come from choosing the wrong base, so every card below states the base first.

#### Formula card: percentages

- *x*% of *y* = *y*% of *x*. A percentage change is (change / original) × 100, with the original as base.
- Successive changes of *a*% and *b*% give a net change of *a* + *b* + *ab*/100 per cent.
- If price rises by *r*%, consumption must fall by 100*r*/(100 + *r*)% to keep expenditure fixed. If price falls by *r*%, consumption can rise by 100*r*/(100 − *r*)%.
- Fractions worth memorising: 1/6 = 16.67%, 1/7 = 14.29%, 1/8 = 12.5%, 1/9 = 11.11%, 1/11 = 9.09%, 1/12 = 8.33%.

**Shortcut.** Convert the percentage to a fraction ("25% of the price rises" means 1/4 more, so 1/5 less) and reason in parts.

::: example
**Sugar rises in price by 25%. By what percentage must a household cut consumption to hold spending constant?**

1. Let the old price be 100 per kg and use 1 kg: spending 100.
2. New price is 125, so the same 100 buys 100/125 = 0.8 kg.
3. The cut is 0.2 kg out of 1 kg. Formula check: 100 × 25 / 125 = 20.

[Result: 20%.]{.result}
:::

::: example
**In an exam, 30% of candidates failed mathematics, 25% failed English and 10% failed both. What percentage passed both?**

1. Failed at least one subject: 30 + 25 − 10 = 45% (inclusion and exclusion).
2. Passed both: 100 − 45.

[Result: 55%.]{.result}
:::

#### Formula card: profit and loss

- Profit% = (profit / cost price) × 100; selling price = cost price × (1 ± *p*/100). Discount is always on the marked price; profit is always on the cost price.
- Successive discounts of *a*% and *b*% equal a single discount of *a* + *b* − *ab*/100.
- A dishonest weight giving *e* grams short per true kilogram of *w* grams: gain% = *e* / (*w* − *e*) × 100.

**Shortcut.** Work with multipliers: a 20% discount is × 0.8, a 25% markup is × 1.25.

::: example
**An item is marked ₹800. Successive discounts of 20% and 10% are given. The cost price is ₹480. Find the profit percentage.**

1. Selling price: 800 × 0.8 × 0.9 = ₹576. This equals a single discount of 20 + 10 − 2 = 28%.
2. Profit: 576 − 480 = ₹96.
3. Profit% on cost: 96/480 × 100.

[Result: 20% profit.]{.result}
:::

::: example
**A trader sells at cost price but uses a 900 g weight for a kilogram. Find the gain.**

1. The customer pays for 1,000 g and receives 900 g, so the error is 100 g.
2. The trader's cost for what was delivered is the value of 900 g.
3. Gain% = 100 / 900 × 100.

[Result: 11.11%, not 10%, because the base is what was actually given.]{.result}
:::

#### Formula card: ratio, proportion, partnership and alligation

- If *a* : *b* = *c* : *d* then *ad* = *bc*. Convert a ratio to parts and find the value of one part.
- Partners share profit in the ratio of (capital × time).
- Alligation: mixing a dearer item at price *d* with a cheaper one at *c* to reach mean price *m*, the quantities are in the ratio (*d* − *m*) : (*m* − *c*).

**Shortcut.** Draw the alligation cross: put *c* and *d* on top, *m* in the middle, subtract diagonally, and read the answer along the bottom.

::: example
**Rice at ₹40 per kg is mixed with rice at ₹55 per kg to give a mixture worth ₹48 per kg. In what ratio?**

1. Cheaper: 40; dearer: 55; mean: 48.
2. Cheaper : dearer = (55 − 48) : (48 − 40) = 7 : 8.
3. Check: (7 × 40 + 8 × 55) / 15 = (280 + 440)/15 = 48.

[Result: 7 : 8 (cheaper to dearer).]{.result}
:::

::: example
**A invests ₹5,000 for 12 months and B invests ₹8,000 for 6 months. They earn ₹9,000. Find each share.**

1. Capital × time: A = 60,000; B = 48,000. Ratio 60 : 48 = 5 : 4.
2. Parts total 9; one part is 9,000 / 9 = ₹1,000.

[Result: A gets ₹5,000 and B gets ₹4,000.]{.result}
:::

#### Formula card: averages

- Average = sum / count. A change of Δ in the average over *n* items means the total changed by *n*Δ.
- When a new member joins and the average rises by Δ, the new member exceeds the old average by (*n* + 1)Δ.
- Weighted average = Σ(count × value) / Σ count.

**Shortcut.** Always convert averages to totals, change the total, and convert back.

::: example
**The average age of 8 students is 15. When the teacher is included, the average rises by 2. Find the teacher's age.**

1. Total of students: 8 × 15 = 120.
2. New total: 9 × 17 = 153.
3. Teacher = 153 − 120.

[Result: 33 years.]{.result}
:::

::: example
**A batsman's average after 10 innings is 42. What must he score in the 11th to raise it to 45?**

1. Total after 10 innings: 420. Required total after 11: 11 × 45 = 495.
2. Score = 495 − 420. Check by the shortcut: 45 + 10 × 3 = 75.

[Result: 75 runs.]{.result}
:::

::: lens
[CISCO · JUNIPER · NOKIA · QUALCOMM]{.co}

Percentage and ratio questions are the bulk of the quantitative section in these drives because they are quick to set and quick to mark. The examiner is testing whether you pick the correct base. A strong candidate states the base aloud ("profit on cost, discount on marked") before computing, which also catches the commonest error.
:::

::: check
1. A price falls by 20%. By what percentage can consumption rise at constant spending? [^c12a-8]
2. A number is increased by 30% and then decreased by 30%. Net change? [^c12a-9]
3. Milk at ₹30 per litre and ₹42 per litre are mixed to make ₹36 per litre. Ratio? [^c12a-10]
4. The average of five numbers is 18. Two are removed, with average 12. Average of the other three? [^c12a-11]
:::

[^c12a-8]: 100 × 20 / (100 − 20) = 25%.
[^c12a-9]: 30 − 30 − 900/100 = −9%, a fall of 9%.
[^c12a-10]: (42 − 36) : (36 − 30) = 6 : 6 = 1 : 1.
[^c12a-11]: Total 90; removed 24; remaining 66, so 66/3 = 22.

:::
