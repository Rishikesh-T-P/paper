::: {.p12}

## [12.9]{.sec}Databases: keys, SQL, normalisation, transactions and indexes [Must · ■■□]{.tag} {#s12-9}

A database management system, or DBMS, stores data so that many programs can query and change it safely. Network teams use one for inventories, IP address management and monitoring, and campus tests ask about it at multiple-choice depth: keys, normal forms, a join or two, ACID and indexes. We follow one running inventory, drawn from Campus Net, through the whole section.

### Relations, keys and the ER model

A *relation* is a table; a *tuple* is a row; an *attribute* is a column. Keys identify rows, and the vocabulary is tested directly.

| Key | Definition | Inventory example |
|---|---|---|
| Super key | Any set of attributes that is unique per row | (name), (name, vendor) |
| Candidate key | A minimal super key | `name` |
| Primary key | The candidate chosen to identify rows; unique and not null | `device.name` |
| Unique key | Unique, but may be null (one null in some systems) | `device.serial` |
| Foreign key | Attribute referring to a primary key elsewhere; enforces referential integrity | `device.site_id` refers to `site.site_id` |
| Composite key | A key of several attributes | (`device`, `interface`) |

An *entity-relationship diagram* shows entities as boxes and relationships as lines; the crow's foot at one end means "many". One site has many devices and one device has many interfaces, so the inventory is a chain of one-to-many links.

<figure>
<svg viewBox="0 0 480 90" width="480">
<rect class="box" x="10" y="20" width="110" height="50"/><line class="ln" x1="10" y1="36" x2="120" y2="36"/>
<text class="lbl" x="65" y="32" text-anchor="middle">Site</text><text class="sm" x="16" y="50">site_id (PK)</text><text class="sm" x="16" y="62">city</text>
<rect class="box" x="185" y="20" width="110" height="50"/><line class="ln" x1="185" y1="36" x2="295" y2="36"/>
<text class="lbl" x="240" y="32" text-anchor="middle">Device</text><text class="sm" x="191" y="50">name (PK), site_id (FK)</text><text class="sm" x="191" y="62">vendor, ports</text>
<rect class="box" x="360" y="20" width="110" height="50"/><line class="ln" x1="360" y1="36" x2="470" y2="36"/>
<text class="lbl" x="415" y="32" text-anchor="middle">Interface</text><text class="sm" x="366" y="50">name, device (PK)</text><text class="sm" x="366" y="62">ip, mtu</text>
<line class="ln" x1="120" y1="45" x2="185" y2="45"/>
<line class="ln" x1="185" y1="45" x2="171" y2="38"/><line class="ln" x1="185" y1="45" x2="171" y2="52"/><line class="ln" x1="185" y1="45" x2="171" y2="45"/>
<text class="sm" x="128" y="40">1</text>
<line class="ln" x1="295" y1="45" x2="360" y2="45"/>
<line class="ln" x1="360" y1="45" x2="346" y2="38"/><line class="ln" x1="360" y1="45" x2="346" y2="52"/><line class="ln" x1="360" y1="45" x2="346" y2="45"/>
<text class="sm" x="303" y="40">1</text>
</svg>
<figcaption><b>Figure 12.6</b> Entity-relationship diagram of the Campus Net inventory: three one-to-many links, with the crow's foot on the "many" side.</figcaption>
</figure>

### SQL in one page

SQL statements are written in one order but executed in another, and most wrong answers come from forgetting it: `FROM` and joins, then `WHERE`, `GROUP BY`, `HAVING`, `SELECT`, `ORDER BY`, and last `LIMIT`. Hence a column alias defined in `SELECT` cannot be used in `WHERE`, and `WHERE` filters rows before grouping while `HAVING` filters groups after it.

Our data: `site(1 Main, 2 Hostel, 3 Lab, 4 Annexe)` and `device(name, site_id, vendor, ports)` with `r1`, `r2` (Main, Cisco, 4 ports each), `sw1` (Main, Juniper, 48), `sw2` (Main, Arista, 48), `sw3` (Hostel, Arista, 24), `sw4` (Hostel, Arista, 48) and `fw1` (Lab, Palo Alto, 8).

| Join | Rows returned | Typical use |
|---|---|---|
| `INNER JOIN` | Only matching pairs | Devices with their city |
| `LEFT JOIN` | All left rows; right columns null if no match | Sites including empty ones |
| `RIGHT JOIN` | Mirror image of left | Rarely needed |
| `FULL JOIN` | All rows from both sides | Reconciling two inventories |
| `CROSS JOIN` | Every pair (m × n rows) | Generating combinations |
| Self join | A table joined to itself with aliases | Employees with their managers |

::: example
**Four queries on the inventory, with their exact output.**

