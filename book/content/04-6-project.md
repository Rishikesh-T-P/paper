::: {.p4}

## [4.15]{.sec}Mini-project: Campus-to-Internet [Optional · ■■■]{.tag} {#s4-15}

::: bigidea
A dual-homed enterprise built and verified as code shows every protocol of this chapter working together, and a test suite makes the result repeatable evidence of competence.
:::

**Topology (Containerlab; FRR plus Arista cEOS or Nokia SR Linux).** Campus Net has two access switches (VLANs 10, 20 and a voice VLAN 99) with an LACP uplink to a collapsed-core pair running HSRP or VRRP, with the spanning-tree root aligned to the active gateway. A multi-area OSPF network has area 0 in the core and area 10 for a branch (totally stubby). Two border routers, BR1 and BR2, run eBGP to ISP-A (AS 100) and ISP-B (AS 200), which both peer with a content AS 300, and iBGP between themselves with `next-hop-self`.

**Policy requirements.**

- ISP-A is primary in both directions: local preference 200 inbound to Campus Net, AS-path prepend twice towards ISP-B.
- Advertise only 198.51.100.0/24, using a prefix list and `maximum-prefix`.
- Tag customer routes with communities and filter by community.
- PAT at the borders, LLQ for voice on the WAN, and a GRE tunnel to a branch carrying OSPF.

**Deliverables.**

1. A design document: the IP plan using VLSM (method in [§3.4](#s3-4){.ref}) and a diagram in the style of this book.
2. `topology.clab.yml` and the start-up configurations.
3. A `verify.py` test suite (pytest) that asserts OSPF neighbours are Full, BGP sessions are Established, the best path is via ISP-A, traffic fails over to ISP-B within *N* seconds when the ISP-A link is cut, and DSCP EF is preserved end to end ([Pillar 10](#ch10){.ref} shows the Netmiko and `vtysh` calls).
4. A failure-injection runbook with five faults, each with symptom, diagnosis and fix, which feeds the troubleshooting method of [Pillar 11](#ch11){.ref}.
5. A two-minute explanation of the project, and two résumé bullets.

**Milestones.** Week 1: L2 and the gateways. Week 2: OSPF and the branch. Week 3: BGP and the policy. Week 4: QoS, GRE, tests, runbook. **Stretch.** Replace the GRE tunnel by an MPLS L3VPN provider core, enable BFD, and measure the convergence improvement.

```python
def test_best_path_via_isp_a(bgp):               # pytest fixture runs vtysh on BR1
    best = bgp.best("203.0.113.0/24")
    assert best.as_path[0] == 100 and best.localpref == 200

def test_failover(lab, bgp):
    lab.link_down("br1-isp-a")
    assert bgp.wait_best("203.0.113.0/24", via_as=200, timeout=15)
```

:::
