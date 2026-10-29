::: {.p12}

## [12.4]{.sec}Work, pipes, speed, trains and boats [Must · ■□□]{.tag} {#s12-4}

All five topics in this section are rate problems: a quantity done per unit of time. Work per day, water per hour and distance per hour obey the same equation, quantity = rate × time, so one habit serves them all: convert every statement into a rate before combining.

#### Formula card: time and work

- If A alone takes *a* days, A's rate is 1/*a* of the job per day. Rates add when people work together.
- A and B together: *ab*/(*a* + *b*) days.
- LCM method: take total work as the LCM of the days; each person's rate becomes a whole number of units per day.
- Pipes: a filling pipe has a positive rate, an emptying pipe or leak a negative rate; sum them.
- Man-days: M<sub>1</sub>D<sub>1</sub>H<sub>1</sub>/W<sub>1</sub> = M<sub>2</sub>D<sub>2</sub>H<sub>2</sub>/W<sub>2</sub>.

**Shortcut.** The LCM method removes fractions: for 10 and 15 days, assume 30 units; A does 3 per day and B does 2.

::: example
**A can finish a job in 10 days and B in 15 days. All three of A, B and C together finish in 5 days. How long would C take alone?**

1. Take the work as LCM(10, 15, 5) = 30 units. A does 3 per day and B does 2 per day.
2. A, B and C together do 30/5 = 6 per day, so C does 6 − 3 − 2 = 1 per day.
3. C alone: 30/1 days.

[Result: 30 days.]{.result}
:::

::: example
**A can do a job in 20 days and B in 30 days. They start together, but A leaves after 6 days. How long does the whole job take?**

1. Work = 60 units; A does 3 per day and B does 2 per day.
2. In 6 days together: 6 × 5 = 30 units, leaving 30.
3. B alone does 30 units in 15 days.

[Result: 6 + 15 = 21 days.]{.result}
:::

::: example
**Pipe A fills a tank in 6 hours and pipe B in 8 hours. Pipe C empties it in 12 hours. With all three open, how long to fill the empty tank?**

1. Capacity = LCM(6, 8, 12) = 24 units. A adds 4 per hour, B adds 3, C removes 2.
2. Net rate = 4 + 3 − 2 = 5 units per hour.
3. Time = 24/5.

[Result: 4.8 hours, which is 4 hours 48 minutes.]{.result}
:::

::: example
**A tank fills in 4 hours, but because of a leak it takes 5 hours. How long does the leak alone take to empty a full tank?**

1. Filling rate 1/4 per hour; with the leak 1/5 per hour.
2. Leak rate = 1/4 − 1/5 = 1/20 per hour.

[Result: 20 hours.]{.result}
:::

#### Formula card: time, speed and distance

- Distance = speed × time. Convert km/h to m/s by multiplying by 5/18, and back by 18/5.
- Average speed over equal distances at speeds *x* and *y*: 2*xy*/(*x* + *y*), the harmonic mean. It is not (*x* + *y*)/2. Over equal times it is the arithmetic mean.
- Relative speed: same direction subtract, opposite directions add.
- Catching up: time = initial gap / relative speed.

**Shortcut.** If the speed ratio is *a* : *b* over the same distance, the time ratio is *b* : *a*.

::: example
**A car goes to a city at 60 km/h and returns at 40 km/h. Find the average speed.**

1. Equal distances, so use the harmonic mean: 2 × 60 × 40 / (60 + 40) = 4,800/100.
2. Check with 120 km each way: time 2 h + 3 h = 5 h for 240 km, giving 48 km/h.

[Result: 48 km/h.]{.result}
:::

::: example
**Train X leaves a station at 30 km/h. Two hours later train Y leaves the same station on the same track at 50 km/h. When does Y catch X?**

1. X's head start: 30 × 2 = 60 km.
2. Relative speed: 50 − 30 = 20 km/h.
3. Time after Y departs: 60/20.

[Result: 3 hours after Y leaves, at distance 150 km.]{.result}
:::

#### Formula card: trains, boats and streams

- A train passing a pole or a person covers its own length. Passing a platform or bridge, it covers (train + platform).
- Two trains crossing: the distance is the sum of the lengths, the speed is the relative speed.
- Boat in still water *u*, stream *v*: downstream *u* + *v*, upstream *u* − *v*. Hence *u* = (down + up)/2 and *v* = (down − up)/2.

