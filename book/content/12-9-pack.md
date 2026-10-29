::: {.p12}
::: pack
## Revision Spread {#rv12}

::: revision
::: top
**Ten facts.** (1) With a 1/4 penalty and four options, guess whenever one option is eliminated: expected value 1/3 − 1/6 = +0.17. (2) Average speed over equal distances is 2*xy*/(*x* + *y*); over equal times it is the mean. (3) Work problems: take the LCM of the days as total units. (4) CI − SI over two years is P(*r*/100)<sup>2</sup>. (5) Unit digits of 2, 3, 7, 8 cycle in 4; reduce the exponent mod 4. (6) Polymorphism is a call through the vptr to the vtable; overloading is compile time, overriding is run time. (7) SQL runs FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT. (8) BCNF: every determinant is a super key; 3NF allows a prime attribute as the dependent. (9) Cache address: offset = log<sub>2</sub>(block), index = log<sub>2</sub>(sets), tag = the rest. (10) Design in six steps and put a number on step two; tell stories in STAR with 60% of the time on your own actions.

**Three figures to redraw from memory.** The two-pass pacing bar (Figure 12.1); the address split with tag 19, index 7 and offset 6 (Figure 12.9); the dual-core campus with one summary per building (Figure 12.12).
:::

#### Aptitude master table
| Topic | Formula or rule | Watch for |
|---|---|---|
| Divisors | N = p<sup>a</sup>q<sup>b</sup>: (a+1)(b+1); HCF × LCM = product of two | Three numbers: not valid |
| Unit digit | Cycle 4 (2, 3, 7, 8), 2 (4, 9); 0, 1, 5, 6 fixed | Exponent remainder 0 means last of cycle |
| Remainders | (a·b) mod n = ((a mod n)(b mod n)) mod n | Reduce before multiplying |
| Trailing zeros | n! has ⌊n/5⌋ + ⌊n/25⌋ + … | Count 5s, not 2s |
| Percent change | a + b + ab/100; price up r%: cut 100r/(100+r)% | Base is the old value |
| Profit | On cost; discount on marked price | Successive: a + b − ab/100 |
| False weight | Gain% = error/(true − error) × 100 | Base is what was given |
| Alligation | (dearer − mean) : (mean − cheaper) | Answer is cheaper : dearer |
| Partnership | Share ∝ capital × time | Equal times: capitals |
| Work | Rate 1/*a*; together *ab*/(*a*+*b*) | Leak or drain is negative |
| Speed | km/h × 5/18 = m/s; equal distance: 2*xy*/(*x*+*y*) | Not the simple mean |
| Relative speed | Same way subtract; opposite add | Trains: distance = sum of lengths |
| Platform | (train + platform)/speed | Pole: train only |
| Boats | down *u*+*v*, up *u*−*v*; *u* = (d+u)/2, *v* = (d−u)/2 | Round trip speed is not *u* |
| SI, CI | *PRT*/100; P(1+*r*/100)<sup>n</sup>; half-yearly: *r*/2, 2n | CI − SI (2 y) = P(*r*/100)<sup>2</sup> |
| P and C | P(*n*,*r*), C(*n*,*r*); circular (*n*−1)!; repeats *n*!/(*p*!*q*!) | "Together": glue, then × internal |
| Stars and bars | *r* identical to *k*: C(*r*+*k*−1, *k*−1) | Zero allowed |
| Probability | Favourable/total; at least one: 1 − P(none) | Without replacement: change denominator |
| Clock | Angle |30H − 5.5M|; overlap every 720/11 min | Reduce angles above 180° |
| Calendar | 100 y: 5 odd days; 400 y: 0; leap year: 2 | Count days, divide by 7 |
| Ages | Ratio parts 5*x*, 3*x*; add the years to each | Same years added to both |

#### SQL cheat table
| Item | Rule |
|---|---|
| Order of execution | FROM and joins, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT |
| INNER, LEFT | Matches only; all left rows with nulls. Filter right columns in `ON` for left joins |
| COUNT | `COUNT(*)` counts rows; `COUNT(col)` skips nulls |
| WHERE, HAVING | Rows before grouping; groups after |
| IN, EXISTS | `NOT IN` fails with a null in the subquery; prefer `NOT EXISTS` |
| Window | `fn() OVER (PARTITION BY a ORDER BY b)`: `ROW_NUMBER`, `RANK` (gaps), `DENSE_RANK`, `LAG` |
| Top *n* per group | `ROW_NUMBER() OVER (PARTITION BY g ORDER BY x DESC)`, keep ≤ *n* |
| Second highest | `... WHERE salary < (SELECT MAX(salary) ...)` or `DENSE_RANK() = 2` |
| Transactions | `BEGIN; ...; COMMIT;` or `ROLLBACK`. Claim rows with a conditional `UPDATE` and check the row count |
| Isolation | Dirty, non-repeatable, phantom: each level forbids one more |