1. Arista devices and their city: `SELECT d.name, s.city FROM device d JOIN site s ON d.site_id = s.site_id WHERE d.vendor = 'Arista' ORDER BY d.name;` gives (`sw2`, Main), (`sw3`, Hostel), (`sw4`, Hostel).
2. Devices per site, including empty sites: `SELECT s.city, COUNT(d.name) FROM site s LEFT JOIN device d ON d.site_id = s.site_id GROUP BY s.city;` gives Annexe 0, Hostel 2, Lab 1, Main 4. Using `COUNT(*)` here would wrongly give Annexe 1, since the null-padded row still counts.
3. Sites with more than two devices: `... GROUP BY s.city HAVING COUNT(*) > 2;` gives Main (4).
4. Devices with more ports than the average of their own site (a correlated subquery): `SELECT name FROM device d WHERE ports > (SELECT AVG(ports) FROM device WHERE site_id = d.site_id);` gives `sw1`, `sw2`, `sw4`. The site averages are 26 for Main and 36 for Hostel.

[Result: `COUNT(column)` skips nulls and `COUNT(*)` does not; that distinction decides query 2.]{.result}
:::

The window function `ROW_NUMBER() OVER (PARTITION BY site_id ORDER BY ports DESC)` numbers devices within each site without collapsing rows, which is the clean way to answer "top *n* per group". `EXISTS` stops at the first match and handles nulls safely, whereas `NOT IN` returns nothing if the subquery yields a single null. The classic "second-highest salary" and join questions are solved in [Q12.21 and Q12.22](#ps12){.ref}.

### Normalisation

Normalisation splits tables so that each fact is stored once, which removes three anomalies: *insertion* (cannot add a site without a device), *update* (the same city changed in many rows) and *deletion* (removing the last device loses the site). It rests on *functional dependencies*: *X* → *Y* means that each value of *X* determines one value of *Y*.

| Normal form | Requirement | Violation fixed by |
|---|---|---|
| 1NF | Every cell is atomic; no repeating groups | One row per IP address, not "10.0.0.1, 10.0.0.2" |
| 2NF | 1NF, and no non-key attribute depends on *part* of a composite key | Moving partial dependencies to a new table |
| 3NF | 2NF, and no non-key attribute depends on another non-key attribute (no transitive dependency) | Moving the transitive chain out |
| BCNF | For every dependency *X* → *Y*, *X* is a super key | Splitting on the offending determinant |

::: example
**Normalise `Log(device, site, site_city, interface, ip, vendor, vendor_phone)`.** The dependencies are: device → site, vendor; site → site_city; vendor → vendor_phone; (device, interface) → ip. The key is (device, interface).

1. 1NF: assume every cell holds a single value (otherwise split the multiple IPs into rows).
2. 2NF: `site` and `vendor` depend on `device` alone, which is part of the key. Split into `Device(device, site, site_city, vendor, vendor_phone)` and `Interface(device, interface, ip)`.
3. 3NF: in `Device`, site → site_city and vendor → vendor_phone are transitive. Split into `Device(device, site, vendor)`, `Site(site, site_city)` and `Vendor(vendor, vendor_phone)`.
4. BCNF: in all four tables every determinant is a key, so the design is in BCNF.

[Result: four tables, `Interface`, `Device`, `Site`, `Vendor`; each city and phone number is stored once.]{.result}
:::

::: trap
*Claim:* "3NF and BCNF are the same." *Why it is wrong:* take `Teach(student, course, teacher)` where each teacher teaches one course, so teacher → course. The key is (student, course) or (student, teacher). The table is in 3NF, because `course` is part of a key, yet teacher is not a super key. *Correct statement:* BCNF is stricter; the split into `(teacher, course)` and `(student, teacher)` achieves it, but this particular split loses the dependency (student, course) → teacher.
:::

Denormalisation reverses the process deliberately, to avoid joins in read-heavy systems such as monitoring dashboards, at the price of redundant copies.

### Transactions, ACID and isolation

A *transaction* is a group of statements that must succeed or fail as one. Transferring money by UPI is the standard illustration: debit and credit happen together or not at all.

| Property | Meaning | Mechanism |
|---|---|---|
| Atomicity | All or nothing | Undo log, rollback |
| Consistency | Constraints hold before and after | Keys, checks, triggers |
| Isolation | Concurrent transactions do not see each other's partial work | Locks, multi-version concurrency control (MVCC) |
| Durability | Committed data survives a crash | Write-ahead log flushed before commit |

Concurrency causes three named anomalies. A *dirty read* sees another transaction's uncommitted change. A *non-repeatable read* reads a row twice and gets two values because another transaction committed between. A *phantom* re-runs a range query and finds new rows. The isolation levels of the SQL standard each forbid more of them.

| Isolation level | Dirty read | Non-repeatable read | Phantom |
|---|---|---|---|
| Read uncommitted | possible | possible | possible |
| Read committed | prevented | possible | possible |
| Repeatable read | prevented | prevented | possible (standard) |
| Serializable | prevented | prevented | prevented |

Note that engines differ from the standard table: PostgreSQL's repeatable read is a snapshot that also blocks phantoms, and its default is read committed; MySQL InnoDB defaults to repeatable read. *Deadlock* arises when two transactions each hold a lock the other needs; the engine detects the cycle and aborts one, which the application must retry.

### Indexes and B+ trees

An *index* is a separate sorted structure that lets the engine find rows without scanning the table, like the index of a book. Most engines use a *B+ tree*: a balanced tree in which internal nodes hold only keys and routing pointers, all rows (or row pointers) sit in the leaves, and the leaves are linked in order. The height stays small because each node is a disk page holding hundreds of keys. With a fan-out of 100, one million rows need about three levels, hence three or four page reads for a lookup, against thousands for a scan. The linked leaves make range queries cheap: find the first key, then walk sideways.

<figure>
<svg viewBox="0 0 480 120" width="480">
<defs><marker id="a129" viewBox="0 0 6 6" refX="5" refY="3" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L6 3L0 6z" fill="#1A1D23"/></marker></defs>
<rect class="box" x="190" y="8" width="100" height="22"/><line class="ln" x1="240" y1="8" x2="240" y2="30"/>
<text class="lbl" x="215" y="23" text-anchor="middle">30</text><text class="lbl" x="265" y="23" text-anchor="middle">60</text>
<rect class="box" x="30" y="80" width="110" height="22"/><text class="lbl" x="85" y="95" text-anchor="middle">10 | 20</text>
<rect class="box" x="185" y="80" width="110" height="22"/><text class="lbl" x="240" y="95" text-anchor="middle">30 | 40 | 50</text>
<rect class="box" x="340" y="80" width="110" height="22"/><text class="lbl" x="395" y="95" text-anchor="middle">60 | 70 | 80</text>
<line class="ln" x1="205" y1="30" x2="95" y2="80" marker-end="url(#a129)"/>
<line class="ln" x1="240" y1="30" x2="240" y2="80" marker-end="url(#a129)"/>
<line class="ln" x1="275" y1="30" x2="385" y2="80" marker-end="url(#a129)"/>
<line class="acc" x1="140" y1="91" x2="183" y2="91" marker-end="url(#a129)"/>
<line class="acc" x1="295" y1="91" x2="338" y2="91" marker-end="url(#a129)"/>
<text class="sm" x="240" y="116" text-anchor="middle">leaves are linked in key order: a range scan reads one leaf after another</text>
</svg>
<figcaption><b>Figure 12.7</b> A small B+ tree. Keys below 30 go left, 30 to 59 to the middle, 60 and above to the right; the highlighted links are the leaf chain.</figcaption>
</figure>

A *clustered* index stores the table rows in key order (one per table, normally the primary key); a *non-clustered* index holds keys with pointers to rows. A *composite* index on (`site_id`, `vendor`) serves `WHERE site_id = 1` and `WHERE site_id = 1 AND vendor = 'Arista'`, but not `WHERE vendor = 'Arista'` alone: this is the *leftmost-prefix rule*. An index is ignored when the column is wrapped in a function (`WHERE UPPER(vendor) = ...`) or when the predicate matches most rows, and each index slows inserts and updates and costs storage.

### NoSQL and telemetry stores

Key-value, document, wide-column and graph stores relax the relational model to scale across machines. The CAP theorem says that during a network partition a distributed store must choose between consistency and availability. Interface counters are best kept in a *time-series database* such as Prometheus: 10,000 ports sampled every 10 seconds produce 1,000 samples per second, or 86.4 million samples a day, which suits append-only time-ordered storage rather than a relational table.

::: lens
[CISCO · MICROSOFT · NOKIA · AMAZON]{.co}

Expect "write a query" on paper, a normal-form definition, and one concurrency story. A strong answer states the assumption (which column is the key, whether nulls are possible), writes the query, and traces it on the sample data. The IP-allocation race in [Q12.26](#ps12){.ref} is the favourite for network roles.
:::

::: check
1. Which of `WHERE` and `HAVING` can use an aggregate? [^c12e-1]
2. Table `R(A, B, C)` with B → C and key A. Which normal form fails? [^c12e-2]
3. Can an index on (`site_id`, `vendor`) serve `WHERE vendor = 'Cisco'`? [^c12e-3]
4. Samples per day from 2,000 ports polled every 30 seconds? [^c12e-4]
:::

[^c12e-1]: Only `HAVING`, because `WHERE` runs before grouping.
[^c12e-2]: 3NF: C depends on B, a non-key attribute (a transitive dependency). It is in 2NF, since the key is a single attribute.
[^c12e-3]: No, the leftmost column is absent from the predicate.
[^c12e-4]: 2,000 × (86,400/30) = 2,000 × 2,880 = 5,760,000.

:::