<figure>
<svg viewBox="0 0 480 110" width="480">
<defs><marker id="a124" viewBox="0 0 6 6" refX="5" refY="3" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L6 3L0 6z" fill="#1A1D23"/></marker></defs>
<rect class="fill" x="150" y="52" width="250" height="14"/>
<text class="sm" x="275" y="62" text-anchor="middle">platform (P)</text>
<rect class="box" x="60" y="34" width="90" height="18"/>
<text class="lbl" x="105" y="47" text-anchor="middle">train (L)</text>
<line class="ln" x1="150" y1="34" x2="150" y2="76"/>
<line class="acc" x1="60" y1="84" x2="400" y2="84"/>
<line class="ln" x1="60" y1="78" x2="60" y2="90"/>
<line class="ln" x1="400" y1="78" x2="400" y2="90"/>
<text class="lbl" x="230" y="100" text-anchor="middle">distance covered while crossing = L + P</text>
<line class="ln" x1="75" y1="22" x2="130" y2="22" marker-end="url(#a124)"/>
<text class="sm" x="60" y="25">motion</text>
</svg>
<figcaption><b>Figure 12.2</b> Crossing a platform starts when the front reaches it and ends when the rear leaves it, so the distance is L + P.</figcaption>
</figure>

::: example
**A 240 m train runs at 72 km/h. How long does it take to cross a 360 m platform?**

1. Speed: 72 × 5/18 = 20 m/s.
2. Distance: 240 + 360 = 600 m.
3. Time: 600/20.

[Result: 30 seconds.]{.result}
:::

::: example
**A 200 m train at 60 km/h overtakes a 150 m train moving the same way at 42 km/h. How long does the overtaking take?**

1. Relative speed: 60 − 42 = 18 km/h = 18 × 5/18 = 5 m/s.
2. Distance: 200 + 150 = 350 m.
3. Time: 350/5.

[Result: 70 seconds.]{.result}
:::

::: example
**A boat travels 36 km downstream and returns upstream. Its still-water speed is 15 km/h and the stream is 3 km/h. Total time?**

1. Downstream speed 18 km/h: 36/18 = 2 h.
2. Upstream speed 12 km/h: 36/12 = 3 h.

[Result: 5 hours. The average speed is 72/5 = 14.4 km/h, not 15.]{.result}
:::

::: example
**A boat covers 24 km downstream in 2 hours and 24 km upstream in 3 hours. Find the still-water and stream speeds.**

1. Downstream 24/2 = 12 km/h; upstream 24/3 = 8 km/h.
2. *u* = (12 + 8)/2 = 10; *v* = (12 − 8)/2 = 2.

[Result: boat 10 km/h, stream 2 km/h.]{.result}
:::

::: check
1. A can do a job in 24 days and B in 40. How long together? [^c12b-1]
2. A tap fills a tank in 3 h and another in 6 h; an outlet empties it in 4 h. Time with all open? [^c12b-2]
3. A 100 m train crosses a pole in 10 s. Its speed in km/h? [^c12b-3]
4. A boat's speed in still water is 9 km/h; it takes 4 h to go 20 km upstream. Stream speed? [^c12b-4]
:::

[^c12b-1]: 24 × 40 / 64 = 15 days.
[^c12b-2]: Capacity 12: rates 4 + 2 − 3 = 3 per hour, so 12/3 = 4 hours.
[^c12b-3]: 10 m/s × 18/5 = 36 km/h.
[^c12b-4]: Upstream speed 20/4 = 5 km/h, so *v* = 9 − 5 = 4 km/h.

## [12.5]{.sec}Interest, counting, probability, ages and the calendar [Must · ■■□]{.tag} {#s12-5}

#### Formula card: simple and compound interest

- Simple interest SI = *PRT*/100. Amount A = P + SI.
- Compound interest: A = P(1 + *r*/100)<sup>*n*</sup>; CI = A − P. For half-yearly compounding use rate *r*/2 and 2*n* periods.
- CI − SI for two years = P(*r*/100)<sup>2</sup>; for three years = P(*r*/100)<sup>2</sup>(3 + *r*/100).
- Rule of 72: money doubles in about 72/*r* years at compound rate *r*%.

**Shortcut.** For two years at *r*% the multiplier is 1 + 2*r*/100 + (*r*/100)<sup>2</sup>; at 10% it is 1.21.

