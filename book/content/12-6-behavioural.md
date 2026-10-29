::: {.p12}

## [12.12]{.sec}Behavioural interviews: STAR, Amazon principles and the offer [Must · ■■□]{.tag} {#s12-12}

A behavioural question asks for evidence of past conduct: "Tell me about a time when …". The panel reasons that what you did before is the best predictor of what you will do, so a vague answer fails even when the candidate is capable. Amazon builds its whole loop on this idea, and Google, Microsoft and Cisco use the same format in their managerial and HR rounds. Preparation consists of a small bank of true stories and one structure for telling them.

::: bigidea
A behavioural answer is believed when it is specific, so a story that names your action, a number and a lesson beats a larger story told in generalities.
:::

### STAR and STAR-L

*STAR* is Situation, Task, Action, Result. Situation and Task together take about 20 seconds: where, when, what was at stake, and which part was *yours*. Action takes about 60 seconds and is the core: three concrete steps in the first person. Result takes 20 seconds and carries a number. For failure questions add *L*, the learning (STAR-L), in 10 seconds. A full answer therefore lasts 90 to 120 seconds; for a 30-second version use CAR (Challenge, Action, Result).

<figure>
<svg viewBox="0 0 480 70" width="480">
<rect class="fill" x="20" y="14" width="80" height="26"/>
<rect class="hl" x="100" y="14" width="240" height="26"/><rect class="box" x="100" y="14" width="240" height="26"/>
<rect class="fill" x="340" y="14" width="80" height="26"/>
<rect class="box" x="420" y="14" width="40" height="26"/>
<g class="lbl" text-anchor="middle"><text x="60" y="31">S + T</text><text x="220" y="31">Action: "I" and three steps</text><text x="380" y="31">Result</text><text x="440" y="31">L</text></g>
<g class="sm" text-anchor="middle"><text x="60" y="54">20 s</text><text x="220" y="54">60 s</text><text x="380" y="54">20 s</text><text x="440" y="54">10 s</text></g>
</svg>
<figcaption><b>Figure 12.15</b> The time split of a 110-second STAR-L answer: most of the airtime belongs to what you did.</figcaption>
</figure>

The template below can be filled in the blanks and then spoken aloud until it sounds natural.

> In [semester or internship], our team of [n] was [situation]. I was responsible for [task]. First I [action 1, with a tool or technique], then I [action 2], and when [obstacle] happened I [action 3]. As a result, [number: latency down 40%, three days saved, a grade, adoption]. Next time I would [learning].

::: example
**Prompt: "Tell me about a time you helped a team that was falling behind." The stories here are fictional models; use your own facts.**

*Weak.* "In our final-year project we had some delays, so we all worked hard and managed to finish. It was a good lesson in teamwork."

*Strong.*

1. **S.** Four of us were building an SNMP monitor for the hostel network; two weeks before the demo, the polling module, owned by a teammate, lost about one reply in five.
2. **T.** I was in charge of testing, and the demo date was fixed.
3. **A.** First, I wrote a script that sent 1,000 queries and logged the misses; they clustered after a 2-second timeout. Second, I proposed a longer timeout with two retries and paired with him for an evening to implement it. Third, I added the script to the repository as an automated test so the fault could not return.
4. **R.** Loss fell from about 20% to under 1% over 1,000 queries, and the demo ran without a miss.
5. **L.** I would now run a load test in the first week, not the last.

[Result: the strong version has a measurable problem, three actions that are all "I", a number and a lesson; the weak one has none of these.]{.result}
:::

### The Amazon Leadership Principles

Amazon states sixteen *Leadership Principles*, and every interviewer in a loop owns one or two. A designated *Bar Raiser* from outside the hiring team probes the answers and can veto the offer. In Network Development Engineer loops the principles are mixed into technical rounds too: "tell me about an outage you debugged" tests Dive Deep. The wording below is our paraphrase; read Amazon's own page before the interview.

