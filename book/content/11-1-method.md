::: {.chapter .p11}
::: opener
[Part III · Pillar 11]{.part-label}

[11]{.num}

# Troubleshooting Methodology {#ch11}

[Given a vague diagram and a one-line complaint, we ask, walk the layers aloud, name the proof, and close with fix, verification and prevention.]{.promise}

1. [11.1 Why method beats memory]{} [MUST]{}
2. [11.2 SCALPEL: the seven-step framework]{} [MUST]{}
3. [11.3 Clarifying questions]{} [MUST]{}
4. [11.4 Strategies: where to start and how to narrow]{} [MUST]{}
5. [11.5 Layer command matrix and reading outputs]{} [MUST]{}
6. [11.6 Symptom look-alikes]{} [MUST]{}
7. [11.7 Incident overlay and post-mortems]{} [SHOULD]{}
8. [11.8 The Case File: eighteen scenarios]{} [MUST · cases 1 to 12]{}
9. [11.9 Mock rounds]{} [SHOULD]{}
:::

This chapter integrates the book. The protocols behind each fault are taught in [Pillar 3](#ch3){.ref} and [Pillar 4](#ch4){.ref}, and the tools (`tcpdump`, `ss`, `mtr`, `iperf3`) in [Pillar 8](#ch8){.ref}; here we teach only the method, the diagnosis, and the commands each case needs, citing the home section whenever a mechanism is used. Every topology belongs to **Campus Net**, the fictional university network of Pillar 4, with its two border routers BR1 and BR2 and its providers ISP-A (AS 100) and ISP-B (AS 200). Candidate reports describe three recurring formats: a deliberately vague diagram in which the candidate must ask questions (Cisco), a spoken troubleshooting scenario scored on structure (Google), and a mixed Linux, BGP and OSPF discussion (Amazon network development engineer loops). We state these as observed patterns, not as official formats.

## [11.1]{.sec}Why method beats memory [Must · ■□□]{.tag} {#s11-1}

::: bigidea
A troubleshooting interview scores the way you reduce uncertainty as much as the answer you reach, because an engineer who cannot show a repeatable method cannot be trusted with a production outage.
:::

[**OPD doctor** — a good doctor takes the history, examines, orders the cheapest decisive test, and only then prescribes. Nobody prescribes antibiotics for "I feel unwell".]{.margin}Memory fails in a case round for a simple reason: the space of faults is larger than any list of them. The same symptom, "the user cannot browse", has a dozen causes at five layers, and the interviewer chooses the cause after hearing your first move. A candidate who recalls forty commands but has no order for them tests at random, while a candidate with a method tests the cheapest hypothesis that splits the possibilities in half. This is the behaviour the rubric below rewards.

| Criterion | Earns the mark | Loses the mark |
|--------------|----------------------------------------|------------------------------|
| Clarification | Restates the symptom, asks three to five questions, states assumptions aloud | Types a command before any question |
| Structure | Names a method and the layer under test at each step | Jumps between layers without saying why |
| Technical depth | Right command, healthy output expected, correct inference | Lists commands without saying what they prove |
| Evidence | Each conclusion rests on a quoted output | "It is probably the firewall" |
| Communication | Thinks aloud in short sentences, summarises | Silence, or an unstructured monologue |
| Closure | Fix, verification, prevention, communication | Stops at the diagnosis |

::: example
**One prompt, two candidates.** The prompt is "Users cannot access the web server."

| Minute | Candidate A | Candidate B |
|--------|----------------------------------------|----------------------------------------|
| 0:00 | "I would check the firewall, DNS, the web service, the switch ports and the routes." | "Let me restate: users get an error opening the site. Which users, which error, since when?" |
| 1:30 | Lists twelve commands, none tied to a hypothesis | Learns: one VLAN, timeout (not refusal), started after yesterday's change; states three hypotheses |
| 4:00 | Asked "what does that show?", cannot say what a healthy output looks like | Pings the gateway, then the server: "gateway answers, so L1 to L3 of this VLAN are intact; I test TCP 443 next" |
| 9:00 | Proposes restarting the web server | Finds the ACL line, fixes it, re-tests, proposes a template check |
| Score | Clarification 0, structure 1, evidence 1, closure 0 | Clarification 4, structure 4, evidence 4, closure 4 |
:::

::: trap
*Claim:* "Ping works, so the network is fine." *Why it is wrong:* ICMP proves only that some ICMP packet crossed the path; the application may use a different port, a different policy, or a different path, and a firewall may treat ICMP separately. *Correct statement:* ping proves reachability for ICMP between those two addresses, nothing more.
:::

::: lens
[CISCO · GOOGLE · AMAZON]{.co}

The question is usually a single sentence ("a user cannot reach the internet"). A strong answer restates it, asks before it acts, names the layer under test, and says what output would change its mind. Likely follow-ups: "what if that command shows the opposite?" and "how would you prevent it?"
:::

::: check
1. Name the first thing a strong candidate does after hearing a one-line complaint. [^c11-1a]
2. Why is "restart it" a weak answer even when it works? [^c11-1b]
:::

[^c11-1a]: Restate the symptom as something measurable and ask clarifying questions, before any command.
[^c11-1b]: It gives no root cause, so the fault recurs, and it hides the evidence needed to prevent it.

## [11.2]{.sec}SCALPEL: the seven-step framework [Must · ■□□]{.tag} {#s11-2}

::: bigidea
SCALPEL is a fixed order, Symptom, Clarify, Assess, Layer walk, Pinpoint, Execute, Lock in, because the cheap checks that remove the most uncertainty must come before the expensive ones.
:::

The order mirrors the surgical safety checklist: the knife is used only after the checks. Each letter has a spoken form, which is what the interviewer hears and scores.

<figure>
<svg viewBox="0 0 480 285" width="480"><defs><marker id="sc1" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" style="fill:var(--accent)"/></marker></defs>
<rect class="box" x="8" y="8" width="430" height="30" rx="2"/>
<text x="24" y="30" style="font:700 19px var(--sans);fill:var(--accent)" text-anchor="middle">S</text>
<text class="lbl" x="48" y="21">Symptom</text><text class="sm" x="48" y="32">Restate it as something measurable</text>
<text class="sm" x="430" y="27" text-anchor="end">30 s</text>
<line class="ln" x1="24" y1="38" x2="24" y2="44" marker-end="url(#sc1)"/>
<rect class="box" x="8" y="44" width="430" height="30" rx="2"/>
<text x="24" y="66" style="font:700 19px var(--sans);fill:var(--accent)" text-anchor="middle">C</text>
<text class="lbl" x="48" y="57">Clarify</text><text class="sm" x="48" y="68">Scope, timeline, precision, environment, evidence</text>
<text class="sm" x="430" y="63" text-anchor="end">2 min</text>
<line class="ln" x1="24" y1="74" x2="24" y2="80" marker-end="url(#sc1)"/>
<rect class="box" x="8" y="80" width="430" height="30" rx="2"/>
<text x="24" y="102" style="font:700 19px var(--sans);fill:var(--accent)" text-anchor="middle">A</text>
<text class="lbl" x="48" y="93">Assess</text><text class="sm" x="48" y="104">Annotate the path; rank three hypotheses</text>
<text class="sm" x="430" y="99" text-anchor="end">1 min</text>
<line class="ln" x1="24" y1="110" x2="24" y2="116" marker-end="url(#sc1)"/>
<rect class="box" x="8" y="116" width="430" height="30" rx="2"/>
<text x="24" y="138" style="font:700 19px var(--sans);fill:var(--accent)" text-anchor="middle">L</text>
<text class="lbl" x="48" y="129">Layer walk</text><text class="sm" x="48" y="140">Command, healthy output expected, inference drawn</text>
<text class="sm" x="430" y="135" text-anchor="end">10-12 min</text>
<line class="ln" x1="24" y1="146" x2="24" y2="152" marker-end="url(#sc1)"/>
<rect class="box" x="8" y="152" width="430" height="30" rx="2"/>
<text x="24" y="174" style="font:700 19px var(--sans);fill:var(--accent)" text-anchor="middle">P</text>
<text class="lbl" x="48" y="165">Pinpoint</text><text class="sm" x="48" y="176">Root cause that explains every symptom</text>
<text class="sm" x="430" y="171" text-anchor="end">1 min</text>
<line class="ln" x1="24" y1="182" x2="24" y2="188" marker-end="url(#sc1)"/>
<rect class="box" x="8" y="188" width="430" height="30" rx="2"/>
<text x="24" y="210" style="font:700 19px var(--sans);fill:var(--accent)" text-anchor="middle">E</text>
<text class="lbl" x="48" y="201">Execute</text><text class="sm" x="48" y="212">Minimal reversible fix; mitigate first</text>
<text class="sm" x="430" y="207" text-anchor="end">1 min</text>
<line class="ln" x1="24" y1="218" x2="24" y2="224" marker-end="url(#sc1)"/>
<rect class="box" x="8" y="224" width="430" height="30" rx="2"/>
<text x="24" y="246" style="font:700 19px var(--sans);fill:var(--accent)" text-anchor="middle">L</text>
<text class="lbl" x="48" y="237">Lock in</text><text class="sm" x="48" y="248">Verify, prevent, communicate</text>
<text class="sm" x="430" y="243" text-anchor="end">2 min</text>
<path class="acc" d="M438,172 L460,172 L460,100 L440,100" marker-end="url(#sc1)"/>
<text class="sm acct" x="468" y="140" transform="rotate(90 468 140)" text-anchor="middle">hypothesis fails: back to A</text>
</svg>
<figcaption><b>Figure 11.1</b> The SCALPEL card. The accent loop is the rule to remember: when a hypothesis fails or explains only part of the evidence, return to Assess, not to a random command.</figcaption>
</figure>

| Step | Say aloud | Do not |
|----------|--------------------------------------------------|----------------------------------|
| Symptom | "So PC-A gets a timeout opening the intranet; let me confirm what 'cannot reach' means." | Accept "slow", "down" or "broken" unmeasured |
| Clarify | "Three questions first: how many users, since when, what changed?" | Ask more than six; the first three carry most information |
| Assess | "Given one VLAN and a change yesterday, I suspect trunk list, SVI or DHCP relay, in that order." | Hold an unranked list of ten |
| Layer walk | "I test the gateway first. A healthy reply shows ...; a timeout would mean ..." | Run a command without saying what healthy looks like |
| Pinpoint | "Root cause: VLAN 20 missing from the trunk; this explains why only SW2 hosts fail." | Stop at the first finding without checking it explains everything |
| Execute | "Add the VLAN with `add`, not by replacing the list; rollback is removing it." | Fix without a rollback, or fix first and ask later |
| Lock in | "Same ping now passes; I would template the trunk and alert on VLAN drift." | End at "it works now" |

The time budget below suits a twenty-minute round. Most of the time belongs to the layer walk, so the first three minutes have to be spent on questions and not on commands.

<figure>
<svg viewBox="0 0 480 52" width="480">
<rect class="fill" x="10.0" y="8" width="11.5" height="22"/><text class="lbl" x="15.8" y="23" text-anchor="middle">S</text><text class="sm" x="15.8" y="43" text-anchor="middle">0.5</text>
<rect class="fill" x="21.5" y="8" width="46.0" height="22"/><text class="lbl" x="44.5" y="23" text-anchor="middle">C</text><text class="sm" x="44.5" y="43" text-anchor="middle">2</text>
<rect class="fill" x="67.5" y="8" width="23.0" height="22"/><text class="lbl" x="79.0" y="23" text-anchor="middle">A</text><text class="sm" x="79.0" y="43" text-anchor="middle">1</text>
<rect class="box" x="90.5" y="8" width="276.0" height="22"/><text class="lbl" x="228.5" y="23" text-anchor="middle">L</text><text class="sm" x="228.5" y="43" text-anchor="middle">12</text>
<rect class="fill" x="366.5" y="8" width="23.0" height="22"/><text class="lbl" x="378.0" y="23" text-anchor="middle">P</text><text class="sm" x="378.0" y="43" text-anchor="middle">1</text>
<rect class="fill" x="389.5" y="8" width="23.0" height="22"/><text class="lbl" x="401.0" y="23" text-anchor="middle">E</text><text class="sm" x="401.0" y="43" text-anchor="middle">1</text>
<rect class="box" x="412.5" y="8" width="57.5" height="22"/><text class="lbl" x="441.2" y="23" text-anchor="middle">L</text><text class="sm" x="441.2" y="43" text-anchor="middle">2.5</text>
<text class="sm" x="470" y="14" text-anchor="end"></text></svg>
<figcaption><b>Figure 11.2</b> Time budget for a twenty-minute round, in minutes. The letters follow Figure 11.1.</figcaption>
</figure>

::: example
**SCALPEL narrated on Case 1.** The prompt is "A user says the internet is down." The case itself, with its commands, is in [Case 1](#c11-1){.ref}; this transcript shows pacing and phrasing.

| Time | Step | Spoken |
|-------|-----|----------------------------------------------------------------------------------------|
| 0:00 | S | "So one user cannot get to websites. Before I touch anything: does 'internet down' mean every site, every protocol?" |
| 0:30 | C | "Is it one user or many? What error text? Does a ping to a public IP work? Did anything change?" |
| 1:45 | A | "Whole VLAN 10, a name-resolution error, the IP ping works, a DHCP scope was edited yesterday. I rank: wrong DNS from DHCP, DNS server down, port 53 filtered." |
| 2:30 | L | "The IP ping succeeded, so L1 to L3 and NAT are proven; I skip them and say so. I test DNS: which server does the client use?" |
| 6:00 | P | "The client points at 192.168.10.53, which does not exist; the real server answers. Wrong option 6 in the VLAN 10 scope explains why only VLAN 10 fails." |
| 7:00 | E | "Correct the scope, renew leases; users can flush the cache meanwhile." |
| 8:00 | L | "Verify a name lookup from two clients; add a post-change test: resolve a name from every scope." |
:::

::: lens
[CISCO · GOOGLE · AMAZON]{.co}

Interviewers often interrupt to test the loop. When told "that command shows the opposite", answer "that rules out ..., so I return to Assess and the next hypothesis is ...". Candidates who show the loop are scored higher than those who guess correctly the first time.
:::

::: check
1. Which SCALPEL step is repeated when a hypothesis fails? [^c11-2a]
2. Why does Pinpoint require explaining the unaffected cases too? [^c11-2b]
:::

[^c11-2a]: Assess: the failed result is evidence, so the hypotheses are re-ranked.
[^c11-2b]: A cause that explains only the failing cases may be a coincidence; one that also explains why others work is much more likely true.

## [11.3]{.sec}Clarifying questions [Must · ■□□]{.tag} {#s11-3}

::: bigidea
The first three minutes of questions decide the next fifteen, because each answer removes whole layers or locations from the search.
:::

[**Railway enquiry** — "Which train, which date, which class?" comes before "Is there a seat?".]{.margin}Five families cover every complaint: *scope* (who and what is affected), *timeline and change* (since when, what changed), *symptom precision* (the exact error), *environment* (the devices and policies on the path), and *evidence* (what can be observed). The card below holds twenty-five questions; in an interview one asks the three to five highest-yield ones, which are usually numbers 1, 6, 8, 12 and 14.

| Family | Questions |
|--------------|--------------------------------------------------------------------------------|
| Scope | (1) How many users, which VLAN, site or building? (2) One application or all? (3) One direction or both? (4) Wired and wireless alike? (5) Who is unaffected, and what do they share? |
| Timeline and change | (6) Since when, and did it ever work? (7) Constant, periodic or random? (8) What changed: configuration, cable, upgrade, new device, certificate, policy? (9) Anything nearby: desk move, maintenance, provider work? (10) Any pattern in time: hourly, busy hours, backups? |
| Symptom precision | (11) Exact error text or code? (12) Does ping work, from which source to which destination? (13) By name or by IP? (14) Timeout, refusal, reset or slowness, and measured how? (15) Which port and protocol? |
| Environment | (16) Which devices are on the path, and can I log in to them? (17) IP plan, VLANs, routing protocol? (18) Firewalls, NAT, VPN, load balancers? (19) Redundancy: second link, ECMP, LAG, first-hop redundancy? (20) Vendors and software versions? |
| Evidence | (21) Which logs, counters and graphs exist? (22) Commands at both ends? (23) Any packet capture or flow record? (24) A known-good comparison: another user, site, or last week? (25) What has been tried already? |

When the interviewer declines to answer, state an assumption instead and continue: "I will assume a single OSPF area and no firewall on the path; tell me if that is wrong." Stated assumptions are scored positively, whereas silent assumptions are scored as guessing.

::: example
**Turning a vague diagram into a scenario.** The Cisco-style prompt gives two LANs, two routers, a switch each and a cloud labelled WAN, with the words "PC-A cannot reach PC-B". Eight questions define it.

<figure>
<svg viewBox="0 0 480 215" width="480">
<g transform="translate(0,0)">
<line class="ln" x1="30" y1="30" x2="105" y2="30"/>
<line class="ln" x1="105" y1="30" x2="185" y2="30"/>
<line class="ln" x1="185" y1="30" x2="270" y2="30"/>
<line class="ln" x1="270" y1="30" x2="350" y2="30"/>
<line class="ln" x1="350" y1="30" x2="420" y2="30"/>
<line class="ln" x1="420" y1="30" x2="465" y2="30"/>
<rect class="box" x="15" y="20" width="30" height="20" rx="1"/><path class="ln" d="M22,44 L38,44"/><rect class="fill" x="19" y="24" width="22" height="11"/>
<text class="lbl" x="30" y="54" text-anchor="middle">PC-A</text>
<rect class="box" x="83" y="19" width="44" height="22" rx="2"/><path class="ln" d="M92,27 L118,27 M114,24 L118,27 L114,30 M118,34 L92,34 M96,31 L92,34 L96,37"/>
<text class="lbl" x="105" y="51" text-anchor="middle">SW1</text>
<circle class="box" cx="185" cy="30" r="13"/><path class="ln" d="M178,30 L192,30 M185,23 L185,37 M180,25 L190,35 M180,35 L190,25"/>
<text class="lbl" x="185" y="53" text-anchor="middle">R1</text>
<path class="box" d="M242,41 C230,41 230,25 244,25 C244,11 268,7 276,19 C288,13 304,25 296,33 C308,35 304,41 294,41 Z"/>
<text class="lbl" x="270" y="53" text-anchor="middle">WAN?</text>
<circle class="box" cx="350" cy="30" r="13"/><path class="ln" d="M343,30 L357,30 M350,23 L350,37 M345,25 L355,35 M345,35 L355,25"/>
<text class="lbl" x="350" y="53" text-anchor="middle">R2</text>
<rect class="box" x="398" y="19" width="44" height="22" rx="2"/><path class="ln" d="M407,27 L433,27 M429,24 L433,27 L429,30 M433,34 L407,34 M411,31 L407,34 L411,37"/>
<text class="lbl" x="420" y="51" text-anchor="middle">SW2</text>
<rect class="box" x="450" y="20" width="30" height="20" rx="1"/><path class="ln" d="M457,44 L473,44"/><rect class="fill" x="454" y="24" width="22" height="11"/>
<text class="lbl" x="465" y="54" text-anchor="middle">PC-B</text>
<text class="sm" x="240" y="88" text-anchor="middle">As given: no addresses, no VLANs, no protocol</text>
</g>
<g transform="translate(0,100)">
<line class="ln" x1="30" y1="30" x2="105" y2="30"/>
<line class="ln" x1="105" y1="30" x2="185" y2="30"/>
<line class="ln" x1="185" y1="30" x2="270" y2="30"/>
<line class="ln" x1="270" y1="30" x2="350" y2="30"/>
<line class="ln" x1="350" y1="30" x2="420" y2="30"/>
<line class="ln" x1="420" y1="30" x2="465" y2="30"/>
<text class="sm" x="156" y="26" text-anchor="middle">Gi0/1</text>
<text class="sm" x="226" y="26" text-anchor="middle">10.0.0.1/30</text>
<text class="sm" x="309" y="26" text-anchor="middle">10.0.0.2/30</text>
<text class="sm" x="379" y="26" text-anchor="middle">Gi0/1</text>
<rect class="box" x="15" y="20" width="30" height="20" rx="1"/><path class="ln" d="M22,44 L38,44"/><rect class="fill" x="19" y="24" width="22" height="11"/>
<text class="lbl" x="30" y="54" text-anchor="middle">PC-A</text>
<text class="sm" x="30" y="63" text-anchor="middle">192.168.1.10</text>
<rect class="box" x="83" y="19" width="44" height="22" rx="2"/><path class="ln" d="M92,27 L118,27 M114,24 L118,27 L114,30 M118,34 L92,34 M96,31 L92,34 L96,37"/>
<text class="lbl" x="105" y="51" text-anchor="middle">SW1</text>
<text class="sm" x="105" y="60" text-anchor="middle">VLAN 20</text>
<circle class="box" cx="185" cy="30" r="13"/><path class="ln" d="M178,30 L192,30 M185,23 L185,37 M180,25 L190,35 M180,35 L190,25"/>
<text class="lbl" x="185" y="53" text-anchor="middle">R1</text>
<text class="sm" x="185" y="62" text-anchor="middle">.1 gateway</text>
<path class="box" d="M242,41 C230,41 230,25 244,25 C244,11 268,7 276,19 C288,13 304,25 296,33 C308,35 304,41 294,41 Z"/>
<text class="lbl" x="270" y="53" text-anchor="middle">WAN</text>
<text class="sm" x="270" y="62" text-anchor="middle">OSPF area 0</text>
<circle class="box" cx="350" cy="30" r="13"/><path class="ln" d="M343,30 L357,30 M350,23 L350,37 M345,25 L355,35 M345,35 L355,25"/>
<text class="lbl" x="350" y="53" text-anchor="middle">R2</text>
<text class="sm" x="350" y="62" text-anchor="middle">.1 on Gi0/1.60</text>
<rect class="box" x="398" y="19" width="44" height="22" rx="2"/><path class="ln" d="M407,27 L433,27 M429,24 L433,27 L429,30 M433,34 L407,34 M411,31 L407,34 L411,37"/>
<text class="lbl" x="420" y="51" text-anchor="middle">SW2</text>
<text class="sm" x="420" y="60" text-anchor="middle">VLAN 60</text>
<rect class="box" x="450" y="20" width="30" height="20" rx="1"/><path class="ln" d="M457,44 L473,44"/><rect class="fill" x="454" y="24" width="22" height="11"/>
<text class="lbl" x="465" y="54" text-anchor="middle">PC-B</text>
<text class="sm" x="465" y="63" text-anchor="middle">192.168.60.20</text>
<text class="sm acct" x="240" y="88" text-anchor="middle">After eight questions: addressed, routed, no firewall in path</text>
</g>
</svg>
<figcaption><b>Figure 11.3</b> The vague diagram as given (top) and after eight questions (bottom). The addresses are as designed; what PC-B actually has is not yet known.</figcaption>
</figure>

| Candidate asks | Interviewer answers |
|-----------------------------------|------------------------------------------------------------|
| Addresses and gateways? | PC-A 192.168.1.10/24, gateway R1 .1; PC-B should be 192.168.60.20/24, gateway R2 .1 |
| What exactly fails? | Ping from PC-A to PC-B times out; nothing else tested |
| Does PC-A reach anything behind R2? | Yes, the file server 192.168.50.5 in VLAN 50 |
| Did it ever work? | PC-B was connected for the first time this morning, in the new VLAN 60 |
| How are R1 and R2 joined, and which protocol? | Provider Layer 2 circuit, 10.0.0.0/30, OSPF area 0; no firewall |
| What changed? | SW2 and R2 were configured for VLAN 60 yesterday |
| How does R2 reach SW2? | One trunk, one sub-interface per VLAN |
| May I see outputs on SW2 and R2? | Yes, on request |

[Result: the WAN is proven by the file server; the search narrows to PC-B, SW2 and R2's VLAN 60 sub-interface. [Mock round 1](#s11-9){.ref} continues from here.]{.result}
:::

::: lens
[CISCO · JUNIPER · GOOGLE]{.co}

For a vague diagram, candidates report being scored mainly on whether they define the scenario before proposing anything. A strong answer ends the clarifying phase with a one-sentence summary: "so the WAN works, PC-B is new, and the fault is local to VLAN 60 on SW2 or R2".
:::

::: check
1. Which two questions in the table separate "the network" from "one device"? [^c11-3a]
2. What do you do if the interviewer says "assume anything"? [^c11-3b]
:::

[^c11-3a]: "Does PC-A reach anything behind R2?" and "Did it ever work?" prove the WAN and the age of the fault.
[^c11-3b]: State the assumptions aloud, in a list of two or three, then proceed and revisit them if evidence contradicts one.

## [11.4]{.sec}Strategies: where to start and how to narrow [Must · ■□□]{.tag} {#s11-4}

::: bigidea
The best starting point is the one that discards the largest part of the search space with one test, so the strategy depends on what is already known about the fault.
:::

[**Diwali lights** — to find one dead bulb in a long string, test the middle first and discard half; the same binary search works on a path of routers.]{.margin}Six strategies are in common use. None is correct in general, so the skill lies in choosing, and in saying why.

| Strategy | Start | Use when | Risk |
|----------------|----------------------------|----------------------------|------------------------|
| Bottom-up | Cable, port, link state (L1), then upward | A physical change, a new link, intermittent loss | Slow when the fault is in the application |
| Top-down | Application error, then downward | One application fails and others work | Misses a path problem that hits only that port |
| Divide and conquer | `ping` the gateway or the middle hop (L3), then go up or down | Many hops, no other clue; the default | Needs access to several devices |
| Follow the packet | `traceroute`, then each device's forwarding decision along the way | A multi-hop path, routing suspected | Forward path may differ from the return path |
| Compare with working | Diff the failing and the working user, site or configuration | One of two similar things fails | A shared cause is missed |
| Swap or isolate | Replace the cable, optic or port with a known-good one | Hardware suspected after counters or light levels point to it | Destroys evidence if done first |

<figure>
<svg viewBox="0 0 480 215" width="480"><defs><marker id="st1" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#1A1D23"/></marker></defs>
<rect class="box" x="8" y="8" width="250" height="34" rx="2"/><text class="lbl" x="18" y="29">Physical change, new cable or hardware suspected?</text>
<line class="ln" x1="258" y1="25" x2="300" y2="25" marker-end="url(#st1)"/><text class="sm" x="279" y="21" text-anchor="middle">yes</text>
<rect class="fill" x="302" y="8" width="170" height="34" rx="2"/><text class="lbl" x="387" y="29" text-anchor="middle">Bottom-up, or swap the part</text>
<line class="ln" x1="133" y1="42" x2="133" y2="58" marker-end="url(#st1)"/><text class="sm" x="140" y="53">no</text>
<rect class="box" x="8" y="58" width="250" height="34" rx="2"/><text class="lbl" x="18" y="79">One user or site works, another fails?</text>
<line class="ln" x1="258" y1="75" x2="300" y2="75" marker-end="url(#st1)"/><text class="sm" x="279" y="71" text-anchor="middle">yes</text>
<rect class="fill" x="302" y="58" width="170" height="34" rx="2"/><text class="lbl" x="387" y="79" text-anchor="middle">Compare with the working case</text>
<line class="ln" x1="133" y1="92" x2="133" y2="108" marker-end="url(#st1)"/><text class="sm" x="140" y="103">no</text>
<rect class="box" x="8" y="108" width="250" height="34" rx="2"/><text class="lbl" x="18" y="129">Complaint names one application?</text>
<line class="ln" x1="258" y1="125" x2="300" y2="125" marker-end="url(#st1)"/><text class="sm" x="279" y="121" text-anchor="middle">yes</text>
<rect class="fill" x="302" y="108" width="170" height="34" rx="2"/><text class="lbl" x="387" y="129" text-anchor="middle">Top-down from the application</text>
<line class="ln" x1="133" y1="142" x2="133" y2="158" marker-end="url(#st1)"/><text class="sm" x="140" y="153">no</text>
<rect class="box" x="8" y="158" width="250" height="34" rx="2"/><text class="lbl" x="18" y="179">Many hops, access to several devices?</text>
<line class="ln" x1="258" y1="175" x2="300" y2="175" marker-end="url(#st1)"/><text class="sm" x="279" y="171" text-anchor="middle">yes</text>
<rect class="fill" x="302" y="158" width="170" height="34" rx="2"/><text class="lbl" x="387" y="179" text-anchor="middle">Divide and conquer from L3</text>
<line class="ln" x1="133" y1="192" x2="133" y2="203"/><text class="sm" x="140" y="210">no: default is divide and conquer from L3</text></svg>
<figcaption><b>Figure 11.4</b> Strategy chooser. The default is divide and conquer from Layer 3.</figcaption>
</figure>

::: example
**The same fault with four strategies.** Campus Net has a six-device path: PC, SW1, R1, R2, R3 and a server. The link between R2 and R3 is administratively down because an engineer shut the wrong interface. The count is the number of tests before the faulty link is isolated.

<figure>
<svg viewBox="0 0 480 105" width="480">
<line class="ln" x1="40" y1="30" x2="120" y2="30"/>
<line class="ln" x1="120" y1="30" x2="200" y2="30"/>
<line class="ln" x1="200" y1="30" x2="280" y2="30"/>
<line class="acc" x1="280" y1="30" x2="360" y2="30"/>
<line class="ln" x1="360" y1="30" x2="440" y2="30"/>
<rect class="box" x="25" y="20" width="30" height="20" rx="1"/><path class="ln" d="M32,44 L48,44"/><rect class="fill" x="29" y="24" width="22" height="11"/>
<text class="lbl" x="40" y="54" text-anchor="middle">PC</text>
<rect class="box" x="98" y="19" width="44" height="22" rx="2"/><path class="ln" d="M107,27 L133,27 M129,24 L133,27 L129,30 M133,34 L107,34 M111,31 L107,34 L111,37"/>
<text class="lbl" x="120" y="51" text-anchor="middle">SW1</text>
<circle class="box" cx="200" cy="30" r="13"/><path class="ln" d="M193,30 L207,30 M200,23 L200,37 M195,25 L205,35 M195,35 L205,25"/>
<text class="lbl" x="200" y="53" text-anchor="middle">R1</text>
<circle class="box" cx="280" cy="30" r="13"/><path class="ln" d="M273,30 L287,30 M280,23 L280,37 M275,25 L285,35 M275,35 L285,25"/>
<text class="lbl" x="280" y="53" text-anchor="middle">R2</text>
<circle class="box" cx="360" cy="30" r="13"/><path class="ln" d="M353,30 L367,30 M360,23 L360,37 M355,25 L365,35 M355,35 L365,25"/><circle class="acc" cx="360" cy="30" r="16"/>
<text class="lbl" x="360" y="53" text-anchor="middle">R3</text>
<rect class="box" x="426" y="15" width="28" height="30" rx="1"/><path class="ln" d="M426,25 L454,25 M426,35 L454,35"/><circle class="accf" cx="448" cy="20" r="1.2" style="fill:#1A1D23"/>
<text class="lbl" x="440" y="55" text-anchor="middle">Server</text>
<text class="sm" x="80" y="60" text-anchor="middle">1</text>
<text class="sm" x="160" y="60" text-anchor="middle">2</text>
<text class="sm" x="240" y="60" text-anchor="middle">3</text>
<text class="sm" x="320" y="60" text-anchor="middle">4</text>
<text class="sm" x="400" y="60" text-anchor="middle">5</text>
<line class="ln" x1="40" y1="63" x2="280" y2="63"/><text class="sm" x="288" y="66">1. from PC ping R2: reply, so links 1 to 3 are healthy</text><line class="acc" x1="40" y1="81" x2="360" y2="81"/><text class="sm" x="368" y="84">2. from PC ping R3: timeout, so the fault is in link 4</text></svg>
<figcaption><b>Figure 11.5</b> Binary search on the path. Two pings from the PC isolate link 4; one `show interface` on R2 then confirms the cause.</figcaption>
</figure>

| Strategy | Sequence | Tests |
|----------------|----------------------------------------------------------------------|--------|
| Bottom-up | PC port, SW1 port, R1 interface, link R1 to R2, link R2 to R3 (down) | 5 |
| Top-down | Browser timeout; `curl` by IP shows it is not DNS; `traceroute` stops after R2; `show interface` on R2 | 4 |
| Divide and conquer | `ping R2` works; `ping R3` fails; `show interface` on R2 confirms | 2 plus 1 |
| Follow the packet | `traceroute` shows last hop R2; inspect R2's route and egress interface | 2 |

[Result: with n segments, the binary search needs about log2 n tests (here two for five links), whereas the sequential strategies need up to n.]{.result}
:::

::: trap
*Claim:* "I always start at Layer 1." *Why it is wrong:* the physical layer is cheap to check only on the local device; on a remote path one `ping` at the middle already tests Layers 1 to 3 together and halves the search. *Correct statement:* use bottom-up after a physical change, and divide and conquer otherwise.
:::

::: check
1. A single laptop fails while its neighbour on the same switch works. Which strategy is natural? [^c11-4a]
2. Why is a swap done after the counters are saved? [^c11-4b]
:::

[^c11-4a]: Compare with working: diff the laptop's address, VLAN, port configuration and DHCP lease against its neighbour's.
[^c11-4b]: Replacing the part clears the counters and the fault, so the evidence for the root cause would be lost.

:::