::: example
**Find the compound interest and simple interest on ₹10,000 at 10% per annum for 2 years, and verify the difference formula.**

1. SI = 10,000 × 10 × 2 / 100 = ₹2,000.
2. Amount at CI = 10,000 × 1.1<sup>2</sup> = 12,100, so CI = ₹2,100.
3. Difference = 100 = 10,000 × (0.1)<sup>2</sup>.

[Result: CI ₹2,100, SI ₹2,000, difference ₹100.]{.result}
:::

::: example
**₹8,000 is invested at 20% per annum, compounded half-yearly. Find the amount after one year.**

1. Half-yearly rate 10%, two periods.
2. Amount = 8,000 × 1.1 × 1.1.

[Result: ₹9,680 (annual compounding would give ₹9,600).]{.result}
:::

#### Formula card: permutations and combinations

- Permutations (order matters): P(*n*, *r*) = *n*!/(*n* − *r*)!. Combinations: C(*n*, *r*) = *n*!/(*r*!(*n* − *r*)!).
- Arrangements of *n* objects with repeats *p*, *q*: *n*!/(*p*!*q*!).
- Circular arrangements of *n* people: (*n* − 1)!. If two named people must be adjacent: treat them as one block and multiply by 2.
- Objects that must be together: glue them as one block, arrange, then multiply by the internal arrangements.
- Distributing *r* identical items among *k* people (stars and bars): C(*r* + *k* − 1, *k* − 1).
- "At least" counts: add the cases, or subtract the complement from the total.

**Shortcut.** Decide first whether order matters. If a question says "select", "choose" or "committee", use C; if it says "arrange" or "form a number", use P.

::: example
**How many 4-digit numbers can be formed from the digits 1 to 7 with no repetition? How many are even?**

1. All: P(7, 4) = 7 × 6 × 5 × 4 = 840.
2. Even: the units digit is 2, 4 or 6 (3 choices). The other three places take P(6, 3) = 6 × 5 × 4 = 120 ways.
3. Even numbers: 3 × 120.

[Result: 840 numbers, of which 360 are even.]{.result}
:::

::: example
**A committee of 4 is chosen from 6 men and 4 women with at least 2 women. How many committees?**

1. Two women and two men: C(4, 2) × C(6, 2) = 6 × 15 = 90.
2. Three women and one man: C(4, 3) × C(6, 1) = 4 × 6 = 24.
3. Four women: C(4, 4) = 1.

[Result: 90 + 24 + 1 = 115.]{.result}
:::

#### Formula card: probability

- P(event) = favourable / total, for equally likely outcomes. Two dice have 36 outcomes; a deck has 52 cards (4 suits, 12 face cards); *n* coins have 2<sup>*n*</sup> outcomes.
- Complement: P(at least one) = 1 − P(none). Independent events multiply; mutually exclusive events add.
- Conditional: P(A | B) = P(A and B)/P(B). Without replacement, probabilities change after each draw.

**Shortcut.** The words "at least one" almost always mean: compute the complement.

::: example
**Two fair dice are thrown. What is the probability that the sum is 8?**

1. Pairs summing to 8: (2,6), (3,5), (4,4), (5,3), (6,2), which is 5 pairs.
2. Total pairs: 36.

[Result: 5/36.]{.result}
:::

::: example
**A bag has 5 red, 3 blue and 2 green balls. Three are drawn at random. What is the probability that at least one is red?**

1. Complement: no red, so all three come from the 5 non-red balls: C(5, 3) = 10.
2. Total ways: C(10, 3) = 120. So P(none) = 10/120 = 1/12.
3. P(at least one red) = 1 − 1/12.

[Result: 11/12.]{.result}
:::

#### Formula card: ages, clocks and calendars

- Ages: write today's ages as ratio parts (5*x*, 3*x*), then add or subtract the years for the other time.
- Clocks: the minute hand moves 6° per minute and the hour hand 0.5° per minute, so the angle at H hours M minutes is |30H − 5.5M|; if above 180° subtract it from 360°. The hands overlap every 720/11 = 65<sup>5</sup>⁄<sub>11</sub> minutes.
- Calendars: 100 years have 5 odd days, 200 years 3, 300 years 1, 400 years 0. An ordinary year has 1 odd day and a leap year 2. An *odd day* is a day beyond whole weeks.