| # | Principle | Plain meaning | What a fresher's evidence looks like |
|---|---|---|---|
| 1 | Customer Obsession | Start from the user's need, and keep their trust | You changed a design after watching users struggle |
| 2 | Ownership | Treat the whole outcome as yours, beyond your job description | You fixed what nobody assigned to you |
| 3 | Invent and Simplify | Look for a simpler or new way, and accept being misunderstood for a while | You scripted a manual task |
| 4 | Are Right, A Lot | Sound judgement, from data and from seeking views that differ | You changed your mind on evidence |
| 5 | Learn and Be Curious | Keep learning and exploring | You taught yourself a protocol for a project |
| 6 | Hire and Develop the Best | Raise the standard of the people around you | You mentored a junior |
| 7 | Insist on the Highest Standards | Refuse to ship what you know is flawed | You redid work that passed but was fragile |
| 8 | Think Big | Aim for a bolder result than the obvious one | You designed for ten times the load |
| 9 | Bias for Action | Decide when speed matters; most choices can be reversed | You chose with incomplete data and corrected it |
| 10 | Frugality | Do more with less | You used free tools to meet a budget |
| 11 | Earn Trust | Listen, speak candidly, admit mistakes | You owned an error in front of the team |
| 12 | Dive Deep | Know the details; audit the data | You root-caused a fault using packet captures |
| 13 | Have Backbone; Disagree and Commit | Challenge respectfully, then commit fully | You objected, lost the vote and delivered anyway |
| 14 | Deliver Results | Meet commitments despite obstacles | You shipped by the deadline despite a setback |
| 15 | Strive to be Earth's Best Employer | Create a safe, productive, inclusive place | You made a team meeting work for quieter members |
| 16 | Success and Scale Bring Broad Responsibility | Consider the wider effects of what you build | You considered privacy or misuse in a project |

### Building the story bank

Eight true stories, each tagged to two to four principles, cover most questions; two spares are kept for later rounds, because the interviewers in one loop each look for a fresh story. Mine them from projects, internships, hackathons, club work, lab incidents, sport and part-time work. Quantify each (hours saved, latency, users, marks).

| # | Theme | Primary | Secondary | Prompt it answers |
|---|---|---|---|---|
| S1 | Helped a user | Customer Obsession | Earn Trust, Deliver Results | "Beyond what was asked" |
| S2 | Beyond my role | Ownership | Bias for Action | "Took on something not yours" |
| S3 | Root-caused an outage | Dive Deep | Highest Standards | "Used data to find the cause" |
| S4 | Failure and recovery | Learn and Be Curious, Earn Trust | Ownership | "A time you failed" |
| S5 | Disagreed with a peer | Have Backbone; Disagree and Commit | Earn Trust | "Disagreed with a senior" |
| S6 | Decided with little data | Bias for Action | Are Right, A Lot | "Incomplete information" |
| S7 | Automated a manual task | Invent and Simplify | Frugality, Deliver Results | "Found a simpler way" |
| S8 | Raised the quality bar | Insist on the Highest Standards | Hire and Develop the Best | "Refused to compromise" |

