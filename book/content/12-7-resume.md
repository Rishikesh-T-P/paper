::: {.p12}

## [12.13]{.sec}Résumé and project deep-dives for networking roles [Must · ■□□]{.tag} {#s12-13}

The résumé does two jobs. It passes a first screen, by a person who reads for about thirty seconds or by software that matches keywords, and it becomes the agenda of the interview, because every line on it may be questioned. Juniper, Arista and Broadcom panels are reported to spend most of a technical round on one or two résumé projects. A résumé is therefore a list of promises, and the interview checks whether each can be kept.

::: bigidea
Put on the page only what you can defend for five minutes at a whiteboard, because the interviewer will choose the line you are least ready for.
:::

### Layout of the one-page résumé

A fresher's résumé is one page, in a single column, exported as PDF. Multi-column layouts, tables, icons and skill bars are often misread by applicant-tracking software, and a photograph or marital status is not wanted. Order the sections by strength: for most students, projects come before certificates.

<figure>
<svg viewBox="0 0 480 252" width="480">
<rect class="box" x="10" y="6" width="170" height="240"/>
<g class="lbl"><text x="18" y="22">Ananya Rao</text></g>
<text class="sm" x="18" y="32">email · phone · LinkedIn · GitHub (live links)</text>
<line class="lg" x1="18" y1="37" x2="172" y2="37"/>
<rect class="fill" x="18" y="42" width="154" height="22"/><text class="sm" x="22" y="56">EDUCATION: degree, college, CGPA, year</text>
<rect class="fill" x="18" y="68" width="154" height="30"/><text class="sm" x="22" y="80">SKILLS: Languages · Networking</text><text class="sm" x="22" y="91">Tools · Automation · Cloud</text>
<rect class="hl" x="18" y="102" width="154" height="68"/><rect class="box" x="18" y="102" width="154" height="68"/><text class="sm" x="22" y="114">PROJECTS (3): name, stack, link</text><text class="sm" x="22" y="128">• Accomplished X, measured by Y,</text><text class="sm" x="22" y="138">   by doing Z</text><text class="sm" x="22" y="152">• one or two bullets per project,</text><text class="sm" x="22" y="162">   each with a number</text>
<rect class="fill" x="18" y="174" width="154" height="22"/><text class="sm" x="22" y="188">EXPERIENCE or INTERNSHIP</text>
<rect class="fill" x="18" y="200" width="154" height="16"/><text class="sm" x="22" y="212">CERTIFICATIONS (CCNA, AWS CCP)</text>
<rect class="fill" x="18" y="220" width="154" height="18"/><text class="sm" x="22" y="232">ACHIEVEMENTS: ratings, hackathons</text>
<g class="lbl">
<line class="lg" x1="180" y1="30" x2="215" y2="30"/><text x="220" y="33">Links must open; no photograph, no address</text>
<line class="lg" x1="180" y1="53" x2="215" y2="53"/><text x="220" y="56">CGPA only if 7.5 or above</text>
<line class="lg" x1="180" y1="83" x2="215" y2="83"/><text x="220" y="86">Group skills; list only what you can be tested on</text>
<line class="acc" x1="180" y1="136" x2="215" y2="136"/><text x="220" y="139">The core of the page: about 40% of the space</text>
<line class="lg" x1="180" y1="185" x2="215" y2="185"/><text x="220" y="188">Internship: what you owned and its effect</text>
<line class="lg" x1="180" y1="208" x2="215" y2="208"/><text x="220" y="211">Optional; pair each with one project that uses it</text>
</g>
<text class="sm" x="220" y="236">One page · single column · standard headings · PDF · 10 to 11 pt</text>
</svg>
<figcaption><b>Figure 12.17</b> The one-page layout of a fresher's networking résumé, with the projects block emphasised.</figcaption>
</figure>

Skills are grouped so that a reader can find a keyword at once: *Languages* (C, Python), *Networking* (TCP/IP, VLAN, STP, OSPF, BGP, ACLs, NAT), *Tools* (Wireshark, tcpdump, GNS3 or EVE-NG, Linux), *Automation* (Netmiko, NAPALM, Ansible, REST and NETCONF) and *Cloud* (AWS VPC). Align the keywords with the job description for network development, network consulting or software-in-networking roles, but only those you could explain. Red flags include "OSI model" as a skill, percentage bars for skills, vague buzzwords and links that return an error.

