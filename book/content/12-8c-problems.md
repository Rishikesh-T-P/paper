::: {.p12}
::: problems
::: q
### Q12.41 Tell me about yourself.
[ALL · HR · ■□□ · S]{.meta}

[30-second answer, model (Ananya, fictional): "I am Ananya Rao, a final-year electronics and communication student at a Pune engineering college. Currently I am focused on networking: I built LabWatch, a Python tool that polls twelve lab switches every 30 seconds and raises an alert when a link stays above 80% for three samples. I got here through my CCNA preparation and a summer internship where I scripted configuration backups for 40 devices. I am drawn to Cisco's campus switching and Meraki products because they combine the routing and automation I enjoy. That is why I applied for this role."]{.short}

**Make it yours.** Present: project plus a number; Past: one or two proofs; Future: one named product and a link. 60 to 90 seconds. **Probes.** "Tell me more about LabWatch" (have the architecture ready, Q12.51). **Mistake.** Reading the résumé aloud, or starting with school marks.
:::

::: q
### Q12.42 Why networking? Why this company?
[ALL · HR · ■□□ · S]{.meta}

[30-second answer, model: "In my second year a campus outage of two hours turned out to be a duplex mismatch on one cable; finding it from interface counters made networks feel like detective work. The field is also where every service eventually depends on the same few protocols. I chose [company] because [one product or team] solves [problem] at a scale I want to work on, and my LabWatch and OSPF lab work are close to [that team's] daily tasks."]{.short}

**Make it yours.** A real moment, then the company's specific product, then your matching proof. **Probes.** "What do you know about our products?", "Which of our competitors do you prefer?" Read the company's engineering blog the week before. **Mistake.** "Because it is a reputed company".
:::

::: q
### Q12.43 (Customer Obsession) A time you went beyond what was asked for a user.
[AMAZON · CISCO · BEHAVIOURAL · ■■□ · T]{.meta}

[30-second answer, model: **S/T.** Hostel students complained of slow Wi-Fi each evening; the IT office had closed the tickets as "bandwidth is fine". I wanted the actual cause. **A.** I surveyed 40 students, then logged client counts per access point every minute for five evenings with a small script. Two of the nine access points carried 60% of the clients. I showed the chart to the IT office and proposed lowering the power of those two and moving one. **R.** Median ping to the gateway at 9 p.m. fell from 180 ms to 60 ms, and tickets for the month fell from 22 to 7.]{.short}

**Make it yours.** Who was the user, what did they say, what did you measure, what changed. **Probes.** "What if IT had refused?" (take the data to the warden). "How did you know the survey was representative?" **Principles.** Also fits Dive Deep.
:::

::: q
### Q12.44 (Ownership) A time you took responsibility for something outside your role.
[AMAZON · MICROSOFT · BEHAVIOURAL · ■■□ · T]{.meta}

[30-second answer, model: **S.** Two days before a networking practical, the simulator images failed to load on 30 lab PCs; the technician was on leave and the repair was queued for later in the week. **T.** It was not my job, but my batch would lose the exam slot. **A.** I found that the cache folder had been corrupted, wrote a script to restore the images from the shared drive, tested it on three machines, and wrote a one-page guide so the instructor could repeat it. **R.** All 30 PCs were working in two hours and the practical went ahead as scheduled.]{.short}

**Make it yours.** The cost of doing nothing, what you chose to own, how you made it repeatable. **Probes.** "Did you ask permission?" (say you informed the instructor first). **Mistake.** Taking over someone's work without telling them.
:::

::: q
### Q12.45 (Dive Deep) A time you found the root cause of a difficult problem.
[AMAZON · CISCO · JUNIPER · BEHAVIOURAL · ■■□ · T]{.meta}

[30-second answer, model: **S.** Transfers between two lab PCs ran at about 8 Mb/s on a 100 Mb/s link, on and off. **T.** I was asked to find out why before a demonstration. **A.** I first ruled out the cable and the PCs with `iperf` on a different port. Then I read the interface counters on the switch: late collisions and CRC errors were rising on the one port. One end was set to auto-negotiate and the other hard-coded to 100 Mb/s full duplex, so the auto side fell back to half duplex: a duplex mismatch. **R.** Setting both ends to auto restored 94 Mb/s, and I added the check to the lab handbook.]{.short}

