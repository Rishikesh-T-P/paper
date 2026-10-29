::: {.chapter .p4}
::: opener
[Part I · Pillar 4]{.part-label}

[4]{.num}

# Routing and Switching, CCNA to CCNP ENCOR {#ch4}

[A packet crosses a campus, an ISP and the Internet; we learn who decides each hop, and why.]{.promise}

1. [4.1 Inside the box: planes and the CLI]{} [SHOULD]{}
2. [4.2 Switching, VLANs, trunking, inter-VLAN routing]{} [MUST]{}
3. [4.3 Spanning Tree and EtherChannel]{} [MUST]{}
4. [4.4 The routing table, static and default routes]{} [MUST]{}
5. [4.5 OSPF]{} [MUST]{}
6. [4.6 EIGRP]{} [OPTIONAL]{}
7. [4.7 BGP]{} [MUST]{}
8. [4.8 First-hop redundancy]{} [SHOULD]{}
9. [4.9 Route control: prefix lists, route maps, redistribution, VRF-lite]{} [SHOULD]{}
10. [4.10 MPLS and L3VPN]{} [SHOULD]{}
11. [4.11 Quality of Service]{} [SHOULD]{}
12. [4.12 IP multicast]{} [OPTIONAL]{}
13. [4.13 IP services and access lists on IOS]{} [MUST]{}
14. [4.14 Tunnels and enterprise architecture]{} [OPTIONAL]{}
:::

Every topology and lab in this chapter belongs to one fictional organisation, **Campus Net**: a university network with a sales-and-engineering office floor (VLANs 10 and 20), two border routers, BR1 and BR2, and two upstream providers, ISP-A (AS 100) and ISP-B (AS 200). Subnetting, NAT theory, the longest-prefix-match algorithm, Dijkstra, access-list theory and the internals of the forwarding hardware are taught in their home chapters, and are cited here by one sentence and a page reference. This chapter teaches what is configured on the devices, what the protocols do on the wire, and how each is verified. The CCNA topics are mixed with the CCNP ENCOR topics; the tags tell you which to read first.

## [4.1]{.sec}Inside the box: planes and the CLI [Should · ■□□]{.tag} {#s4-1}

