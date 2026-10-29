::: {.p12}

## [12.14]{.sec}Where it is asked, drills and the portfolio project [Optional · ■□□]{.tag} {#s12-14}

Knowledge from this pillar decays faster than the networking in earlier pillars, because it is practised in speed and speech. This final section therefore says which company asks what, how to drill in thirty-minute blocks, and how to gather the whole pillar into one portfolio.

### Where each topic is asked

The matrix records reported emphasis, not guarantees: ● often, ◐ sometimes, ○ rarely. Verify against your drive's notice.

| Topic | Cisco | Qualcomm | Google | Microsoft | Amazon NDE | Juniper | Arista | Nokia | Broadcom |
|---|---|---|---|---|---|---|---|---|---|
| Aptitude in the OA | ● | ● | ○ | ○ | ◐ | ● | ◐ | ● | ● |
| CS MCQs (C, OS, DBMS, networks) | ● | ● | ○ | ◐ | ◐ | ● | ◐ | ● | ● |
| OOP viva | ● | ● | ◐ | ● | ◐ | ● | ● | ● | ● |
| DBMS and SQL | ● | ◐ | ◐ | ● | ◐ | ◐ | ◐ | ● | ◐ |
| Computer organisation, bits | ◐ | ● | ◐ | ◐ | ○ | ◐ | ● | ◐ | ● |
| Light system design | ● | ○ | ● | ● | ● | ◐ | ◐ | ◐ | ○ |
| Behavioural (STAR) | ● | ◐ | ● | ● | ● | ◐ | ◐ | ◐ | ◐ |
| Résumé and project deep-dive | ● | ● | ● | ● | ● | ● | ● | ● | ● |

### Drills

| ID | Drill | Time |
|---|---|---|
| D12A.1 to D12A.12 | A 20-question timed set for each topic group of [§12.2](#s12-2){.ref} to [§12.6](#s12-6){.ref}; use the forty questions after the Problem Set first | 25 min each |
| D12A.M1 | Full mock paper: 50 questions, 60 minutes, pacing as in [Figure 12.1](#s12-1){.ref} | 60 min |
| D12E.1 | Three design mocks from [§12.11](#s12-11){.ref}, the six steps timed, a friend as interviewer | 3 × 35 min |
| D12F.1 | Story-mining worksheet: list ten incidents, tag each with principles | 60 min |
| D12F.2 | Record answers to ten behavioural prompts; score structure, "I", number, learning, time | 60 min |
| D12G.1 | Rewrite your résumé against the twenty-point checklist in the Revision Spread | 60 min |
| D12G.2 | Fill the deep-dive table of [§12.13](#s12-13){.ref} for your main project; time the two-minute version | 60 min |

The daily routine for aptitude is thirty minutes: ten minutes revising one formula card, fifteen minutes on a timed set, five minutes entering every miss in the error log. Keep the log honestly; its trend tells you which of the three error types to attack.

| Date | Topic | Question | Error type | Fix |
|---|---|---|---|---|
| 12 Mar | Time and work | A, B, C: C alone | Careless (read 5 days as 6) | Underline the numbers |
| 13 Mar | P and C | Vowels together | Concept (forgot inner order) | Glue, arrange, multiply |

The three types are *concept* (you did not know the rule), *careless* (you knew it) and *speed* (right but too slow). Concept errors need a card; careless errors need a habit such as writing the base before computing; speed errors need timed sets.

::: lab
`LAB 12.1 · 30 MIN` Build the inventory of [§12.9](#s12-9){.ref} and watch an index change a query plan. Save the statements of that section in `inventory.sql`, then run:

```python
import sqlite3
c = sqlite3.connect(":memory:")
c.executescript(open("inventory.sql").read())
q = "SELECT s.city, COUNT(d.name), COALESCE(SUM(d.ports), 0) FROM site s " \
    "LEFT JOIN device d ON d.site_id = s.site_id GROUP BY s.city ORDER BY 3 DESC"
print(c.execute(q).fetchall())
print(c.execute("EXPLAIN QUERY PLAN SELECT * FROM device WHERE vendor = 'Arista'").fetchall())
c.execute("CREATE INDEX ix_vendor ON device(vendor)")
print(c.execute("EXPLAIN QUERY PLAN SELECT * FROM device WHERE vendor = 'Arista'").fetchall())
```

The key output lines are `[('Main', 4, 104), ('Hostel', 2, 72), ('Lab', 1, 8), ('Annexe', 0, 0)]`, then `SCAN device`, then `SEARCH device USING INDEX ix_vendor (vendor=?)`.

**What you should notice:** the empty site Annexe survives because of the left join, and the plan changes from a scan of every row to a search through the index. On seven rows the difference is invisible in time; on seven million it decides the query.
:::

Then answer ten graded queries on the same data; the expected results are in the table, and writing each before running it is the point of the exercise.

| # | Task | Expected result |
|---|---|---|
| 1 | Devices with at least 24 ports | `sw1`, `sw2`, `sw3`, `sw4` |
| 2 | Devices per vendor, largest first | Arista 3, Cisco 2, Juniper 1, Palo Alto 1 |
| 3 | Cities whose total ports exceed 50 | Hostel 72, Main 104 |
| 4 | Devices from Cisco or Juniper | `r1`, `r2`, `sw1` |
| 5 | Sites with no device, using `NOT IN` | Annexe |
| 6 | Vendors present at more than one site | Arista |
| 7 | Share of all ports held by `sw1` | 26.09% (48 of 184) |
| 8 | The largest device in Hostel | `sw4` |
| 9 | Pairs of devices at the same site | 7 (six at Main, one at Hostel) |
| 10 | Rank by ports with `RANK()` | `sw1`, `sw2`, `sw4` rank 1; `sw3` 4; `fw1` 5; `r1`, `r2` 6 |

### Mini-project: the Placement Readiness Portfolio

The pillar ends with a deliverable that you can send to a recruiter. Gather: (i) the final one-page résumé; (ii) a GitHub profile with two or three polished repositories from the projects of Pillars 8 to 11; (iii) a story bank of eight STAR stories mapped to the principles, in the matrix of [Figure 12.16](#s12-12){.ref}; (iv) one design write-up, the campus network for your own college with real building names and a plausible IP plan; (v) a two-minute and a ten-minute recording of your main project; (vi) your error-log trend, showing the rate of each error type falling over four weeks.

::: check
1. In the matrix, which two themes cover most of the technical rounds? [^c12j-1]
2. Which error type does a timed set cure? [^c12j-2]
:::

[^c12j-1]: OOP viva and résumé or project deep-dive, which are ● for every company listed.
[^c12j-2]: Speed errors; concept errors need a formula card and careless errors need a checking habit.

:::