**Make it yours.** Symptom, hypotheses ruled out in order, the one datum that located the cause. **Probes.** "What would you have done if the counters were clean?" (packet capture on both sides). Troubleshooting method: [Pillar 11](#ch11){.ref}.
:::

::: q
### Q12.46 (Have Backbone; Disagree and Commit) A time you disagreed with a teammate or professor.
[AMAZON · GOOGLE · BEHAVIOURAL · ■■□ · T]{.meta}

[30-second answer, model: **S.** For LabWatch, our supervisor asked us to use SNMPv2c; I wanted SNMPv3 because v2c sends the community string in clear text. **A.** I wrote a short note: three of our five switch models did not support v3 in the lab images, and v2c on an isolated management VLAN limited the risk. I raised my concern once, with the evidence, and the supervisor decided on v2c. I committed fully: I put the poller on the management VLAN, restricted access with an ACL, and documented the risk. **R.** We delivered on time, and I later enabled v3 on the two models that supported it.]{.short}

**Make it yours.** Show respect, data, a clear decision, and full commitment afterwards. **Probes.** "Were you right?" (partly; the constraint was real). **Mistake.** A story in which the other person was simply wrong.
:::

::: q
### Q12.47 (Bias for Action) A time you decided with incomplete information.
[AMAZON · MICROSOFT · BEHAVIOURAL · ■■□ · T]{.meta}

[30-second answer, model: **S.** Two hours before a hackathon demonstration, the server on port 8080 was unreachable from the judges' network; the college firewall rules were unknown and IT was not responding. **T.** Decide whether to wait or change the plan. **A.** Waiting was not an option and the change was reversible, so I wrote a ten-line script that tried ports 80, 443 and 8443 from the venue network. Only 443 was open. We moved the demo there and kept the old setting as a fallback. **R.** The demonstration ran without a failure and we placed second.]{.short}

**Make it yours.** State the deadline, what you did not know, why the decision was reversible, and how you cheaply reduced uncertainty. **Probes.** "What if 443 had been closed?" (the phone hotspot, prepared in advance).
:::

::: q
### Q12.48 (Deliver Results) A time you met a tough deadline.
[AMAZON · CISCO · BEHAVIOURAL · ■■□ · T]{.meta}

[30-second answer, model: **S/T.** A reliable file transfer over UDP, with a sliding window, was due in ten days and I had written no code. **A.** I cut the scope into steps with dates: stop-and-wait by day 3, sliding window by day 7, tests and report by day 10. I used `tc netem` to emulate 10% loss from the first version, so bugs showed early. When the window logic failed on day 6, I dropped the planned congestion control rather than the tests. **R.** A 1 MB file arrived with a matching hash under 10% loss, submitted on day 10.]{.short}

**Make it yours.** The fixed date, the plan, what you cut and why. **Probes.** "What would you have cut next?" **Mistake.** Heroic overnight work as the only action.
:::

::: q
### Q12.49 (Learn and Be Curious) Something you learnt recently on your own.
[AMAZON · GOOGLE · BEHAVIOURAL · ■□□ · T]{.meta}

[30-second answer, model: "No course covered BGP, so I taught myself. I read the core sections of RFC 4271, then built a three-AS lab in GNS3 over two weekends, and deliberately broke it: a wrong next hop, a missing network statement, a looping AS path. Each failure taught me one rule, such as why an iBGP route needs the next hop to be reachable. I wrote two pages of notes and explained them to twelve juniors in a one-hour session, which showed me three gaps that I then closed."]{.short}

**Make it yours.** What, how (a project, not just videos), what broke, how you shared it. **Probes.** "What will you learn next, and why?" Have an answer that matches the role.
:::

::: q
### Q12.50 Tell me about a failure. What did you learn?
[AMAZON · GOOGLE · CISCO · BEHAVIOURAL · ■■■ · T]{.meta}

[30-second answer, model: **S/T.** I was automating VLAN changes on six lab switches with a Netmiko script. **A (failure).** I ran it without a dry run, and a template error replaced the VLAN configuration; the lab was down for 40 minutes. I told the instructor at once, and restored the switches from backups that I happened to have saved. Then I added three things to the script: a dry-run mode that prints the diff, an automatic backup before any change, and a rollback command. **R.** No incident in the next three months, and the instructor adopted the script. **L.** Change tools must be safe by default, not by my care.]{.short}

**Make it yours.** A real failure with your own responsibility, quickly owned, and a system-level fix. **Probes.** "Whose fault was it?" (mine; avoid blaming). **Mistake.** A disguised success ("I worked too hard").
:::

::: q
### Q12.51 Walk me through your best project. Draw the architecture.
[JUNIPER · ARISTA · CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer, model: "LabWatch monitors twelve lab switches. A Python poller sends SNMP requests to each switch every 30 seconds, stores interface counters in SQLite, and a small web page plots utilisation; an alert rule e-mails me when a link exceeds 80% for three samples."]{.short}

```
12 switches --SNMP--> poller (asyncio) --> SQLite --> web dashboard
                              \--> alert rule --> e-mail
```

**Approach.** Draw five boxes before speaking; say the problem, your share (all of the poller, half the dashboard), then one number: 38 samples per second (12 switches × 48 ports × 2 counters / 30 s = 38.4). **Probes.** "Why SNMP and not streaming telemetry?" (supported by all the lab devices); "How is the data stored?" Method in [§12.13](#s12-13){.ref}.
:::

::: q
### Q12.52 What was the hardest bug in your project and how did you find it?
[JUNIPER · ARISTA · BROADCOM · TECH-1 · ■■□ · T]{.meta}

[30-second answer, model: the utilisation graph showed impossible negative spikes. The cause was the 32-bit counter `ifInOctets`, which wraps after 2<sup>32</sup> bytes: at 1 Gb/s that is 34 seconds, so at a 30-second poll the counter often wraps between two readings and the raw difference is negative. I found it by printing consecutive raw values near a spike. I fixed it with the 64-bit `ifHCInOctets` and, for old devices, by computing deltas modulo 2<sup>32</sup>.]{.short}

**Check.** 2<sup>32</sup> × 8 / 10<sup>9</sup> = 34.4 s at 1 Gb/s; 343.6 s at 100 Mb/s. **Probes.** "What if the counter wraps twice between polls?" (poll faster than the wrap time; at 100 Gb/s even 64-bit counters last years). **Method.** Symptom, hypothesis, raw data, cause, fix, test.
:::

::: q
### Q12.53 If your project had to serve 1,000 times the load, what breaks first?
[AMAZON · GOOGLE · CISCO · TECH-2 · ■■■ · T]{.meta}

[30-second answer: today LabWatch handles 38.4 samples per second; at 1,000 times (12,000 switches) that is 38,400 per second. The poller breaks first, because it waits for each switch in turn, and the single-writer SQLite database second. The fixes are a pool of asynchronous pollers sharded by device, batched inserts, and a time-series database with down-sampling.]{.short}

**Order of reasoning.** Estimate (12,000 × 48 × 2 / 30 = 38,400 per second); find the bottleneck by tracing one cycle; fix it; name the next one (the network: SNMP over UDP loses polls under load, so move to streaming telemetry). **Mistake.** "Just add servers" with no bottleneck named.
:::

::: q
### Q12.54 What would you do differently if you started the project again?
[AMAZON · MICROSOFT · BEHAVIOURAL · ■■■ · T]{.meta}

[30-second answer: three changes, each with a reason: use 64-bit counters from the first day (it cost me two days to find the wrap); write tests against a fake SNMP agent before the poller (I tested by hand on real switches); and consider gNMI streaming where devices support it, because polling cannot see changes shorter than the interval.]{.short}

**Make it yours.** Name real flaws, not trivial ones ("better UI"). Link each to a lesson and to the next version. **Probes.** "Which would you do first?" (the tests, since they make the other changes safe). **Mistake.** "Nothing; it went well".
:::
:::
:::