<figure>
<svg viewBox="0 0 480 168" width="480">
<text class="sm" x="160" y="18" text-anchor="middle">1</text>
<text class="sm" x="180" y="18" text-anchor="middle">2</text>
<text class="sm" x="200" y="18" text-anchor="middle">3</text>
<text class="sm" x="220" y="18" text-anchor="middle">4</text>
<text class="sm" x="240" y="18" text-anchor="middle">5</text>
<text class="sm" x="260" y="18" text-anchor="middle">6</text>
<text class="sm" x="280" y="18" text-anchor="middle">7</text>
<text class="sm" x="300" y="18" text-anchor="middle">8</text>
<text class="sm" x="320" y="18" text-anchor="middle">9</text>
<text class="sm" x="340" y="18" text-anchor="middle">10</text>
<text class="sm" x="360" y="18" text-anchor="middle">11</text>
<text class="sm" x="380" y="18" text-anchor="middle">12</text>
<text class="sm" x="400" y="18" text-anchor="middle">13</text>
<text class="sm" x="420" y="18" text-anchor="middle">14</text>
<text class="sm" x="440" y="18" text-anchor="middle">15</text>
<text class="sm" x="460" y="18" text-anchor="middle">16</text>
<text class="lbl" x="4" y="36">S1 Helped a user</text>
<rect class="box" x="150" y="26" width="20" height="14"/>
<circle class="accf" cx="160" cy="33" r="4"/>
<rect class="box" x="170" y="26" width="20" height="14"/>
<rect class="box" x="190" y="26" width="20" height="14"/>
<rect class="box" x="210" y="26" width="20" height="14"/>
<rect class="box" x="230" y="26" width="20" height="14"/>
<rect class="box" x="250" y="26" width="20" height="14"/>
<rect class="box" x="270" y="26" width="20" height="14"/>
<rect class="box" x="290" y="26" width="20" height="14"/>
<rect class="box" x="310" y="26" width="20" height="14"/>
<rect class="box" x="330" y="26" width="20" height="14"/>
<rect class="box" x="350" y="26" width="20" height="14"/>
<circle class="acc" cx="360" cy="33" r="3.5"/>
<rect class="box" x="370" y="26" width="20" height="14"/>
<rect class="box" x="390" y="26" width="20" height="14"/>
<rect class="box" x="410" y="26" width="20" height="14"/>
<circle class="acc" cx="420" cy="33" r="3.5"/>
<rect class="box" x="430" y="26" width="20" height="14"/>
<rect class="box" x="450" y="26" width="20" height="14"/>
<text class="lbl" x="4" y="50">S2 Beyond my role</text>
<rect class="box" x="150" y="40" width="20" height="14"/>
<rect class="box" x="170" y="40" width="20" height="14"/>
<circle class="accf" cx="180" cy="47" r="4"/>
<rect class="box" x="190" y="40" width="20" height="14"/>
<rect class="box" x="210" y="40" width="20" height="14"/>
<rect class="box" x="230" y="40" width="20" height="14"/>
<rect class="box" x="250" y="40" width="20" height="14"/>
<rect class="box" x="270" y="40" width="20" height="14"/>
<rect class="box" x="290" y="40" width="20" height="14"/>
<rect class="box" x="310" y="40" width="20" height="14"/>
<circle class="acc" cx="320" cy="47" r="3.5"/>
<rect class="box" x="330" y="40" width="20" height="14"/>
<rect class="box" x="350" y="40" width="20" height="14"/>
<rect class="box" x="370" y="40" width="20" height="14"/>
<rect class="box" x="390" y="40" width="20" height="14"/>
<rect class="box" x="410" y="40" width="20" height="14"/>
<rect class="box" x="430" y="40" width="20" height="14"/>
<rect class="box" x="450" y="40" width="20" height="14"/>
<text class="lbl" x="4" y="64">S3 Root-caused an outage</text>
<rect class="box" x="150" y="54" width="20" height="14"/>
<rect class="box" x="170" y="54" width="20" height="14"/>
<rect class="box" x="190" y="54" width="20" height="14"/>
<rect class="box" x="210" y="54" width="20" height="14"/>
<rect class="box" x="230" y="54" width="20" height="14"/>
<rect class="box" x="250" y="54" width="20" height="14"/>
<rect class="box" x="270" y="54" width="20" height="14"/>
<circle class="acc" cx="280" cy="61" r="3.5"/>
<rect class="box" x="290" y="54" width="20" height="14"/>
<rect class="box" x="310" y="54" width="20" height="14"/>
<rect class="box" x="330" y="54" width="20" height="14"/>
<rect class="box" x="350" y="54" width="20" height="14"/>
<rect class="box" x="370" y="54" width="20" height="14"/>
<circle class="accf" cx="380" cy="61" r="4"/>
<rect class="box" x="390" y="54" width="20" height="14"/>
<rect class="box" x="410" y="54" width="20" height="14"/>
<rect class="box" x="430" y="54" width="20" height="14"/>
<rect class="box" x="450" y="54" width="20" height="14"/>
<text class="lbl" x="4" y="78">S4 Failure and recovery</text>
<rect class="box" x="150" y="68" width="20" height="14"/>
<rect class="box" x="170" y="68" width="20" height="14"/>
<circle class="acc" cx="180" cy="75" r="3.5"/>
<rect class="box" x="190" y="68" width="20" height="14"/>
<rect class="box" x="210" y="68" width="20" height="14"/>
<rect class="box" x="230" y="68" width="20" height="14"/>
<circle class="accf" cx="240" cy="75" r="4"/>
<rect class="box" x="250" y="68" width="20" height="14"/>
<rect class="box" x="270" y="68" width="20" height="14"/>
<rect class="box" x="290" y="68" width="20" height="14"/>
<rect class="box" x="310" y="68" width="20" height="14"/>
<rect class="box" x="330" y="68" width="20" height="14"/>
<rect class="box" x="350" y="68" width="20" height="14"/>
<circle class="accf" cx="360" cy="75" r="4"/>
<rect class="box" x="370" y="68" width="20" height="14"/>
<rect class="box" x="390" y="68" width="20" height="14"/>
<rect class="box" x="410" y="68" width="20" height="14"/>
<rect class="box" x="430" y="68" width="20" height="14"/>
<rect class="box" x="450" y="68" width="20" height="14"/>
<text class="lbl" x="4" y="92">S5 Disagreed with a peer</text>
<rect class="box" x="150" y="82" width="20" height="14"/>
<rect class="box" x="170" y="82" width="20" height="14"/>
<rect class="box" x="190" y="82" width="20" height="14"/>
<rect class="box" x="210" y="82" width="20" height="14"/>
<rect class="box" x="230" y="82" width="20" height="14"/>
<rect class="box" x="250" y="82" width="20" height="14"/>
<rect class="box" x="270" y="82" width="20" height="14"/>
<rect class="box" x="290" y="82" width="20" height="14"/>
<rect class="box" x="310" y="82" width="20" height="14"/>
<rect class="box" x="330" y="82" width="20" height="14"/>
<rect class="box" x="350" y="82" width="20" height="14"/>
<circle class="acc" cx="360" cy="89" r="3.5"/>
<rect class="box" x="370" y="82" width="20" height="14"/>
<rect class="box" x="390" y="82" width="20" height="14"/>
<circle class="accf" cx="400" cy="89" r="4"/>
<rect class="box" x="410" y="82" width="20" height="14"/>
<rect class="box" x="430" y="82" width="20" height="14"/>
<rect class="box" x="450" y="82" width="20" height="14"/>
<text class="lbl" x="4" y="106">S6 Decided with little data</text>
<rect class="box" x="150" y="96" width="20" height="14"/>
<rect class="box" x="170" y="96" width="20" height="14"/>
<rect class="box" x="190" y="96" width="20" height="14"/>
<rect class="box" x="210" y="96" width="20" height="14"/>
<circle class="acc" cx="220" cy="103" r="3.5"/>
<rect class="box" x="230" y="96" width="20" height="14"/>
<rect class="box" x="250" y="96" width="20" height="14"/>
<rect class="box" x="270" y="96" width="20" height="14"/>
<rect class="box" x="290" y="96" width="20" height="14"/>
<rect class="box" x="310" y="96" width="20" height="14"/>
<circle class="accf" cx="320" cy="103" r="4"/>
<rect class="box" x="330" y="96" width="20" height="14"/>
<rect class="box" x="350" y="96" width="20" height="14"/>
<rect class="box" x="370" y="96" width="20" height="14"/>
<rect class="box" x="390" y="96" width="20" height="14"/>
<rect class="box" x="410" y="96" width="20" height="14"/>
<rect class="box" x="430" y="96" width="20" height="14"/>
<rect class="box" x="450" y="96" width="20" height="14"/>
<text class="lbl" x="4" y="120">S7 Automated a manual task</text>
<rect class="box" x="150" y="110" width="20" height="14"/>
<rect class="box" x="170" y="110" width="20" height="14"/>
<rect class="box" x="190" y="110" width="20" height="14"/>
<circle class="accf" cx="200" cy="117" r="4"/>
<rect class="box" x="210" y="110" width="20" height="14"/>
<rect class="box" x="230" y="110" width="20" height="14"/>
<rect class="box" x="250" y="110" width="20" height="14"/>
<rect class="box" x="270" y="110" width="20" height="14"/>
<rect class="box" x="290" y="110" width="20" height="14"/>
<rect class="box" x="310" y="110" width="20" height="14"/>
<rect class="box" x="330" y="110" width="20" height="14"/>
<circle class="acc" cx="340" cy="117" r="3.5"/>
<rect class="box" x="350" y="110" width="20" height="14"/>
<rect class="box" x="370" y="110" width="20" height="14"/>
<rect class="box" x="390" y="110" width="20" height="14"/>
<rect class="box" x="410" y="110" width="20" height="14"/>
<circle class="acc" cx="420" cy="117" r="3.5"/>
<rect class="box" x="430" y="110" width="20" height="14"/>
<rect class="box" x="450" y="110" width="20" height="14"/>
<text class="lbl" x="4" y="134">S8 Raised the quality bar</text>
<rect class="box" x="150" y="124" width="20" height="14"/>
<rect class="box" x="170" y="124" width="20" height="14"/>
<rect class="box" x="190" y="124" width="20" height="14"/>
<rect class="box" x="210" y="124" width="20" height="14"/>
<rect class="box" x="230" y="124" width="20" height="14"/>
<rect class="box" x="250" y="124" width="20" height="14"/>
<circle class="acc" cx="260" cy="131" r="3.5"/>
<rect class="box" x="270" y="124" width="20" height="14"/>
<circle class="accf" cx="280" cy="131" r="4"/>
<rect class="box" x="290" y="124" width="20" height="14"/>
<rect class="box" x="310" y="124" width="20" height="14"/>
<rect class="box" x="330" y="124" width="20" height="14"/>
<rect class="box" x="350" y="124" width="20" height="14"/>
<rect class="box" x="370" y="124" width="20" height="14"/>
<rect class="box" x="390" y="124" width="20" height="14"/>
<rect class="box" x="410" y="124" width="20" height="14"/>
<rect class="box" x="430" y="124" width="20" height="14"/>
<rect class="box" x="450" y="124" width="20" height="14"/>
<text class="sm" x="150" y="154">filled = primary principle, open = secondary; numbers follow the table above</text>
</svg>
<figcaption><b>Figure 12.16</b> The story-by-principle matrix, with example entries. A complete bank has every principle from 1 to 16 covered at least once.</figcaption>
</figure>