**Shortcut.** Count the days between two dates and take the remainder after dividing by 7.

::: example
**The ratio of the ages of two engineers is 5 : 3. Six years hence it will be 7 : 5. Find their present ages.**

1. Write (5*x* + 6) / (3*x* + 6) = 7/5 and cross-multiply: 25*x* + 30 = 21*x* + 42.
2. Then 4*x* = 12, so *x* = 3.

[Result: 15 and 9 years. Check: 21 : 15 = 7 : 5.]{.result}
:::

::: example
**(a) What is the angle between the hands at 3:40? (b) At what time between 4 and 5 do the hands overlap? (c) If 26 January 2026 is a Monday, what day is 15 August 2026?**

1. (a) |30 × 3 − 5.5 × 40| = |90 − 220| = 130°, which is below 180°.
2. (b) At 4:00 the minute hand is 120° behind. It gains 5.5° per minute, so 120/5.5 = 240/11 = 21<sup>9</sup>⁄<sub>11</sub> minutes.
3. (c) Days from 26 January to 15 August: 5 + 28 + 31 + 30 + 31 + 30 + 31 + 15 = 201. Since 201 = 28 × 7 + 5, move five days from Monday.

[Result: (a) 130°; (b) about 4:21:49; (c) Saturday.]{.result}
:::

#### Formula card: mensuration

- Rectangle: area *lb*, perimeter 2(*l* + *b*). Circle: area π*r*<sup>2</sup>, circumference 2π*r*; use π = 22/7 when the radius is a multiple of 7.
- Cuboid: volume *lbh*, surface 2(*lb* + *bh* + *hl*). Cube: volume *a*<sup>3</sup>, surface 6*a*<sup>2</sup>.
- Cylinder: volume π*r*<sup>2</sup>*h*, curved surface 2π*rh*. Cone: volume (1/3)π*r*<sup>2</sup>*h*. Sphere: volume (4/3)π*r*<sup>3</sup>.
- 1 m<sup>3</sup> = 1,000 litres; 1 litre = 1,000 cm<sup>3</sup>.

**Shortcut.** Convert every length to one unit first; most errors are unit errors.

::: example
**A rectangular tank is 4 m long, 3 m wide and 2.5 m deep. How many litres does it hold when full?**

1. Volume = 4 × 3 × 2.5 = 30 m<sup>3</sup>.
2. Each cubic metre is 1,000 litres.

[Result: 30,000 litres.]{.result}
:::

::: example
**A cylindrical cable drum has radius 7 cm and height 20 cm. Find its volume and curved surface area (π = 22/7).**

1. Volume = (22/7) × 7<sup>2</sup> × 20 = 22 × 7 × 20 = 3,080 cm<sup>3</sup>.
2. Curved surface = 2 × (22/7) × 7 × 20 = 880 cm<sup>2</sup>.

[Result: 3,080 cm<sup>3</sup> and 880 cm<sup>2</sup>.]{.result}
:::

::: check
1. A sum of ₹10,000 at 10% compound: find CI − SI over three years. [^c12b-5]
2. Ways to arrange the letters of ROUTER. [^c12b-6]
3. Ways for 6 people to sit at a round table with two named people adjacent. [^c12b-7]
4. Probability of exactly two heads in three tosses. [^c12b-8]
5. A father is three times as old as his son. In 12 years he will be twice as old. Present ages? [^c12b-9]
6. If 1 January 2000 was a Saturday, what day was 1 January 2001? [^c12b-10]
:::

[^c12b-5]: P(r/100)<sup>2</sup>(3 + r/100) = 10,000 × 0.01 × 3.1 = ₹310 (CI 3,310 less SI 3,000).
[^c12b-6]: 6!/2! = 360, since R repeats.
[^c12b-7]: Block the pair: (5 − 1)! × 2 = 48.
[^c12b-8]: C(3, 2)/8 = 3/8.
[^c12b-9]: F = 3S and F + 12 = 2(S + 12) give S = 12 and F = 36.
[^c12b-10]: The year 2000 was a leap year, so 2 odd days: Saturday + 2 = Monday.

:::