### The bullet formula

Each bullet follows Google's *XYZ* form: "Accomplished **X**, as measured by **Y**, by doing **Z**." It forces a result and a method into one line and starts with a verb in the past tense.

| Weak | Strong |
|---|---|
| Worked on a network automation project using Python | Cut lab configuration time from 2 hours to 5 minutes (about 96% less) by writing a Python and Netmiko script that pushes templated configurations to 12 routers |
| Made a file transfer tool | Reduced packet loss in a UDP file-transfer tool in C from 12% to 0.5% by adding selective-repeat retransmission with a 16-packet window |
| Learnt OSPF and BGP | Built a three-area OSPF and two-AS eBGP lab in GNS3 with route maps that prefer the primary link, and verified failover in under 5 seconds with traceroute |
| Member of coding club | Solved 450 problems on an online judge and reached a rating of 1,650 (Codeforces) |

The percentage in the second row of the table is checked: 1 − 5/120 = 0.958. Never invent a number; use measurements you actually took, and state the conditions if asked ("12 routers in a virtual lab").

### Choosing and presenting projects

Network interviewers prefer a project that is measurable, network-relevant and your own code. Strong choices are a multi-area OSPF and eBGP lab; a packet sniffer in C on raw sockets; a small TCP over UDP with a sliding window; a DHCP or DNS server in Python; an SDN controller application; a monitoring dashboard fed by SNMP or gNMI; a VXLAN-EVPN lab in containerlab. The labs and mini-projects of Pillars 8 to 11 are designed to be listed here. Give each repository a README with a one-line purpose, an architecture diagram, how to run it, results, and tests; a licence file completes it.

### How to defend a project

An interviewer asks, in some order, ten things. Prepare a written answer to each, in a two-minute version and a ten-minute version.

| # | Question | What a good answer contains |
|---|---|---|
| 1 | What problem, and why does it matter? | One sentence of need, one of who suffers |
| 2 | Draw the architecture | Five boxes and the data path, drawn without notes |
| 3 | What did you build, and what did others? | Your share, stated plainly |
| 4 | What was the hardest bug and how did you find it? | Symptom, method, tool, cause (a Dive Deep story) |
| 5 | What alternatives did you reject, and why? | Two options with a reason each |
| 6 | How did you test it? | Unit tests, fault injection, a measured baseline |
| 7 | What were the results? | Numbers with conditions |
| 8 | What breaks at ten times, and at a thousand times, the load? | The first bottleneck and its fix |
| 9 | What about security? | Credentials, input validation, least privilege |
| 10 | What would you change? | One honest flaw and the next step |

::: example
**Prepare the answer to "why did you choose Netmiko, and not NETCONF, for the config pusher?"**

1. State the facts of the situation: the lab devices were three vendors, two of which had no NETCONF support in the images available.
2. Name the cost of the choice: screen-scraping is brittle, since output formats change between versions.
3. Name the mitigation and the next step: parsing with templates, a test per command, and a plan to move supported devices to NETCONF.

[Result: the answer shows a constraint, a trade-off and an improvement, which is what "why" questions look for.]{.result}
:::

::: trap
*Claim:* "Listing many technologies makes the résumé stronger." *Why it is wrong:* each one is a licence for a question, and three missed questions end a project discussion. *Correct statement:* list fewer tools, and be able to explain how each works, why you chose it and what its limits are. Likewise, claiming the team's work as your own is detected by a single probe: "which part did you write?"
:::

::: lens
[JUNIPER · ARISTA · BROADCOM · CISCO · AMAZON]{.co}

The deep-dive is usually the longest block of a technical round. The panel is estimating your real contribution, your understanding of the layers below your code, and your honesty about limits. A strong candidate draws the architecture unprompted, brings a number, and answers "what would you change?" with a specific flaw. The model answers are in [Q12.51 to Q12.54](#ps12){.ref}.
:::

::: check
1. Rewrite "Improved performance of the DNS server" in the XYZ form, with placeholder numbers. [^c12i-1]
2. A script cut a task from 90 minutes to 6. What is the percentage reduction? [^c12i-2]
:::

[^c12i-1]: For example: "Raised throughput of a Python DNS server from 800 to 3,200 queries per second by caching answers for their TTL and using asynchronous sockets."
[^c12i-2]: 1 − 6/90 = 0.933, about 93%.

:::