One story serves several principles by changing the angle, not the facts. The SNMP story above, for example, is told for *Ownership* by stressing that the polling module was not yours, for *Dive Deep* by stressing the 1,000-query log and the clustering of misses, and for *Deliver Results* by stressing the fixed demo date.

::: trap
*Claim:* "We" is more modest and therefore better. *Why it is wrong:* the panel is hiring you, and a story told in "we" gives no evidence of what you did. *Correct statement:* say "we" for the situation and "I" for every action; add the team's result and your own share of it.
:::

### "Tell me about yourself"

This question opens most interviews, and the usual error is to recite a résumé. Use *Present, Past, Future*, in 60 to 90 seconds.

> I am [name], a final-year [branch] student at [college]. **Present:** I am focused on networking and systems; I [one project in one line, with a number]. **Past:** I got here through [an internship, CCNA, research or competitive programming: one or two proofs]. **Future:** I am drawn to [company]'s [specific product] because [link to your skills]. That is why I applied for this role.

Vary the lead by round: the technical round opens with the project to be questioned; the managerial round opens with impact and teamwork; the HR round adds one personal trait with evidence. The "Future" line is what makes the answer yours.

| Company | Products to name in the "Future" line |
|---|---|
| Cisco | Catalyst and Meraki switching and Wi-Fi, SD-WAN, Webex |
| Juniper | Junos, Mist AI-driven wireless and wired |
| Qualcomm | Snapdragon modems and connectivity (Wi-Fi, 5G) |
| Arista | EOS, CloudVision, cloud-scale data-centre switching |
| Amazon | AWS backbone, VPC and Transit Gateway |
| Microsoft | Azure networking and the global WAN |
| Nokia | SR Linux, IP routing and optical |
| Broadcom | Switch silicon for data centres |