#### OOP, organisation and design in brief
- Pillars: encapsulation (protect), abstraction (simplify), inheritance (is-a), polymorphism (one call, many behaviours). Prefer composition over inheritance.
- Virtual: one vptr per object, one vtable per class; constructors cannot be virtual, polymorphic bases need a virtual destructor. Abstract class holds code and a contract; interface is a contract only.
- SOLID: one reason to change; extend, do not edit; subclass substitutes for base; small interfaces; depend on abstractions.
- Normal forms: atomic cells; whole key; nothing but the key; every determinant a super key.
- B+ tree: shallow (fan-out 100: three levels per million rows), linked leaves for ranges, leftmost-prefix rule; indexes slow writes.
- Two's complement: negate by invert and add one; range −2<sup>*n*−1</sup> to 2<sup>*n*−1</sup> − 1; overflow when same-sign operands give an opposite-sign result. Float: 1, 8, 23 bits, bias 127.
- Hierarchy: L1 about 1 ns, DRAM about 100 ns, SSD about 100 µs: each step ten to a thousand times slower. AMAT = hit + miss rate × penalty. Pipeline speedup *kn*/(*k* + *n* − 1); hazards: structural, data, control.
- Design: clarify, estimate, sketch, deep-dive two parts, failures, trade-offs. Campus: 8,000 × 0.4 × 2 Mb/s = 6.4 Gb/s. Limiter: token bucket for bursts, sliding-window counter ≈ previous × overlap + current, 429 and `Retry-After`. CDN: 500 TB/day is 46 Gb/s mean, three times at peak.

#### Behaviour, résumé and offer
- STAR: S and T 20 s, Action 60 s in "I", Result 20 s with a number, Learning 10 s. Eight stories tagged to two to four principles of the sixteen; a fresh story per interviewer.
- Tell me about yourself: Present, Past, Future in 60 to 90 s, with a named product in the last sentence.
- Offer: compare *guaranteed annual cash*; ask what variable pay paid last year; one-time bonuses are not recurring; on-campus offers rarely negotiate.
- Résumé checklist: (1) one page, (2) single column, (3) PDF, (4) no photograph, (5) live links, (6) CGPA only if 7.5 or above, (7) skills grouped, (8) only defensible skills, (9) three projects, (10) a number in each bullet, (11) every bullet begins with a past-tense verb, (12) XYZ form, (13) stack named for each project, (14) README and diagram on GitHub, (15) tests visible, (16) certifications matched to a project, (17) achievements with ratings, (18) keywords match the job, (19) no skill bars, (20) consistent dates.
- Project defence: ten questions (problem, architecture, your share, hardest bug, trade-offs, tests, results, ten and a thousand times load, security, change); prepare a two-minute and a ten-minute version.

::: flash
#### Flashcards
| Q | A | Q | A |
|---|---|---|---|
| Net of +*a*% then +*b*% | *a* + *b* + *ab*/100 | Unit-digit cycle of 7 | 7, 9, 3, 1 |
| Price up *r*%: cut consumption by | 100*r*/(100 + *r*)% | False weight gain | error/(true − error) × 100 |
| Alligation ratio | (dearer − mean) : (mean − cheaper) | A and B together | *ab*/(*a* + *b*) days |
| Average speed, equal distances | 2*xy*/(*x* + *y*) | km/h to m/s | × 5/18 |
| Crossing a platform | (train + platform)/speed | CI − SI, two years | P(*r*/100)<sup>2</sup> |
| Circular arrangements of *n* | (*n* − 1)! | P(at least one) | 1 − P(none) |
| Trailing zeros of *n*! | ⌊*n*/5⌋ + ⌊*n*/25⌋ + … | Angle between clock hands | \|30H − 5.5M\| |
| Divisors of p<sup>a</sup>q<sup>b</sup> | (a + 1)(b + 1) | HCF × LCM of two numbers | Their product |
| How polymorphism works | vptr to vtable | Overloading binds at | Compile time |
| Why a virtual destructor | `delete` through a base pointer | Open-closed principle | Extend, do not edit |
| Rule of three | Destructor, copy constructor, copy assignment | An interface in C++ | Abstract class of pure virtuals |
| SQL execution order | FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY | `COUNT(*)` against `COUNT(col)` | Rows against non-nulls |
| 2NF fails when | A partial dependency on a composite key | BCNF requires | Every determinant a super key |
| A phantom read | New rows in a repeated range query | Leftmost-prefix rule | A composite index serves queries from its left columns |
| Durability comes from | The write-ahead log | Range of *n*-bit two's complement | −2<sup>*n*−1</sup> to 2<sup>*n*−1</sup> − 1 |
| Negate in two's complement | Invert and add one | IEEE 754 single | 1, 8, 23 bits; bias 127 |
| Cache fields | Offset log<sub>2</sub> B, index log<sub>2</sub> sets, tag the rest | Pipeline speedup | *kn*/(*k* + *n* − 1) |
| AMAT | Hit time + miss rate × penalty | Six steps of design | Clarify, estimate, sketch, deep-dive, failures, trade-offs |
| 1 Gb/s for a day | 10.8 TB | Token bucket against leaky bucket | Burst against smooth |
| STAR time split | 20 s, 60 s, 20 s, 10 s | The XYZ bullet | Accomplished X, measured by Y, by doing Z |
:::
:::
:::
:::