A router or switch performs three jobs that run at three different speeds. The *management plane* (the CLI, SSH, SNMP, NETCONF) is how humans and tools configure it. The *control plane* (OSPF, BGP, spanning tree, ARP) runs on the CPU and builds tables. The *data plane* (the forwarding hardware) uses those tables to move transit packets at line rate, without involving the CPU. The tables are the routing information base (RIB) and the forwarding information base (FIB); how the FIB is held in TCAM is taught in [§5.2](#s5-2){.ref}. Here it is enough to know that a packet *addressed to the router* (an OSPF hello, an SSH session) is punted to the CPU, whereas a *transit* packet never leaves the fast path.

<figure>
<svg viewBox="0 0 480 150" width="480">
  <defs><marker id="a41" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#1A1D23"/></marker></defs>
  <rect class="box" x="20" y="8" width="230" height="30" rx="2"/><text class="lbl" x="135" y="27" text-anchor="middle">Management plane: CLI, SSH, SNMP, NETCONF</text>
  <rect class="box" x="20" y="52" width="230" height="38" rx="2"/><text class="lbl" x="135" y="68" text-anchor="middle">Control plane (CPU): OSPF, BGP, STP</text><text class="sm" x="135" y="82" text-anchor="middle">protocols fill the RIB, which is compiled into the FIB</text>
  <rect class="box" x="20" y="104" width="230" height="38" rx="2"/><text class="lbl" x="135" y="120" text-anchor="middle">Data plane (ASIC): FIB, TCAM</text><text class="sm" x="135" y="134" text-anchor="middle">forwards transit packets at line rate</text>
  <line class="ln" x1="135" y1="90" x2="135" y2="104" marker-end="url(#a41)"/>
  <rect class="fill" x="300" y="112" width="50" height="22" rx="2"/><text class="sm" x="325" y="126" text-anchor="middle">transit</text>
  <line class="ln" x1="350" y1="123" x2="250" y2="123" marker-end="url(#a41)"/>
  <line class="ln" x1="440" y1="123" x2="440" y2="123"/>
  <rect class="fill" x="300" y="62" width="50" height="22" rx="2"/><text class="sm" x="325" y="76" text-anchor="middle">OSPF hello</text>
  <path class="acc" d="M300,73 L250,73" marker-end="url(#a41)"/>
  <text class="sm" x="360" y="76">punted to the CPU</text>
  <text class="sm" x="360" y="127">stays on the fast path</text>
</svg>
<figcaption><b>Figure 4.1</b> Three planes. A packet for the router (accent arrow) is punted to the control plane; a transit packet never leaves the data plane.</figcaption>
</figure>

The Cisco IOS command line has modes that are visible in the prompt: `Router>` (user), `Router#` (privileged), `Router(config)#` (global configuration) and `Router(config-if)#` or `Router(config-router)#` (a sub-mode). `enable` and `configure terminal` go up a level, `exit` goes back one and `end` returns to privileged mode. `show running-config` displays the active configuration in RAM, whereas `show startup-config` displays the copy in NVRAM that survives a reload; `copy running-config startup-config` saves. Prefix a privileged command with `do` to run it from a configuration mode, and use `?` and the Tab key freely, because abbreviations (`sh ip int br`) are accepted when unambiguous.

::: example
**The first fifteen minutes on a new Campus Net router.**

1. Name the device and protect privileged mode with a hashed secret, because `enable password` is stored readably.
2. Create a local user and enable SSH, which needs a hostname, a domain name and an RSA key.
3. Restrict the virtual terminal lines to SSH, address the interfaces, add a banner and save.

```
hostname BR1
ip domain-name campus.example
enable secret S3cr3t!
username admin privilege 15 secret Adm1n!
crypto key generate rsa modulus 2048
ip ssh version 2
line vty 0 4
 login local
 transport input ssh
interface GigabitEthernet0/1
 ip address 192.0.2.2 255.255.255.252
 no shutdown
banner motd # Authorised use only #
end
copy running-config startup-config
```

```
BR1# show ip interface brief
Interface           IP-Address     OK? Method Status  Protocol
GigabitEthernet0/1  192.0.2.2      YES manual up      up
BR1# show ip ssh
SSH Enabled - version 2.0
```

[Result: Status is the Layer 1 state and Protocol the Layer 2 state; "up/up" is the only healthy pair.]{.result}
:::

<figure>
<svg viewBox="0 0 480 150" width="480">
  <defs><marker id="s41" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#1A1D23"/></marker></defs>
  <rect class="box" x="10" y="10" width="110" height="24"/><text class="mono" x="65" y="26" text-anchor="middle">Router&gt;</text><text class="sm" x="128" y="26">user EXEC: look, ping</text>
  <rect class="box" x="40" y="42" width="130" height="24"/><text class="mono" x="105" y="58" text-anchor="middle">Router#</text><text class="sm" x="178" y="58">privileged EXEC: show, copy, debug</text>
  <rect class="box" x="70" y="74" width="150" height="24"/><text class="mono" x="145" y="90" text-anchor="middle">Router(config)#</text><text class="sm" x="228" y="90">global configuration</text>
  <rect class="box" x="100" y="106" width="150" height="24"/><text class="mono" x="175" y="122" text-anchor="middle">Router(config-if)#</text><text class="sm" x="258" y="122">sub-mode: interface, router, line, vlan</text>
  <path class="acc" d="M40,36 L40,42 M70,68 L70,74 M100,100 L100,106"/>
  <text class="sm" x="330" y="14">enable / disable</text><text class="sm" x="330" y="46">configure terminal / end</text><text class="sm" x="330" y="78">interface, router ... / exit</text>
</svg>
<figcaption><b>Figure 4.1b</b> The CLI modes. The prompt names the mode: <span class="mono">&gt;</span> user, <span class="mono">#</span> privileged, <span class="mono">(config...)#</span> a configuration mode.</figcaption>
</figure>

A device boots in a fixed order: the ROM monitor runs a power-on self-test, loads the operating-system image from flash, and then reads the saved configuration from NVRAM; if none exists it offers the setup dialogue. The *configuration register* (`show version` prints it, normally 0x2102) controls this. Setting it to 0x2142 makes the router ignore the saved configuration at the next boot, which is the basis of password recovery: boot with 0x2142, copy the startup configuration into running configuration, change the secret, restore 0x2102 and save. Physical access is therefore equivalent to administrative access, which is why console ports are kept in locked rooms.

Packet forwarding has also evolved in three generations. *Process switching* sends every packet to the CPU, which looks up the route and rebuilds the header; it is the slowest and is used today only for packets addressed to the router. *Fast switching* caches the result of the first packet of a flow. *Cisco Express Forwarding* (CEF) precomputes two tables, the FIB (a copy of the best routes, organised for longest-prefix lookup) and the *adjacency table* (the Layer 2 rewrite string for each next hop, including its MAC address learnt by ARP), and forwards every packet by a single lookup in each. On a switch or high-end router those tables sit in hardware. A missing adjacency, for instance because ARP failed, produces packet drops that `show ip cef` and `show adjacency` reveal even when the route looks correct.

<figure>
<svg viewBox="0 0 480 100" width="480">
  <defs><marker id="s41b" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#1A1D23"/></marker></defs>
  <rect class="box" x="10" y="24" width="130" height="40" rx="2"/><text class="lbl" x="75" y="40" text-anchor="middle">RIB</text><text class="sm" x="75" y="54" text-anchor="middle">10.1.1.0/24 via 10.1.12.2</text>
  <rect class="box" x="175" y="24" width="130" height="40" rx="2"/><text class="lbl" x="240" y="40" text-anchor="middle">FIB</text><text class="sm" x="240" y="54" text-anchor="middle">10.1.1.0/24 to adjacency 7</text>
  <rect class="box" x="340" y="24" width="130" height="40" rx="2"/><text class="lbl" x="405" y="40" text-anchor="middle">Adjacency table</text><text class="sm" x="405" y="54" text-anchor="middle">Gi0/2, MAC aabb.cc00.0200</text>
  <line class="ln" x1="140" y1="44" x2="175" y2="44" marker-end="url(#s41b)"/><line class="ln" x1="305" y1="44" x2="340" y2="44" marker-end="url(#s41b)"/>
  <text class="sm" x="157" y="38" text-anchor="middle">best only</text><text class="sm" x="322" y="38" text-anchor="middle">ARP</text>
  <text class="sm" x="10" y="90">Control plane builds the RIB; CEF derives the FIB and the Layer 2 rewrite; the data plane reads only the last two.</text>
</svg>
<figcaption><b>Figure 4.1c</b> From routing table to forwarding. A transit packet needs one FIB lookup and one adjacency rewrite.</figcaption>
</figure>

[**Junos and FRR** — Junos has a candidate configuration: you edit it, run `commit`, and can `rollback 1`. IOS applies each line instantly. FRR's `vtysh` is IOS-like, and Arista EOS is almost identical to IOS.]{.margin}The same three planes exist on every vendor, but the commands differ. The table maps the five commands one uses most.

| Task | Cisco IOS-XE | Junos | Arista EOS | FRR (`vtysh`) |
|---|---|---|---|---|
| Interface summary | `show ip interface brief` | `show interfaces terse` | `show ip interface brief` | `show interface brief` |
| Routing table | `show ip route` | `show route` | `show ip route` | `show ip route` |
| OSPF neighbours | `show ip ospf neighbor` | `show ospf neighbor` | `show ip ospf neighbor` | `show ip ospf neighbor` |
| BGP summary | `show ip bgp summary` | `show bgp summary` | `show ip bgp summary` | `show bgp summary` |
| Save configuration | `copy run start` | `commit` | `write memory` | `write memory` |

Configuration is managed by copying it. `copy running-config tftp:` (or `scp:`) saves it off the device; `copy tftp: flash:` loads a new image; `show version` reports the image, the uptime and the register; `show running-config | section ospf` filters output. On a production device, change windows are protected by `configure replace` or by a rollback timer, because a mistyped command over SSH can cut the session that is needed to correct it.

CDP (Cisco) and LLDP (the open standard, IEEE 802.1AB) advertise a device's name, port and platform to its neighbours. `show cdp neighbors detail` is the quickest way to learn what is on the other end of a cable. Both are best disabled on ports facing untrusted users.

::: lab
`LAB 4.1 · 15 MIN`  Packet Tracer: two routers and one switch, base configuration and SSH as in the worked example. Then run the multi-vendor task on Containerlab, with one Nokia SR Linux and one Arista cEOS node.

```
BR1# show cdp neighbors detail | include Device|IP address
Device ID: SW1
  IP address: 192.168.99.2
```

**What you should notice:** CDP reveals the neighbour's address without a routing protocol. Fill in the equivalence table above for the other two vendors; the *concepts* (interface, route, neighbour) are the same, and only the commands differ.
:::

::: check
1. What does it mean when `show ip interface brief` prints "up/down"? [^c4-0a]
2. Why is `enable secret` preferred to `enable password`? [^c4-0b]
:::

[^c4-0a]: The line is up at Layer 1 but the protocol (Layer 2) is down, for example from a keepalive or encapsulation mismatch.
[^c4-0b]: It stores a hash; `enable password` stores a readable (or weakly obfuscated) string.

## [4.2]{.sec}Switching, VLANs, trunking and inter-VLAN routing [Must · ■□□]{.tag} {#s4-2}

::: bigidea
A VLAN divides one physical switch into several broadcast domains, because the switch refuses to forward a frame to a port of a different VLAN; a router, or a Layer 3 switch, is therefore required to carry traffic between them.
:::

<figure>
<svg viewBox="0 0 480 130" width="480">
  <text class="sm" x="10" y="12">Physical: one switch</text>
  <rect class="box" x="10" y="20" width="200" height="50" rx="2"/>
  <rect class="hl" x="20" y="30" width="30" height="14"/><rect class="hl" x="55" y="30" width="30" height="14"/><rect class="fill" x="90" y="30" width="30" height="14"/><rect class="fill" x="125" y="30" width="30" height="14"/><rect class="hl" x="160" y="30" width="30" height="14"/>
  <text class="sm" x="20" y="60">VLAN 10 (shaded yellow), VLAN 20 (grey)</text>
  <text class="sm" x="260" y="12">Logical: two switches, no link between them</text>
  <rect class="box" x="260" y="20" width="100" height="30" rx="2"/><text class="lbl" x="310" y="39" text-anchor="middle">SALES VLAN 10</text>
  <rect class="box" x="370" y="20" width="100" height="30" rx="2"/><text class="lbl" x="420" y="39" text-anchor="middle">ENG VLAN 20</text>
  <text class="sm" x="260" y="72">A broadcast in VLAN 10 never reaches a VLAN 20 port.</text>
  <text class="sm" x="10" y="100">Join the two only with a Layer 3 device: router, or switch with ip routing.</text>
  <rect class="accf" x="10" y="108" width="3" height="14"/><text class="sm" x="20" y="119">Every VLAN is normally one IP subnet.</text>
</svg>
<figcaption><b>Figure 4.1d</b> A VLAN is a logical switch. Ports of one colour behave as if they belonged to a separate device.</figcaption>
</figure>

A Layer 2 switch forwards on destination MAC address. It *learns* by reading the source MAC of every arriving frame and recording the (MAC, port, VLAN) triple in its MAC address table, which entries expire after 300 seconds of silence by default. For a known destination the frame leaves one port; for a broadcast, a multicast (without snooping) or an *unknown unicast* the switch floods the frame out of every other port in the VLAN. Thus, without VLANs, a single switch is a single broadcast domain, and every host hears every ARP request.

```
SW1# show mac address-table dynamic vlan 10
Vlan    Mac Address       Type     Ports
  10    0050.7966.6801    DYNAMIC  Gi0/1
  10    0050.7966.6802    DYNAMIC  Gi0/24
```

The forwarding decision of a switch can be summarised in a table. It also explains the failure modes met later: a flood is cheap in a small VLAN, but ruinous in a loop.

| Frame arriving in VLAN V | Destination | The switch |
|---|---|---|
| Unicast, MAC known | learnt on port P | forwards out of P only (filters if P is the arrival port) |
| Unicast, MAC unknown | not in table | floods out of all other ports in V (*unknown unicast flooding*) |
| Broadcast (ff:ff:ff:ff:ff:ff) | all hosts | floods out of all other ports in V |
| Multicast, no snooping | group | floods like a broadcast; with IGMP snooping only to joined ports |
| Source MAC new or moved | learning | records or updates the (MAC, port, VLAN) entry |

Two consequences follow. First, a MAC address appearing on two ports in quick succession ("MAC flapping") signals either a loop or a duplicated address. Secondly, the MAC table has finite size (a few thousand to hundreds of thousands of entries), so an attacker who sends frames with random source addresses can fill it and force the switch to flood everything; port security limits the number of addresses per port ([§9.5](#s9-5){.ref}).

An *access port* belongs to one VLAN and sends and receives untagged frames. A *trunk port* carries several VLANs on one link, and marks each frame with an IEEE 802.1Q tag so that the far end knows its VLAN. The tag is four bytes inserted between the source MAC and the EtherType, so the frame check sequence is recomputed and the maximum frame grows from 1518 to 1522 bytes.

<figure>
<svg viewBox="0 0 480 130" width="480">
  <text class="sm" x="10" y="12">Untagged frame</text>
  <rect class="box" x="10" y="18" width="80" height="24"/><text class="lbl" x="50" y="34" text-anchor="middle">Dest MAC 6</text>
  <rect class="box" x="90" y="18" width="80" height="24"/><text class="lbl" x="130" y="34" text-anchor="middle">Src MAC 6</text>
  <rect class="box" x="170" y="18" width="60" height="24"/><text class="lbl" x="200" y="34" text-anchor="middle">Type 2</text>
  <rect class="box" x="230" y="18" width="150" height="24"/><text class="lbl" x="305" y="34" text-anchor="middle">Payload 46 to 1500</text>
  <rect class="box" x="380" y="18" width="60" height="24"/><text class="lbl" x="410" y="34" text-anchor="middle">FCS 4</text>
  <text class="sm" x="10" y="68">802.1Q tagged frame (4 bytes inserted; FCS recomputed)</text>
  <rect class="box" x="10" y="74" width="60" height="24"/><text class="lbl" x="40" y="90" text-anchor="middle">Dest 6</text>
  <rect class="box" x="70" y="74" width="60" height="24"/><text class="lbl" x="100" y="90" text-anchor="middle">Src 6</text>
  <rect class="hl" x="130" y="74" width="56" height="24"/><rect class="box" x="130" y="74" width="56" height="24" fill="none"/><text class="lbl" x="158" y="90" text-anchor="middle">TPID 2</text>
  <rect class="hl" x="186" y="74" width="30" height="24"/><rect class="acc" x="186" y="74" width="30" height="24"/><text class="lbl" x="201" y="90" text-anchor="middle">PCP 3</text>
  <rect class="hl" x="216" y="74" width="22" height="24"/><rect class="acc" x="216" y="74" width="22" height="24"/><text class="lbl" x="227" y="90" text-anchor="middle">DEI</text>
  <rect class="hl" x="238" y="74" width="48" height="24"/><rect class="acc" x="238" y="74" width="48" height="24"/><text class="lbl" x="262" y="90" text-anchor="middle">VID 12</text>
  <rect class="box" x="286" y="74" width="46" height="24"/><text class="lbl" x="309" y="90" text-anchor="middle">Type 2</text>
  <rect class="box" x="332" y="74" width="100" height="24"/><text class="lbl" x="382" y="90" text-anchor="middle">Payload</text>
  <rect class="box" x="432" y="74" width="40" height="24"/><text class="lbl" x="452" y="90" text-anchor="middle">FCS</text>
  <text class="sm" x="130" y="116">TPID = 0x8100.  TCI (2 bytes) = PCP 3 bits | DEI 1 bit | VID 12 bits</text>
</svg>
<figcaption><b>Figure 4.2</b> The 802.1Q tag. Twelve VID bits give 4096 values, of which 0 and 4095 are reserved, hence 4094 usable VLANs.</figcaption>
</figure>

VLAN 1 is the default; 2 to 1001 are normal-range; 1002 to 1005 are reserved for legacy FDDI and Token Ring; 1006 to 4094 are extended. One VLAN on a trunk is the *native VLAN* (VLAN 1 by default), whose frames cross the trunk *untagged*. If the two ends disagree about it, frames leak between VLANs and CDP and spanning tree print a native-VLAN mismatch warning. Best practice is to set the native VLAN to an unused one (for example 99) on both ends and to prune the allowed list to the VLANs that need to cross.

::: example
**Two VLANs, one trunk, router on a stick.** Campus Net has SALES (VLAN 10, 192.168.10.0/24) and ENG (VLAN 20, 192.168.20.0/24). A SALES PC on SW1 and an ENG PC on SW2 must communicate. SW1 trunks to SW2 and to R1.

```
! SW1 and SW2
vlan 10
 name SALES
vlan 20
 name ENG
interface GigabitEthernet0/1
 switchport mode access
 switchport access vlan 10        ! PC on SW1 (SW2: access vlan 20)
interface GigabitEthernet0/24
 switchport mode trunk
 switchport trunk allowed vlan 10,20
 switchport trunk native vlan 99
! R1: one physical link, two sub-interfaces
interface GigabitEthernet0/0
 no shutdown
interface GigabitEthernet0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
interface GigabitEthernet0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
```

1. The SALES PC has no route to 192.168.20.0/24, so it ARPs for its gateway 192.168.10.1 and sends the packet to R1's MAC (untagged on the access port).
2. SW1 tags the frame with VID 10 on the trunk to R1. R1 reads the tag and delivers it to sub-interface .10.
3. R1 looks up 192.168.20.0/24, a connected route out of .20, rewrites the Layer 2 header and sends the packet back on the same cable, now tagged VID 20.
4. SW1 forwards the VID 20 frame over the trunk to SW2, which removes the tag and delivers it on the ENG access port.

[Result: the packet crosses the R1 link twice, which is why the design is called a hairpin and why that link limits inter-VLAN throughput.]{.result}
:::

<figure>
<svg viewBox="0 0 480 190" width="480">
  <defs><marker id="a42" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#1A1D23"/></marker><marker id="b42" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#21705A"/></marker></defs>
  <circle class="box" cx="240" cy="26" r="14"/><path class="ln" d="M232,18 L248,34 M248,18 L232,34"/><text class="lbl" x="268" y="30">R1</text>
  <rect class="box" x="195" y="92" width="90" height="26" rx="2"/><text class="lbl" x="240" y="109" text-anchor="middle">SW1</text>
  <rect class="box" x="370" y="92" width="90" height="26" rx="2"/><text class="lbl" x="415" y="109" text-anchor="middle">SW2</text>
  <rect class="box" x="20" y="150" width="80" height="24"/><text class="lbl" x="60" y="166" text-anchor="middle">SALES PC</text>
  <rect class="box" x="375" y="150" width="80" height="24"/><text class="lbl" x="415" y="166" text-anchor="middle">ENG PC</text>
  <line class="ln" x1="225" y1="92" x2="225" y2="42" marker-end="url(#a42)"/><text class="sm" x="219" y="68" text-anchor="end">2 VID 10</text>
  <line class="ln" x1="255" y1="42" x2="255" y2="92" marker-end="url(#b42)" stroke="#21705A"/><text class="sm" x="261" y="68">3 VID 20</text>
  <line class="ln" x1="285" y1="105" x2="365" y2="105" marker-end="url(#a42)"/><text class="sm" x="325" y="98" text-anchor="middle">4 VID 20</text>
  <line class="ln" x1="80" y1="150" x2="200" y2="118" marker-end="url(#a42)"/><text class="sm" x="104" y="146">1 untagged</text>
  <line class="ln" x1="415" y1="118" x2="415" y2="150" marker-end="url(#a42)"/><text class="sm" x="421" y="138">5 untagged</text>
  <text class="sm" x="10" y="12">trunks: SW1-R1, SW1-SW2 (native VLAN 99)</text>
</svg>
<figcaption><b>Figure 4.3</b> The router-on-a-stick hairpin. The packet enters R1 tagged 10 and leaves tagged 20 on the same link.</figcaption>
</figure>

A *Layer 3 switch* removes the hairpin. Enabling `ip routing` and creating a *switched virtual interface* (SVI) per VLAN lets the switch route in hardware between its own VLANs: `interface Vlan10` with `ip address 192.168.10.1 255.255.255.0` replaces the sub-interface, and hosts keep the same gateway address. SVIs scale better than sub-interfaces, because the forwarding is done by the switching ASIC rather than by a single router link. A *routed port* (`no switchport`) is a Layer 3 port with no VLAN at all.

```
SW1(config)# ip routing
SW1(config)# interface Vlan10
SW1(config-if)# ip address 192.168.10.1 255.255.255.0
SW1# show ip route connected
C  192.168.10.0/24 is directly connected, Vlan10
```

*Voice VLAN.* An IP phone and the PC behind it share one access port. The port is given a second, *voice* VLAN (`switchport voice vlan 150`); CDP or LLDP-MED tells the phone which VLAN to tag, while the PC's frames stay untagged in the access VLAN. The port behaves as a trunk with just two VLANs, and the voice traffic can then be placed in a separate IP subnet and a priority queue ([§4.11](#s4-11){.ref}).

```
interface GigabitEthernet0/5
 switchport mode access
 switchport access vlan 10
 switchport voice vlan 150
 spanning-tree portfast
 spanning-tree bpduguard enable
```

Two Layer 2 mechanisms deserve suspicion. The *Dynamic Trunking Protocol* (DTP) lets two ports negotiate a trunk; the outcome is in the table (a port set to `mode trunk` or `desirable` initiates, `auto` only agrees). An attacker who sends DTP frames to a port left on `dynamic auto` can turn it into a trunk and see every VLAN. The *VLAN Trunking Protocol* (VTP) distributes the VLAN database from servers to clients, and a switch that joins with a higher revision number and an empty database overwrites the VLANs of the whole domain (the "VTP bomb"). The remedy is to configure ports explicitly (`switchport mode access` or `trunk`, plus `switchport nonegotiate`), to use VTP transparent or off, and to shut down unused ports. Port security, DHCP snooping and VLAN-hopping defences are taught in [§9.5](#s9-5){.ref}.

<figure>
<svg viewBox="0 0 480 120" width="480">
  <defs><marker id="v42" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#1A1D23"/></marker></defs>
  <rect class="box" x="10" y="30" width="80" height="30" rx="2"/><text class="lbl" x="50" y="43" text-anchor="middle">Attacker</text><text class="sm" x="50" y="53" text-anchor="middle">access VLAN 1</text>
  <rect class="box" x="150" y="30" width="80" height="30" rx="2"/><text class="lbl" x="190" y="49" text-anchor="middle">SW1</text>
  <rect class="box" x="290" y="30" width="80" height="30" rx="2"/><text class="lbl" x="330" y="49" text-anchor="middle">SW2</text>
  <rect class="box" x="410" y="30" width="60" height="30" rx="2"/><text class="lbl" x="440" y="43" text-anchor="middle">Victim</text><text class="sm" x="440" y="53" text-anchor="middle">VLAN 20</text>
  <line class="ln" x1="90" y1="45" x2="150" y2="45" marker-end="url(#v42)"/><text class="sm" x="120" y="24" text-anchor="middle">[1][20][data]</text>
  <line class="ln" x1="230" y1="45" x2="290" y2="45" marker-end="url(#v42)"/><text class="sm" x="260" y="24" text-anchor="middle">[20][data]</text>
  <line class="ln" x1="370" y1="45" x2="410" y2="45" marker-end="url(#v42)"/>
  <text class="sm" x="10" y="90">SW1 strips the outer tag (1) because VLAN 1 is the native VLAN of the trunk and is sent untagged, leaving tag 20 for SW2.</text>
  <text class="sm" x="10" y="102">Defence: native VLAN unused (not 1) on every trunk; never put hosts in the native VLAN.</text>
</svg>
<figcaption><b>Figure 4.1e</b> VLAN hopping by double tagging. The attack is one-way (the reply cannot return) and works only when the attacker's access VLAN equals the trunk's native VLAN. Further defences are in §9.5.</figcaption>
</figure>

| Local \ Peer | access | trunk | dynamic auto | dynamic desirable |
|---|---|---|---|---|
| **access** | access | mismatch | access | access |
| **trunk** | mismatch | trunk | trunk | trunk |
| **dynamic auto** | access | trunk | access | trunk |
| **dynamic desirable** | access | trunk | trunk | trunk |

::: trap
*Claim:* two ports on `dynamic auto` will form a trunk. *Why it is wrong:* `auto` only responds to a negotiating peer and never initiates, so two `auto` ports both wait and settle on access mode. *Correct statement:* at least one end must be `trunk` or `desirable`; better, configure both ends statically.
:::

::: example
**Converting the design to an L3 switch.** Campus Net upgrades the trunk-to-R1 design: SW1 becomes the gateway, and R1 is kept only for the border.

1. Enable routing in the switch: `ip routing`.
2. Create `interface Vlan10` and `interface Vlan20` with the addresses that R1's sub-interfaces had (192.168.10.1 and 192.168.20.1). Hosts need no change.
3. Remove the R1 sub-interfaces. Make SW1's uplink a routed port with `no switchport` and a /30 to R1, and exchange routes with OSPF or a static route.
4. Confirm: the VLAN must exist and have at least one active port in the VLAN, or the SVI stays down.

```
SW1# show ip interface brief | include Vlan
Vlan10   192.168.10.1  YES manual up   up
Vlan20   192.168.20.1  YES manual up   up
```

[Result: inter-VLAN traffic never leaves SW1, and its capacity is the switching ASIC's, not one 1 Gb/s link's.]{.result}
:::

::: lens
[CISCO · JUNIPER · ARISTA]{.co}

Expected: the difference between access and trunk, what the native VLAN is, and the symptom of a mismatch; why 4094; ROAS against SVI. A strong answer volunteers the security point (DTP, native VLAN, VTP) and the hairpin bottleneck. Follow-ups: what is on the wire for a frame from VLAN 10 to VLAN 20; what happens when the trunk's allowed list omits a VLAN.
:::

::: lab
`LAB 4.2 · 15 MIN`  Build Figure 4.3 in Packet Tracer, then break it twice.

```
SW1(config-if)# switchport trunk native vlan 1      ! on one end only
SW1(config-if)# switchport trunk allowed vlan remove 20
```

```
%CDP-4-NATIVE_VLAN_MISMATCH: Native VLAN mismatch discovered on Gi0/24 (1), with SW2 Gi0/24 (99).
SALES-PC> ping 192.168.20.10
Request timed out.   <-- VLAN 20 no longer crosses the trunk
```

**What you should notice:** the native mismatch is only a log message and traffic may still flow; the pruned VLAN silently fails. `show interfaces trunk` shows the third table ("VLANs in spanning tree forwarding state and not pruned") shrinking.
:::

::: check
1. Why does a trunk frame grow to 1522 bytes? [^c4-1]
2. A host on VLAN 10 can ping its gateway but not a host in VLAN 20 on another switch. Name two causes. [^c4-2]
:::

[^c4-1]: The 4-byte 802.1Q tag is added to the maximum 1518-byte untagged frame.
[^c4-2]: VLAN 20 is missing from a trunk's allowed list or from SW2's VLAN database; or inter-VLAN routing (sub-interface or SVI) for VLAN 20 is down.

## [4.3]{.sec}Spanning Tree and EtherChannel [Must · ■■□]{.tag} {#s4-3}

::: bigidea
Ethernet frames carry no hop count, so a loop in the Layer 2 topology circulates a broadcast forever; the Spanning Tree Protocol (STP) therefore elects one root switch and blocks the minimum number of ports needed to leave a loop-free tree.
:::

Redundant switch links are desirable, yet a loop produces three failures at once: a *broadcast storm* (frames multiply and fill every link), *MAC table instability* (the same source appears on alternating ports) and duplicate frame delivery. Switches exchange *bridge protocol data units* (BPDUs) every two seconds to agree on a tree. The agreement uses four steps in this order:

1. **Root bridge.** The switch with the lowest *bridge ID* (BID) wins. The BID is the priority followed by the MAC address.
2. **Root port**, one on every non-root switch: the port with the lowest *root path cost*; ties go to the lowest *sender BID*, then the lowest *sender port ID*.
3. **Designated port**, one on every segment: the port of the switch advertising the lowest root path cost on that segment (ties again by sender BID, then port ID). Every port of the root bridge is designated.
4. **Blocked** (alternate) ports: all remaining ports.

<figure>
<svg viewBox="0 0 480 70" width="480">
  <rect class="box" x="10" y="14" width="60" height="30"/><text class="lbl" x="40" y="33" text-anchor="middle">Priority 4</text>
  <rect class="box" x="70" y="14" width="130" height="30"/><text class="lbl" x="135" y="33" text-anchor="middle">System ID extension 12</text>
  <rect class="fill" x="200" y="14" width="270" height="30"/><text class="lbl" x="335" y="33" text-anchor="middle">MAC address 48</text>
  <path class="acc" d="M10,52 L200,52"/><text class="sm" x="10" y="64">16-bit priority field = configured priority + VLAN ID (32768 + 1 = 32769)</text>
  <text class="sm" x="10" y="9">Bridge ID (64 bits). Only the top 4 bits are configurable, so priority moves in steps of 4096.</text>
</svg>
<figcaption><b>Figure 4.4</b> The bridge ID. The VLAN number occupies the low 12 bits, which is why the configurable priority must be a multiple of 4096.</figcaption>
</figure>

A BPDU carries the fields needed for the election: the *root bridge ID* the sender believes in, the *root path cost* from the sender, the *sender's own bridge ID* and the *sender port ID* (port priority, 128 by default, and port number), plus the timers (hello, forward delay, max age) set by the root. Only the root generates BPDUs; every other switch relays an updated copy through its designated ports, adding the cost of the link on which it was received. That is why a non-root switch's root path cost is, in effect, the sum of the costs of the links its BPDU crossed. When a switch stops hearing the root's BPDUs on its root port for max-age (20 s), it assumes the path is lost and starts a new election. A *topology change* (a port moving to or from forwarding) is signalled up to the root, which tells every switch to shorten its MAC-table ageing to 15 s, so stale entries do not blackhole traffic.

Link costs depend on speed. The classic (short) values are 10 Mb/s = 100, 100 Mb/s = 19, 1 Gb/s = 4 and 10 Gb/s = 2; the long values used by `spanning-tree pathcost method long` and by MST are 1 Gb/s = 20,000 and 10 Gb/s = 2,000. Because per-VLAN spanning tree (PVST+) runs an independent tree per VLAN, the BID includes the VLAN, and the default priority for VLAN 1 is displayed as 32769.

::: example
**Root election on the Campus Net triangle.** Three switches in VLAN 1, all at default priority 32768 (shown 32769), MACs ending 0001 (SW1), 0002 (SW2) and 0003 (SW3), joined pairwise by 1 Gb/s links (cost 4).

**Part 1. Default priorities.**

1. Priorities tie, so the lowest MAC wins: SW1 is root. All its ports are designated.
2. SW2 and SW3 each reach the root by their direct link at cost 4 (the path through the third switch costs 8), so each direct port is a root port.
3. On the SW2-SW3 segment both switches offer root path cost 4. The tie goes to the lower sender BID, SW2. SW2's port is designated; SW3's port is not a root or designated port, hence **alternate (blocking)**.

**Part 2. Set SW3's priority to 4096** (BID 4097 for VLAN 1).

4. SW3 now has the lowest BID and becomes root. SW1 and SW2 each reach SW3 directly at cost 4.
5. On the SW1-SW2 segment both offer cost 4; SW1's BID is lower, so SW1 is designated and SW2's port on that segment blocks.

**Part 3. Two parallel links SW1-SW2** (Gi0/1 and Gi0/2), SW1 root again.

6. SW2 has two candidate root ports with equal cost 4 and an identical sender BID. The tie goes to the lowest *sender port ID*: SW1's Gi0/1 (128.1) beats Gi0/2 (128.2). SW2's port that hears 128.2 becomes alternate.

[Result: three outcomes, each decided by a different step of the election: lowest MAC, lowest sender BID, lowest sender port ID.]{.result}
:::

<figure>
<svg viewBox="0 0 480 190" width="480">
  <rect class="box" x="170" y="14" width="140" height="38" rx="2"/><text class="lbl" x="240" y="30" text-anchor="middle">SW1 ROOT</text><text class="sm" x="240" y="44" text-anchor="middle">32769 . 0000.0000.0001</text>
  <rect class="box" x="20" y="130" width="140" height="38" rx="2"/><text class="lbl" x="90" y="146" text-anchor="middle">SW2</text><text class="sm" x="90" y="160" text-anchor="middle">32769 . 0000.0000.0002</text>
  <rect class="box" x="320" y="130" width="140" height="38" rx="2"/><text class="lbl" x="390" y="146" text-anchor="middle">SW3</text><text class="sm" x="390" y="160" text-anchor="middle">32769 . 0000.0000.0003</text>
  <line class="ln" x1="190" y1="52" x2="95" y2="130"/><text class="sm" x="125" y="84" text-anchor="end">cost 4</text>
  <line class="ln" x1="290" y1="52" x2="385" y2="130"/><text class="sm" x="355" y="84">cost 4</text>
  <line class="ln" x1="160" y1="149" x2="320" y2="149"/><text class="sm" x="240" y="143" text-anchor="middle">cost 4</text>
  <circle class="box" cx="182" cy="62" r="7"/><text class="sm" x="182" y="65" text-anchor="middle">D</text>
  <circle class="box" cx="298" cy="62" r="7"/><text class="sm" x="298" y="65" text-anchor="middle">D</text>
  <circle class="box" cx="108" cy="119" r="7"/><text class="sm" x="108" y="122" text-anchor="middle">R</text>
  <circle class="box" cx="372" cy="119" r="7"/><text class="sm" x="372" y="122" text-anchor="middle">R</text>
  <circle class="box" cx="172" cy="149" r="7"/><text class="sm" x="172" y="152" text-anchor="middle">D</text>
  <circle class="hl" cx="308" cy="149" r="8"/><path class="acc" d="M302,143 L314,155 M314,143 L302,155"/>
  <text class="sm" x="308" y="176" text-anchor="middle">alternate (blocking)</text>
</svg>
<figcaption><b>Figure 4.5</b> Part 1 of the election. R = root port, D = designated port, cross = blocked. Every port on the root is designated; SW3 blocks because SW2 has the lower BID.</figcaption>
</figure>

::: trap
*Claim:* a root port is on the root switch and a designated port is the one that forwards toward it. *Why it is wrong:* the root bridge has no root port; the root port is on the *non-root* switch and faces the root. Designated ports are chosen per *segment*, not per switch. *Correct statement:* the root has only designated ports; each non-root switch has exactly one root port.
:::

::: example
**Load sharing with PVST+.** The Campus Net triangle carries VLANs 10 and 20. Rather than let one tree decide, the designer makes SW2 root for VLAN 10 (`spanning-tree vlan 10 priority 4096`, BID 4106) and SW3 root for VLAN 20 (`spanning-tree vlan 20 priority 4096`, BID 4116). All links remain cost 4.

1. VLAN 10: root SW2. SW1 and SW3 use their direct links to SW2 as root ports. On the SW1-SW3 segment both offer cost 4; SW1's BID (32778, 0001) is lower than SW3's (32778, 0003), so SW1's port is designated and **SW3's port blocks**.
2. VLAN 20: root SW3. SW1 and SW2 use their links to SW3. On the SW1-SW2 segment SW1's BID is lower, so SW1 is designated and **SW2's port blocks**.
3. Result per link: SW1-SW2 forwards VLAN 10 and blocks VLAN 20 at SW2; SW1-SW3 forwards VLAN 20 and blocks VLAN 10 at SW3; SW2-SW3 forwards both.

```
SW3# show spanning-tree vlan 10 | include Gi0/1
Gi0/1   Altn BLK 4  128.1  P2p      <-- blocked for VLAN 10 only
SW3# show spanning-tree vlan 20 | include Gi0/1
Gi0/1   Desg FWD 4  128.1  P2p      <-- forwards VLAN 20
```

[Result: every link carries traffic for at least one VLAN, which a single tree cannot do. The price is two trees to reason about, so the root of each VLAN should be aligned with the first-hop gateway of that VLAN.]{.result}
:::

*Convergence.* In 802.1D a port moves Blocking → Listening (15 s) → Learning (15 s) → Forwarding, and a topology change is detected only after the *max-age* timer (20 s) expires, so recovery takes up to 50 seconds. *Rapid STP* (802.1w) removes the timers. Its ports have three states (discarding, learning, forwarding) and four roles: root, designated, *alternate* (a backup path to the root through another switch) and *backup* (a second port on the same segment). When a link fails, the alternate port becomes the root port at once. On a new point-to-point link a *proposal/agreement* handshake lets a designated port go to forwarding after its neighbour blocks its other non-edge ports (the "sync"), which takes a fraction of a second. A neighbour is declared dead after three missed hellos (6 s), not after max-age. An *edge port* (PortFast) goes straight to forwarding because it faces an end host.

<figure>
<svg viewBox="0 0 480 100" width="480">
  <text class="sm" x="10" y="12">802.1D: up to 50 s</text>
  <rect class="fill" x="10" y="18" width="160" height="22"/><text class="lbl" x="90" y="33" text-anchor="middle">Blocking 20 s (max age)</text>
  <rect class="fill" x="170" y="18" width="120" height="22"/><text class="lbl" x="230" y="33" text-anchor="middle">Listening 15 s</text>
  <rect class="fill" x="290" y="18" width="120" height="22"/><text class="lbl" x="350" y="33" text-anchor="middle">Learning 15 s</text>
  <rect class="hl" x="410" y="18" width="60" height="22"/><text class="lbl" x="440" y="33" text-anchor="middle">Forwarding</text>
  <text class="sm" x="10" y="62">Rapid STP: sub-second on point-to-point links</text>
  <rect class="fill" x="10" y="68" width="14" height="22"/><rect class="hl" x="24" y="68" width="446" height="22"/>
  <text class="lbl" x="250" y="83" text-anchor="middle">proposal, agreement, forwarding; discarding is brief</text>
</svg>
<figcaption><b>Figure 4.6</b> Convergence after a link failure, drawn to scale.</figcaption>
</figure>

| | 802.1D | Rapid STP (802.1w) | PVST+ / Rapid PVST+ | MST (802.1s) |
|---|---|---|---|---|
| Trees | one for all VLANs (CST) | one for all VLANs | one per VLAN | one per *instance*, each carrying many VLANs |
| Convergence | up to 50 s | under a second | 802.1D / 802.1w speed | 802.1w speed |
| Load sharing | none | none | by choosing a different root per VLAN | by mapping VLANs to instances |
| CPU and BPDU load | low | low | grows with VLAN count | low, scales to thousands of VLANs |

MST groups VLANs into instances, so that 1000 VLANs can share two trees. Switches belong to the same *region* only if their region name, revision number and VLAN-to-instance mapping all match. On Cisco, `spanning-tree mode rapid-pvst` is the usual choice for a campus with up to a few hundred VLANs.

<figure>
<svg viewBox="0 0 480 190" width="480">
  <rect class="box" x="180" y="10" width="120" height="26" rx="2"/><text class="lbl" x="240" y="27" text-anchor="middle">Core</text>
  <rect class="box" x="60" y="80" width="130" height="26" rx="2"/><text class="lbl" x="125" y="97" text-anchor="middle">Distribution 1 (root)</text>
  <rect class="box" x="290" y="80" width="130" height="26" rx="2"/><text class="lbl" x="355" y="97" text-anchor="middle">Distribution 2 (backup root)</text>
  <rect class="box" x="60" y="150" width="130" height="26" rx="2"/><text class="lbl" x="125" y="167" text-anchor="middle">Access switch</text>
  <rect class="box" x="290" y="150" width="130" height="26" rx="2"/><text class="lbl" x="355" y="167" text-anchor="middle">Access switch</text>
  <line class="lg" x1="210" y1="36" x2="125" y2="80"/><line class="lg" x1="270" y1="36" x2="355" y2="80"/><line class="lg" x1="190" y1="93" x2="290" y2="93"/>
  <line class="lg" x1="110" y1="106" x2="110" y2="150"/><line class="lg" x1="140" y1="106" x2="300" y2="150"/><line class="lg" x1="340" y1="106" x2="340" y2="150"/><line class="lg" x1="370" y1="106" x2="170" y2="150"/>
  <text class="sm" x="116" y="128" text-anchor="end">Root Guard</text><text class="sm" x="350" y="128" text-anchor="end">Root Guard</text>
  <text class="sm" x="238" y="132">Loop Guard on uplinks</text><text class="sm" x="238" y="142">that may be blocked</text>
  <text class="sm" x="10" y="186">PortFast and BPDU Guard on every host-facing port</text>
  <path class="acc" d="M62,170 L40,170 L40,184 L8,184"/>
</svg>
<figcaption><b>Figure 4.6b</b> Where the guard features go in a campus: Root Guard downward from the distribution layer, Loop Guard on access uplinks, PortFast with BPDU Guard on edge ports.</figcaption>
</figure>

Several safeguards complete the design. **PortFast** with **BPDU Guard** goes on access ports: PortFast skips the wait, and BPDU Guard puts the port in err-disabled state if a BPDU arrives, which stops a rogue switch. **Root Guard** goes on distribution downlinks to keep access switches from becoming root; a port that hears a superior BPDU moves to root-inconsistent. **Loop Guard** goes on non-designated uplinks, so that a port that suddenly stops receiving BPDUs (a unidirectional link) does not start forwarding. **UDLD** detects the unidirectional fibre itself.

```
spanning-tree mode rapid-pvst
spanning-tree vlan 1,10,20 priority 4096      ! root (use "root primary" to compute it)
spanning-tree portfast default                ! all access ports become edge ports
spanning-tree portfast bpduguard default
interface GigabitEthernet0/48                 ! distribution downlink
 spanning-tree guard root
interface GigabitEthernet0/1                  ! access uplink
 spanning-tree guard loop
```

```
SW3# show spanning-tree vlan 1
VLAN0001
  Spanning tree enabled protocol rstp
  Root ID    Priority    32769
             Address     0000.0000.0001
             Cost        4
             Port        1 (GigabitEthernet0/1)   <-- root port
Interface        Role Sts Cost      Prio.Nbr Type
Gi0/1            Root FWD 4         128.1    P2p
Gi0/2            Altn BLK 4         128.2    P2p   <-- alternate
```

<figure>
<svg viewBox="0 0 480 130" width="480">
  <defs><marker id="r43" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#1A1D23"/></marker></defs>
  <rect class="box" x="30" y="20" width="90" height="30" rx="2"/><text class="lbl" x="75" y="39" text-anchor="middle">Root / upstream</text>
  <rect class="box" x="360" y="20" width="90" height="30" rx="2"/><text class="lbl" x="405" y="39" text-anchor="middle">New switch</text>
  <line class="ln" x1="120" y1="28" x2="360" y2="28" marker-end="url(#r43)"/><text class="sm" x="240" y="22" text-anchor="middle">1 Proposal: I am designated here</text>
  <text class="sm" x="240" y="58" text-anchor="middle">2 New switch syncs: blocks its other non-edge ports</text>
  <line class="ln" x1="360" y1="70" x2="120" y2="70" marker-end="url(#r43)"/><text class="sm" x="240" y="84" text-anchor="middle">3 Agreement: my root port is this one</text>
  <rect class="hl" x="30" y="94" width="90" height="22" rx="2"/><text class="sm" x="75" y="108" text-anchor="middle">forwards at once</text>
  <text class="sm" x="170" y="108">Each hop repeats the handshake, so the wave crosses a campus in milliseconds.</text>
</svg>
<figcaption><b>Figure 4.6c</b> The Rapid STP proposal and agreement handshake on a point-to-point link.</figcaption>
</figure>

*EtherChannel* bundles up to eight parallel links into one logical port-channel, which spanning tree treats as one link, so that no member is blocked and the bandwidth adds. Members must match in speed, duplex, VLAN list and trunk mode. Negotiation is by LACP (IEEE 802.1AX, modes `active` and `passive`), by Cisco's PAgP (`desirable`, `auto`) or statically with `on`. A bundle forms when at least one end initiates and both use the same protocol; `on` never negotiates, so it pairs only with `on`.

MST needs the instance map to be identical across the region. The mapping is configured once, and unmapped VLANs fall into instance 0 (the *internal spanning tree*, which also represents the region to the outside):

```
spanning-tree mode mst
spanning-tree mst configuration
 name CAMPUS
 revision 1
 instance 1 vlan 10,30
 instance 2 vlan 20,40
spanning-tree mst 1 priority 4096
spanning-tree mst 2 priority 8192
```

| | active | passive | desirable | auto | on |
|---|---|---|---|---|---|
| **active** | yes | yes | no | no | no |
| **passive** | yes | no | no | no | no |
| **desirable** | no | no | yes | yes | no |
| **auto** | no | no | yes | no | no |
| **on** | no | no | no | no | yes |

```
SW1(config)# interface range GigabitEthernet0/1-2
SW1(config-if-range)# channel-group 1 mode active
SW1# show etherchannel summary
Group  Port-channel  Protocol    Ports
1      Po1(SU)       LACP        Gi0/1(P)  Gi0/2(P)
```

The flags read: S = Layer 2, U = in use; P = bundled in the channel; `s` = suspended (the member's settings disagree), D = down. Traffic is spread over members by a hash of header fields (`port-channel load-balance src-dst-ip`), so one flow always uses one member, and a single flow never exceeds one link's speed. Multi-chassis versions (vPC, MLAG) that terminate a bundle on two switches are taught in [§5.3](#s5-3){.ref}.

A bundle is also a design tool: because the channel is one logical port, spanning tree sees one link and keeps it forwarding, and the bundle survives the failure of a member with no topology change. A *Layer 3 EtherChannel* (`no switchport` on the port-channel, then an IP address) carries routed traffic between switches without VLANs. Typical causes of a bundle that does not form or suspends members are tabulated.

| Symptom in `show etherchannel summary` | Likely cause | Check |
|---|---|---|
| Members `(s)` | member settings differ from the bundle | `show run interface`, speed, duplex, trunk list |
| Members `(I)` stand-alone | partner is not running the same protocol, or silent | `show lacp neighbor`, partner mode |
| Port-channel `(SD)` | all members down | cabling, partner shutdown |
| Bundle up, one link saturated | hash puts many flows on one member | `port-channel load-balance`, `show etherchannel load-balance` |
| MAC flapping across members | one side `on`, other LACP | make both LACP |

```
SW1(config)# port-channel load-balance src-dst-ip
SW1# test etherchannel load-balance interface Po1 ip 192.168.10.5 10.0.0.80
Would select Gi0/2 of Po1
```

::: lens
[CISCO · JUNIPER · ARISTA]{.co}

STP is the most reliably asked Layer 2 topic. Expect a triangle or a square, and the request to name the root, root ports, designated ports and the blocked port. Show the four-step order aloud, because the examiner is checking the method more than the answer. Follow-ups: why 4096, why RSTP is fast, where each guard goes, and a "network freezes, MACs flap" scenario (a loop, found with `show spanning-tree` and the interface counters).
:::

::: lab
`LAB 4.3 · 20 MIN`  Build the triangle, then fail the root port.

```
SW3(config)# spanning-tree mode rapid-pvst
SW3(config)# spanning-tree vlan 1 priority 4096
SW2(config)# interface GigabitEthernet0/1
SW2(config-if)# shutdown
```

```
SW3# show spanning-tree vlan 1 | include Root
  This bridge is the root
```

**What you should notice:** `show spanning-tree` on SW1 and SW2 now names SW3 as root. With the default 802.1D mode the alternate port takes 30 to 50 s to forward; with `rapid-pvst` pings recover in about a second. To see a storm, disable spanning tree on all three switches (`no spanning-tree vlan 1`) in simulation only.
:::

::: check
1. Why does the root bridge never have a root port? [^c4-3]
2. SW2's two links to the root carry cost 4 each. Which port blocks? [^c4-4]
:::

[^c4-3]: The root port is the best path *toward* the root; the root is already there.
[^c4-4]: The one connected to the root's higher sender port ID (for example 128.2 rather than 128.1).

:::