### Common HR questions and answer frames

| Question | Frame |
|---|---|
| Why this company? | One product or team, one skill of yours it needs, one thing you want to learn |
| Why networking? | A moment that hooked you (a lab, an outage), then the scale of the field |
| Strengths | Two, each with a one-line example |
| Weakness | A real one, plus what you do about it (never "I work too hard") |
| Where in five years? | Deeper technical ownership of a network, possibly leading a small team |
| Relocation, shifts, on-call, bond | Answer honestly; networking operations often involve on-call, so show you understand |
| A conflict | A story from S5, ending in a working relationship |
| Why should we hire you? | Skills matched to the job description, with one proof |
| Higher studies | Honest, with a commitment signal ("I plan to work for several years first") |
| Salary expectation (fresher) | "I would like the company's standard for this role; I am focused on the work" |
| Questions for us | On-call load, the team's tools, how success is measured at six months |

### Offers in India

A fresher's offer is a bundle, not a number. *CTC* (cost to company) includes items that never reach you as cash: the employer's provident-fund share, insurance, gratuity, and bonuses that depend on performance. Separate these before comparing.

| Component | Offer A, "₹30 LPA" | Offer B, "₹24 LPA" |
|---|---|---|
| Fixed base | ₹20 L | ₹24 L |
| Variable pay (stated) | ₹6 L | none |
| One-time joining bonus | ₹4 L (clawback if you leave within two years) | none |
| Recurring cash if variable pays 80% | 20 + 4.8 = ₹24.8 L | ₹24 L |
| First-year cash | 24.8 + 4 = ₹28.8 L | ₹24 L |
| Recurring cash if variable pays 50% | 20 + 3 = ₹23 L | ₹24 L |

