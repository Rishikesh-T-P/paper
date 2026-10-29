::: {.p11}

## [11.8]{.sec}The Case File: eighteen scenarios [Must · ■■□]{.tag} {#s11-8}

Each case follows the same layout so that it can be rehearsed aloud: the prompt as the interviewer says it, a topology (the accent marks where the fault lies, so cover it first and attempt the case), the clarifying questions with the answers the interviewer gives, the ranked hypotheses, a layer walk with the command and the *decisive output line*, the root cause, and then fix, verification, prevention and likely follow-ups. Cases 1 to 12 are the core; 13 to 16 are for strong candidates; 17 and 18 are optional. The tags after the title give the layers involved and the companies whose candidates report such scenarios.

| No. | The complaint | Layers | Level |
|-------|----------------------------------------------|-----------|-------|
| [1](#c11-1){.ref} | Internet works by IP, not by name | L3, L7 | Must |
| [2](#c11-2){.ref} | Same VLAN, different switches, cannot talk | L2 | Must |
| [3](#c11-3){.ref} | Inter-VLAN routing broken for one VLAN | L2, L3 | Must |
| [4](#c11-4){.ref} | Slow file transfers after a cable swap | L1, L2 | Must |
| [5](#c11-5){.ref} | SSH works, big transfers over the VPN hang | L3, L4 | Must |
| [6](#c11-6){.ref} | OSPF neighbours stuck in ExStart | L3 | Must |
| [7](#c11-7){.ref} | OSPF neighbour never appears | L3 | Must |
| [8](#c11-8){.ref} | BGP session stuck in Active | L3, L4 | Must |
| [9](#c11-9){.ref} | BGP up, but a prefix is not advertised or installed | L3 | Must |
| [10](#c11-10){.ref} | One server drops for a minute, several times an hour | L2, L3 | Must |
| [11](#c11-11){.ref} | A whole floor went down when someone plugged in a switch | L2 | Must |
| [12](#c11-12){.ref} | New VLAN's clients get 169.254 addresses | L2, L3, L7 | Must |
| [13](#c11-13){.ref} | Traffic works one way through the firewalls | L3, L4 | Should |
| [14](#c11-14){.ref} | Website slow for some users only | L1 to L3 | Should |
| [15](#c11-15){.ref} | VPN tunnel up, but no traffic | L3, security | Should |
| [16](#c11-16){.ref} | Linux service: refused, then timeout | L4, L7 | Should |
| [17](#c11-17){.ref} | Throughput between Mumbai and Frankfurt is terrible | L4 | Optional |
| [18](#c11-18){.ref} | Traceroute shows a scary loss at hop 4 | L3 | Optional |

### Case 1 · Internet works by IP, not by name [Must · ■□□]{.tag} {#c11-1}

[L3 · L7 · CISCO · GOOGLE · MICROSOFT · AMAZON]{.where}

**Prompt.** "A user says the internet is down."

<figure>
<svg viewBox="0 0 480 150" width="480">
<line class="ln" x1="40" y1="45" x2="130" y2="45"/>
<line class="ln" x1="130" y1="45" x2="240" y2="45"/>
<line class="ln" x1="240" y1="45" x2="350" y2="45"/>
<line class="ln" x1="350" y1="45" x2="440" y2="45"/>
<line class="ln" x1="240" y1="45" x2="240" y2="100"/>
<rect class="box" x="25" y="35" width="30" height="20" rx="1"/><path class="ln" d="M32,59 L48,59"/><rect class="fill" x="29" y="39" width="22" height="11"/>
<text class="lbl" x="40" y="71" text-anchor="middle">PC</text>
<text class="sm" x="40" y="80" text-anchor="middle">192.168.10.25</text>
<rect class="box" x="108" y="34" width="44" height="22" rx="2"/><path class="ln" d="M117,42 L143,42 M139,39 L143,42 L139,45 M143,49 L117,49 M121,46 L117,49 L121,52"/>
<text class="lbl" x="130" y="69" text-anchor="middle">SW1</text>
<rect class="box" x="218" y="34" width="44" height="22" rx="2"/><path class="ln" d="M227,42 L253,42 M249,39 L253,42 L249,45 M253,49 L227,49 M231,46 L227,49 L231,52"/><rect class="acc" x="215" y="31" width="50" height="28" rx="3"/>
<text class="sm" x="240" y="17" text-anchor="middle">Vlan10 192.168.10.1</text>
<text class="lbl" x="240" y="26" text-anchor="middle">Core</text>
<circle class="box" cx="350" cy="45" r="13"/><path class="ln" d="M343,45 L357,45 M350,38 L350,52 M345,40 L355,50 M345,50 L355,40"/>
<text class="lbl" x="350" y="71" text-anchor="middle">Edge</text>
<text class="sm" x="350" y="80" text-anchor="middle">NAT</text>
<path class="box" d="M412,56 C400,56 400,40 414,40 C414,26 438,22 446,34 C458,28 474,40 466,48 C478,50 474,56 464,56 Z"/>
<text class="lbl" x="440" y="71" text-anchor="middle">ISP</text>
<rect class="box" x="226" y="85" width="28" height="30" rx="1"/><path class="ln" d="M226,95 L254,95 M226,105 L254,105"/><circle class="accf" cx="248" cy="90" r="1.2" style="fill:#1A1D23"/>
<text class="lbl" x="240" y="128" text-anchor="middle">DNS</text>
<text class="sm" x="240" y="137" text-anchor="middle">192.168.50.53</text>
<text class="sm acct" x="110" y="126" text-anchor="middle">DHCP option 6 hands out 192.168.10.53</text>
</svg>
<figcaption><b>Figure 11.9</b> Case 1. The VLAN 10 DHCP scope hands out a DNS address in the wrong subnet.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| Everyone or one user? | Every user in VLAN 10; other VLANs are fine |
| What exactly fails? | Browser: "server not found" (`DNS_PROBE_FINISHED_NXDOMAIN`) |
| Does `ping 8.8.8.8` work? | Yes |
| Any change? | The VLAN 10 DHCP scope was edited yesterday |

**Hypotheses, ranked.** (1) DHCP hands out a wrong DNS server; (2) the DNS server is down; (3) an ACL blocks port 53 from VLAN 10.

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L1 to L3 | `ping 8.8.8.8` | `Reply from 8.8.8.8: bytes=32 time=18ms TTL=113` | Link, gateway, NAT and ISP work; lower layers are skipped, and we say why |
| L7 | `ipconfig /all` | `DNS Servers . . . : 192.168.10.53` | The client uses an address in its own subnet where no server lives |
| L7 | `nslookup google.com 192.168.50.53` | `Name: google.com` | The real DNS server is healthy |
| L7 | `dig @192.168.10.53 google.com` | `;; connection timed out; no servers could be reached` | The handed-out address is dead |
| L7 | `show running-config`, section dhcp | `dns-server 192.168.10.53` | The scope holds the typo |


**Root cause.** DHCP option 6 in the VLAN 10 scope was typed as 192.168.10.53 instead of 192.168.50.53. This explains why only VLAN 10 fails and why raw IP connectivity is intact.

**Fix.** `ip dhcp pool VLAN10`, then `dns-server 192.168.50.53`; clients renew with `ipconfig /renew`. As an interim step, users may enter the correct DNS server by hand.

**Verify.** `nslookup` succeeds from two clients and the browser loads a page.

**Prevent.** Generate scopes from the address plan, and add a post-change test that resolves a name from a client in every scope. DHCP and DNS are taught in [§3.6](#s3-6){.ref} and [§3.10](#s3-10){.ref}.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| If only some names fail? | Suspect split-horizon DNS, a conditional forwarder, or negative caching (the SOA minimum TTL). |
| Why does a ping to a public IP prove so much? | It crosses the local link, the VLAN, the gateway, the NAT and the ISP; only DNS and the layers above remain. |
| What if the DNS server itself were down? | `dig @192.168.50.53` would time out as well, and the fix would be there, not in the scope. |

**Variant.** A wireless client reports "connected, no internet": a captive portal or a DHCP fault on the SSID ([Pillar 6](#ch6){.ref}).

### Case 2 · Same VLAN, different switches, cannot talk [Must · ■□□]{.tag} {#c11-2}

[L2 · CISCO · JUNIPER · ARISTA · NOKIA]{.where}

**Prompt.** "PC-A and PC-B are both in VLAN 20 but cannot ping each other."

<figure>
<svg viewBox="0 0 480 150" width="480">
<line class="ln" x1="40" y1="40" x2="150" y2="40"/>
<line class="acc" x1="150" y1="40" x2="330" y2="40"/>
<line class="ln" x1="330" y1="40" x2="440" y2="40"/>
<line class="ln" x1="150" y1="40" x2="150" y2="105"/>
<line class="ln" x1="330" y1="40" x2="330" y2="105"/>
<text class="sm" x="108" y="36" text-anchor="middle">Gi1/0/5</text>
<text class="sm" x="194" y="36" text-anchor="middle">Gi1/0/24</text>
<text class="sm" x="286" y="36" text-anchor="middle">Gi1/0/24</text>
<text class="sm" x="372" y="36" text-anchor="middle">Gi1/0/7</text>
<rect class="box" x="25" y="30" width="30" height="20" rx="1"/><path class="ln" d="M32,54 L48,54"/><rect class="fill" x="29" y="34" width="22" height="11"/>
<text class="lbl" x="40" y="66" text-anchor="middle">PC-A</text>
<text class="sm" x="40" y="75" text-anchor="middle">VLAN 20</text>
<rect class="box" x="128" y="29" width="44" height="22" rx="2"/><path class="ln" d="M137,37 L163,37 M159,34 L163,37 L159,40 M163,44 L137,44 M141,41 L137,44 L141,47"/>
<text class="lbl" x="150" y="21" text-anchor="middle">SW1</text>
<rect class="box" x="308" y="29" width="44" height="22" rx="2"/><path class="ln" d="M317,37 L343,37 M339,34 L343,37 L339,40 M343,44 L317,44 M321,41 L317,44 L321,47"/>
<text class="lbl" x="330" y="21" text-anchor="middle">SW2</text>
<rect class="box" x="425" y="30" width="30" height="20" rx="1"/><path class="ln" d="M432,54 L448,54"/><rect class="fill" x="429" y="34" width="22" height="11"/>
<text class="lbl" x="440" y="66" text-anchor="middle">PC-B</text>
<text class="sm" x="440" y="75" text-anchor="middle">VLAN 20</text>
<rect class="box" x="135" y="95" width="30" height="20" rx="1"/><path class="ln" d="M142,119 L158,119"/><rect class="fill" x="139" y="99" width="22" height="11"/>
<text class="lbl" x="150" y="131" text-anchor="middle">PC-C</text>
<text class="sm" x="150" y="140" text-anchor="middle">VLAN 10</text>
<rect class="box" x="315" y="95" width="30" height="20" rx="1"/><path class="ln" d="M322,119 L338,119"/><rect class="fill" x="319" y="99" width="22" height="11"/>
<text class="lbl" x="330" y="131" text-anchor="middle">PC-D</text>
<text class="sm" x="330" y="140" text-anchor="middle">VLAN 10</text>
<text class="sm acct" x="240" y="68" text-anchor="middle">trunk: allowed vlan 10</text>
</svg>
<figcaption><b>Figure 11.10</b> Case 2. VLAN 10 hosts cross the trunk; VLAN 20 hosts do not.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| Same subnet? | Yes, 10.20.0.0/24 |
| Do VLAN 10 hosts across the trunk work? | Yes |
| Any change? | The trunk was re-provisioned last night |
| Same-switch VLAN 20 pings? | They work |

**Hypotheses, ranked.** (1) VLAN 20 missing from the trunk's allowed list; (2) VLAN 20 not created on SW2; (3) native VLAN mismatch; (4) spanning tree blocking VLAN 20 only (it runs per VLAN).

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L1 | `show interfaces Gi1/0/24` | `up, line protocol is up`; 0 CRC | The link is clean |
| L2 | `show interfaces trunk` on SW1 | `Vlans allowed on trunk: 10` | VLAN 20 is not carried |
| L2 | `show vlan brief` on SW2 | `20 ENG active Gi1/0/7` | The VLAN exists; hypothesis 2 is ruled out |
| L2 | `show mac address-table vlan 20` on SW1 | PC-A listed; PC-B's MAC absent | Frames from PC-B never arrive |
| L2 | `ip neigh` on PC-A | `10.20.0.7 dev eth0 FAILED` | ARP gets no answer |


**Root cause.** The re-provisioning used `switchport trunk allowed vlan 10`, which *replaces* the list, instead of `add`. Trunks and VLANs are taught in [§4.2](#s4-2){.ref}.

**Fix.** `switchport trunk allowed vlan add 20` on both ends.

**Verify.** `show interfaces trunk` lists 20 under allowed, active and forwarding; the MAC of PC-B is learnt; the ping works.

**Prevent.** Build trunks from a template that sets the list explicitly, and diff the allowed list after every change.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| What shows a native VLAN mismatch? | `%CDP-4-NATIVE_VLAN_MISMATCH` in the log, and frames leaking between VLANs. |
| How would you see it on Junos? | `show ethernet-switching interface` and `show vlans`. |
| Which list on the trunk shows a spanning-tree block? | The third: VLANs in forwarding state and not pruned. |

**Variant.** The VLAN is allowed and active, but absent from the forwarding list: a per-VLAN root disagreement is blocking it on this trunk.

::: trap
*Claim:* "`allowed vlan 20` adds VLAN 20 to the trunk." *Why it is wrong:* without the keyword `add`, the command replaces the whole list. *Correct statement:* use `switchport trunk allowed vlan add 20`.
:::

### Case 3 · Inter-VLAN routing broken for one VLAN [Must · ■□□]{.tag} {#c11-3}

[L2 · L3 · CISCO · AMAZON · JUNIPER]{.where}

**Prompt.** "Hosts in VLAN 30 can ping each other but nothing outside their VLAN."

<figure>
<svg viewBox="0 0 480 160" width="480">
<line class="ln" x1="240" y1="50" x2="130" y2="115"/>
<line class="ln" x1="240" y1="50" x2="350" y2="115"/>
<line class="ln" x1="130" y1="115" x2="50" y2="115"/>
<line class="ln" x1="350" y1="115" x2="430" y2="115"/>
<text class="sm" x="162" y="102">Gi1/0/48</text>
<text class="sm" x="318" y="102" text-anchor="end">Gi1/0/48</text>
<rect class="box" x="218" y="39" width="44" height="22" rx="2"/><path class="ln" d="M227,47 L253,47 M249,44 L253,47 L249,50 M253,54 L227,54 M231,51 L227,54 L231,57"/><rect class="acc" x="215" y="36" width="50" height="28" rx="3"/>
<text class="sm" x="240" y="22" text-anchor="middle">SVIs Vlan10, 20, 30</text>
<text class="lbl" x="240" y="31" text-anchor="middle">Core</text>
<rect class="box" x="108" y="104" width="44" height="22" rx="2"/><path class="ln" d="M117,112 L143,112 M139,109 L143,112 L139,115 M143,119 L117,119 M121,116 L117,119 L121,122"/>
<text class="lbl" x="130" y="139" text-anchor="middle">ASW1</text>
<rect class="box" x="328" y="104" width="44" height="22" rx="2"/><path class="ln" d="M337,112 L363,112 M359,109 L363,112 L359,115 M363,119 L337,119 M341,116 L337,119 L341,122"/>
<text class="lbl" x="350" y="139" text-anchor="middle">ASW2</text>
<rect class="box" x="35" y="105" width="30" height="20" rx="1"/><path class="ln" d="M42,129 L58,129"/><rect class="fill" x="39" y="109" width="22" height="11"/>
<text class="lbl" x="50" y="141" text-anchor="middle">VLAN 30</text>
<rect class="box" x="415" y="105" width="30" height="20" rx="1"/><path class="ln" d="M422,129 L438,129"/><rect class="fill" x="419" y="109" width="22" height="11"/>
<text class="lbl" x="430" y="141" text-anchor="middle">VLAN 30</text>
<text class="sm acct" x="240" y="125" text-anchor="middle">Vlan30: 10.30.0.1/24</text>
</svg>
<figcaption><b>Figure 11.11</b> Case 3. The core switch has SVIs for three VLANs; Vlan30 is the new one.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| Can they ping their gateway 10.30.0.1? | No |
| Do other VLANs route? | Yes, so `ip routing` is on |
| Anything new? | VLAN 30 was created this week |

**Hypotheses, ranked.** (1) the SVI is shut or down; (2) VLAN 30 is missing from the core's VLAN database or the uplink trunk; (3) hosts have a wrong gateway or mask.

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L3 | `ipconfig` on a host | Gateway `10.30.0.1`, mask `255.255.255.0` | The host settings are correct |
| L3 | `show ip interface brief`, line Vlan30 | `Vlan30  10.30.0.1  YES manual administratively down down` | The SVI is shut |
| L2 | after `no shutdown`: same command | `up   down` | Layer 1 up, but the VLAN has no forwarding port |
| L2 | `show vlan brief` on the core | VLAN 30 absent | The VLAN was created only on the access switch |


**Root cause.** Two faults in series: the SVI was shut, and VLAN 30 was neither defined on the core nor allowed on the uplink. An SVI comes up only when its VLAN exists and has at least one port up in that VLAN (the *autostate* rule, [§4.2](#s4-2){.ref}).

**Fix.** `vlan 30` on the core; `switchport trunk allowed vlan add 30` on the uplinks; `interface vlan 30`, then `no shutdown`.

**Verify.** `show ip interface brief` shows `up up`; a host pings the gateway and then the outside; `show ip route connected` lists 10.30.0.0/24.

**Prevent.** A provisioning playbook that creates the VLAN, the trunk membership and the SVI together, with a post-check.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| What brings an SVI up? | The VLAN exists, at least one port or trunk in it is up and forwarding, and the SVI is not shut. |
| Router-on-a-stick variant? | A missing sub-interface, a wrong `encapsulation dot1Q 30`, or a trunk that does not carry the VLAN. |
| What does `switchport autostate exclude` do? | It stops a port (for example a sniffer) from keeping the SVI up. |

**Variant.** The gateway answers but the hosts carry a /16 mask: ARP for outside addresses is attempted locally and fails.

### Case 4 · Slow file transfers after a cable swap [Must · ■■□]{.tag} {#c11-4}

[L1 · L2 · CISCO · QUALCOMM · BROADCOM · ARISTA]{.where}

**Prompt.** "Since yesterday copying files to the file server is painfully slow; web browsing seems fine."

<figure>
<svg viewBox="0 0 480 120" width="480">
<line class="acc" x1="50" y1="45" x2="190" y2="45"/>
<line class="ln" x1="190" y1="45" x2="320" y2="45"/>
<line class="ln" x1="320" y1="45" x2="430" y2="45"/>
<text class="sm" x="146" y="41" text-anchor="middle">Gi1/0/10</text>
<rect class="box" x="36" y="30" width="28" height="30" rx="1"/><path class="ln" d="M36,40 L64,40 M36,50 L64,50"/><circle class="accf" cx="58" cy="35" r="1.2" style="fill:#1A1D23"/><rect class="acc" x="33" y="27" width="34" height="36" rx="3"/>
<text class="lbl" x="50" y="73" text-anchor="middle">File server</text>
<text class="sm" x="50" y="82" text-anchor="middle">eth0 forced 100/full</text>
<rect class="box" x="168" y="34" width="44" height="22" rx="2"/><path class="ln" d="M177,42 L203,42 M199,39 L203,42 L199,45 M203,49 L177,49 M181,46 L177,49 L181,52"/>
<text class="lbl" x="190" y="69" text-anchor="middle">SW1</text>
<text class="sm" x="190" y="78" text-anchor="middle">Gi1/0/10 auto</text>
<rect class="box" x="298" y="34" width="44" height="22" rx="2"/><path class="ln" d="M307,42 L333,42 M329,39 L333,42 L329,45 M333,49 L307,49 M311,46 L307,49 L311,52"/>
<text class="lbl" x="320" y="69" text-anchor="middle">Core</text>
<rect class="box" x="415" y="35" width="30" height="20" rx="1"/><path class="ln" d="M422,59 L438,59"/><rect class="fill" x="419" y="39" width="22" height="11"/>
<text class="lbl" x="430" y="71" text-anchor="middle">Users</text>
</svg>
<figcaption><b>Figure 11.12</b> Case 4. The server NIC is forced to 100/full; the switch port is left on auto.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| All users, or one server? | One server |
| What changed? | The cable and NIC were replaced and "tuned" |
| Any error messages? | None |
| Throughput measured? | About 2 Mb/s against the usual 900 Mb/s |

**Hypotheses, ranked.** (1) duplex mismatch; (2) bad cable (CRC); (3) NIC offload or driver; (4) uplink congestion.

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L1 | `show interfaces Gi1/0/10` on the switch | `Half-duplex, 100Mb/s`; `1554 late collision`, `8412 runts` | The auto side fell back to half duplex |
| L1 | `ethtool eth0` on the server | `Speed: 100Mb/s`, `Duplex: Full`, `Auto-negotiation: off` | The forced side believes it is full duplex |
| L1 | `ethtool -S eth0` for the crc counters, twice, 10 s apart | `rx_crc_errors` rises between snapshots | Proves the fault is current, not historic |
| L4 | `ss -ti` during a copy | `retrans:3/412` | Bulk TCP collapses on loss; interactive traffic hardly notices |


**Root cause.** A duplex mismatch. A port that does not negotiate is not seen by the auto side, which therefore picks the speed by parallel detection but defaults to half duplex. The half-duplex side detects collisions (late collisions, runts) when the full-duplex side transmits at will; the full-duplex side logs CRC errors from the truncated frames. The mechanism is in [§3.3](#s3-3){.ref}.

**Fix.** Set both ends to auto (preferred), or both forced identically: `ethtool -s eth0 autoneg on`.

**Verify.** 1000/full on both sides, counters stop rising, and `iperf3` reaches about 940 Mb/s.

**Prevent.** An auto/auto policy, and an alert on the rate of late collisions and CRC errors.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| Which side shows late collisions, and which CRC? | The half-duplex side shows late collisions and runts; the full-duplex side shows CRC and frame errors. |
| CRC errors with matching duplex? | Suspect the cable, the optic (`show interfaces transceiver`) or interference. |
| Why is browsing fine but the copy slow? | Short flows carry little data, whereas bulk flows meet the loss and TCP backs off. |

**Variant.** A NIC offload or driver bug gives the same slowness with no errors on the switch; compare `ethtool -k` and driver versions.

### Case 5 · SSH works, big transfers over the VPN hang [Must · ■■□]{.tag} {#c11-5}

[L3 · L4 · GOOGLE · AMAZON · CISCO · JUNIPER · MICROSOFT]{.where}

**Prompt.** "Branch users can open the intranet login page over the site-to-site VPN, but large pages and downloads hang. SSH is fine."

<figure>
<svg viewBox="0 0 480 125" width="480">
<line class="ln" x1="30" y1="45" x2="100" y2="45"/>
<line class="acc dash" x1="100" y1="45" x2="305" y2="45"/>
<line class="ln" x1="100" y1="45" x2="205" y2="45"/>
<line class="ln" x1="205" y1="45" x2="305" y2="45"/>
<line class="ln" x1="305" y1="45" x2="380" y2="45"/>
<line class="ln" x1="380" y1="45" x2="448" y2="45"/>
<rect class="box" x="15" y="35" width="30" height="20" rx="1"/><path class="ln" d="M22,59 L38,59"/><rect class="fill" x="19" y="39" width="22" height="11"/>
<text class="lbl" x="30" y="71" text-anchor="middle">Branch PC</text>
<circle class="box" cx="100" cy="45" r="13"/><path class="ln" d="M93,45 L107,45 M100,38 L100,52 M95,40 L105,50 M95,50 L105,40"/>
<text class="lbl" x="100" y="71" text-anchor="middle">Branch rtr</text>
<path class="box" d="M177,56 C165,56 165,40 179,40 C179,26 203,22 211,34 C223,28 239,40 231,48 C243,50 239,56 229,56 Z"/>
<text class="lbl" x="205" y="71" text-anchor="middle">Internet</text>
<circle class="box" cx="305" cy="45" r="13"/><path class="ln" d="M298,45 L312,45 M305,38 L305,52 M300,40 L310,50 M300,50 L310,40"/>
<text class="lbl" x="305" y="71" text-anchor="middle">HQ VPN rtr</text>
<rect class="box" x="360" y="33" width="40" height="24" rx="1"/><path class="ln" d="M360,45 L400,45 M373,33 L373,45 M387,33 L387,45 M380,45 L380,57 M366,45 L366,57 M394,45 L394,57"/><rect class="acc" x="357" y="30" width="46" height="30" rx="3"/>
<text class="lbl" x="380" y="70" text-anchor="middle">HQ FW</text>
<text class="sm" x="380" y="79" text-anchor="middle">drops ICMP</text>
<rect class="box" x="434" y="30" width="28" height="30" rx="1"/><path class="ln" d="M434,40 L462,40 M434,50 L462,50"/><circle class="accf" cx="456" cy="35" r="1.2" style="fill:#1A1D23"/>
<text class="lbl" x="448" y="73" text-anchor="middle">Server</text>
<text class="sm acct" x="205" y="105" text-anchor="middle">IPsec tunnel, path MTU about 1400</text>
</svg>
<figcaption><b>Figure 11.13</b> Case 5. The HQ firewall behind the VPN router drops all ICMP, including the "fragmentation needed" message.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| Small or large? | Small things work, large hang |
| Only over the VPN? | Yes |
| Recent change? | The HQ firewall was "hardened": all ICMP blocked |
| Which way does the bulk data flow? | Server to client |

**Hypotheses, ranked.** (1) a path-MTU-discovery black hole (ICMP type 3 code 4 blocked); (2) MSS not clamped on the tunnel; (3) servers set the DF bit.

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L3 | `ping -M do -s 1472 10.10.5.20` | `100% packet loss` | A full-size DF packet does not cross |
| L3 | `ping -M do -s 1372 10.10.5.20` | `1380 bytes from 10.10.5.20: ttl=62` | The path MTU is about 1400 |
| L3 | `tracepath -n 10.10.5.20` | `pmtu 1500` unchanged | The router's ICMP never returns, so discovery fails |
| L4 | `tcpdump` at the client | Handshake completes; full-size segments never arrive; server retransmits | The first big segment is the one lost |
| L4 | HQ firewall log | `ICMP type 3 code 4 from branch router dropped` | The proof of the black hole |


**Root cause.** Tunnel encapsulation lowers the usable MTU. The VPN router sends "fragmentation needed" to the server, the HQ firewall drops it, and the server keeps sending 1500-byte DF packets that are discarded: a *PMTUD black hole*. SSH works because its packets are small. Path-MTU discovery is taught in [§3.5](#s3-5){.ref}.

**Fix.** Permit ICMP type 3 code 4 (and, for IPv6, Packet Too Big); also clamp the MSS on the tunnel, `ip tcp adjust-mss 1360`, or on Linux `iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu`.

**Verify.** The large download completes, the SYN carries MSS 1360, and the DF ping at 1372 succeeds.

**Prevent.** A security policy that lists the essential ICMP types (RFC 4890 for IPv6), and a tunnel template with the MSS clamp.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| Why does SSH work? | Its packets are small and never reach the MTU limit. |
| What about UDP applications? | They have no MSS, so they need fragmentation or sizing in the application. |
| How do you size the clamp? | ESP in tunnel mode adds about 50 to 73 bytes (plus 8 for NAT-T), so configure MTU 1400 and MSS 1360 (MTU minus 40). |

**Variant.** IPv6: routers never fragment, so a filtered Packet Too Big message is fatal for every large flow.

::: lens
[GOOGLE · AMAZON · CISCO]{.co}

Asked as a symptom with the cause hidden. A strong answer reaches "size-dependent" within two questions, proposes the DF ping ladder as the test, and names both ICMP and the MSS clamp in the fix. Expect: "why does the ping at 1472 fail but 1372 pass?"
:::

### Case 6 · OSPF neighbours stuck in ExStart [Must · ■■□]{.tag} {#c11-6}

[L3 · CISCO · JUNIPER · NOKIA · ARISTA · AMAZON]{.where}

**Prompt.** "We added a link between R1 and R2 and OSPF will not come up; `show ip ospf neighbor` keeps showing ExStart."

<figure>
<svg viewBox="0 0 480 110" width="480">
<line class="acc" x1="130" y1="40" x2="350" y2="40"/>
<text class="sm" x="173" y="36" text-anchor="middle">10.0.12.1/30</text>
<text class="sm" x="307" y="36" text-anchor="middle">10.0.12.2/30</text>
<circle class="box" cx="130" cy="40" r="13"/><path class="ln" d="M123,40 L137,40 M130,33 L130,47 M125,35 L135,45 M125,45 L135,35"/>
<text class="lbl" x="130" y="66" text-anchor="middle">R1</text>
<text class="sm" x="130" y="75" text-anchor="middle">Gi0/2 MTU 1500</text>
<circle class="box" cx="350" cy="40" r="13"/><path class="ln" d="M343,40 L357,40 M350,33 L350,47 M345,35 L355,45 M345,45 L355,35"/><circle class="acc" cx="350" cy="40" r="16"/>
<text class="lbl" x="350" y="66" text-anchor="middle">R2</text>
<text class="sm" x="350" y="75" text-anchor="middle">Gi0/2 MTU 9000</text>
<text class="sm" x="240" y="98" text-anchor="middle">area 0 · R1 shows EXSTART</text>
</svg>
<figcaption><b>Figure 11.14</b> Case 6. Jumbo frames are configured on R2 only.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| Which state exactly? | ExStart on R1, Exchange then back on R2; it flaps |
| Do hellos pass? | Yes, 2-Way was reached |
| Interface MTUs? | "Not sure" |
| Vendors? | Mixed |

**Hypotheses, ranked.** (1) MTU mismatch; (2) duplicate router ID; (3) unicast problem for the DBD packets.

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L3 | `show ip ospf neighbor` | `2.2.2.2  1  EXSTART/DR  00:00:34  10.0.12.2  Gi0/2` | Hellos work; the database exchange does not |
| L3 | `debug ip ospf adj` | `Nbr 2.2.2.2 has larger interface MTU` | R1 rejects R2's description packets |
| L1 | `show interfaces Gi0/2`, MTU line, on each router | `MTU 1500` on R1, `MTU 9000` on R2 | The mismatch |


**Root cause.** A database description packet carries the sender's interface MTU, and a router rejects one that advertises a larger MTU than its own, so the exchange never completes ([§4.5](#s4-5){.ref}).

**Fix.** Match the MTUs. `ip ospf mtu-ignore` is a stop-gap only, because large updates may then be dropped.

**Verify.** The neighbour reaches Full, `show ip route ospf` lists the remote prefixes, and the databases agree.

**Prevent.** Link templates set MTU on both ends, and an automation pre-check compares them.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| State the OSPF neighbour states. | Down, Init, 2-Way, ExStart, Exchange, Loading, Full. |
| What keeps a neighbour in Init? | One-way hellos: an ACL, a multicast problem, or a passive interface on the far side. |
| What does a duplicate router ID look like? | Flapping adjacencies and flushed LSAs, with `%OSPF-4-DUP_RTRID` in the log. |

**Variant.** On a non-broadcast link, a network-type mismatch gives different timers (10 and 40 s against 30 and 120 s) and no adjacency.

::: trap
*Claim:* "`ip ospf mtu-ignore` fixes it." *Why it is wrong:* it hides the mismatch, and a full-size LSU can later be lost on the smaller side. *Correct statement:* make the MTUs equal, and use the command only as a documented temporary measure.
:::


::: lens
[CISCO · JUNIPER · NOKIA]{.co}

Often asked as a pure recall question, "stuck in ExStart". The full answer gives the mechanism (the MTU field in the database description), the proof (`debug ip ospf adj`) and the objection to `mtu-ignore`. Expect: "what is checked in a DBD packet?"
:::

:::