Offer A is better in year one and, at 80% payout, in later years by ₹0.8 L; at 50% payout it is worse by ₹1 L every year. Hence compute *guaranteed annual cash* separately from the headline, and ask what the variable actually paid last year. Other warning signs are variable pay above 30% of CTC, shares in an unlisted start-up counted at face value, service bonds, and long clawbacks.

On-campus offers are usually fixed by the company and not negotiable on base, and some placement cells forbid holding two offers, so read the policy first. Off-campus and lateral offers can move on the joining bonus, the joining date, location or team, the share grant, and a written review date. Choose one or two items that matter to you. The script is: thank them, state enthusiasm, give one competing offer or market data, ask for one specific number, and stop speaking. Let the company name the figure first where possible.

::: lens
[AMAZON · GOOGLE · MICROSOFT · CISCO]{.co}

Amazon scores each answer against its principle and asks follow-ups until the story is exhausted: "What was your part?", "What was the data?", "What would you do differently?" Prepare one fact for each. Google and Microsoft look for collaboration and growth; Cisco's managerial round adds relocation, flexibility and project depth. Model answers to the standard prompts are in [Q12.41 to Q12.50](#ps12){.ref}.
:::

::: check
1. How many seconds of a 110-second answer should be Action? [^c12h-1]
2. Offer: base ₹18 L, variable ₹4 L paid at 75%, no bonus. Recurring cash? [^c12h-2]
3. Rewrite "We fixed the bug" so that it shows your action. [^c12h-3]
:::

[^c12h-1]: About 60 seconds, a little over half.
[^c12h-2]: 18 + 0.75 × 4 = ₹21 L.
[^c12h-3]: "I reproduced the fault with a packet capture, found the missing retransmission timer and patched it."

:::
