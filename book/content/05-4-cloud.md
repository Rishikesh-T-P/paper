::: {.p5}

## [5.11]{.sec}AWS: the Virtual Private Cloud [Must · ■■□]{.tag} {#s5-11}

::: bigidea
A VPC is a private network that the provider simulates in software, scoped to one region, in which routing is explicit (route tables decide what is public) and filtering is done at two levels, a stateful security group at each interface and a stateless network ACL at each subnet.
:::

The fabric of the preceding sections is invisible to a cloud customer; what the customer sees is a virtual network that behaves like the campus network of Pillar 4. In Amazon Web Services this is the *Virtual Private Cloud* (VPC). A VPC is created in one region with an address block between /16 and /28, for example 10.0.0.0/16. It is divided into *subnets*, and each subnet lives in exactly one *availability zone* (AZ), a physically separate data-centre group within the region, so that high availability means placing one subnet in each of two or more AZs. Within the VPC every subnet can reach every other through an implicit router; the *route table* attached to a subnet decides where all other traffic goes. A VPC has a ready-made route "local" for its own block and nothing else; every other route is added by the customer.

A subnet is *public* if its route table contains a default route (0.0.0.0/0) to an *internet gateway* (IGW), a horizontally scaled, redundant gateway that translates between private addresses and public ones. It is *private* if the default route instead points to a *NAT gateway*, which sits in a public subnet and lets instances start outbound connections while blocking unsolicited inbound ones ([§3.6](#s3-6){.ref}), or if there is no default route at all. Being public also requires the instance to hold a public or Elastic IP address; the route alone is not enough. Note that AWS reserves five addresses in every subnet: the network address (.0), the VPC router (.1), the DNS resolver (.2), one held for future use (.3) and the broadcast address (the last), so a /24 offers 251 usable addresses, not 254.

::: example
**A three-tier web application across two AZs.** The VPC is 10.0.0.0/16 (Figure 5.16).

1. Subnets: public 10.0.1.0/24 (AZ a) and 10.0.2.0/24 (AZ b); private application 10.0.11.0/24 and 10.0.12.0/24; database 10.0.21.0/24 and 10.0.22.0/24. Each has 256 − 5 = 251 usable addresses.
2. Route tables: *public* has 10.0.0.0/16 local and 0.0.0.0/0 to the IGW. Each *application* table has 10.0.0.0/16 local and 0.0.0.0/0 to the NAT gateway in the same AZ (a gateway in a single AZ would be a shared failure point). The *database* table has only the local route, so the database cannot reach the Internet at all.
3. Security groups: ALB-SG allows TCP 443 from 0.0.0.0/0. App-SG allows TCP 8080 *from ALB-SG* (a rule that names a group, not an address range, so it follows instances as they scale). DB-SG allows TCP 5432 from App-SG. No other inbound rule exists.
4. Network ACL on the public subnets: inbound allow TCP 443 from 0.0.0.0/0; outbound allow TCP 1024 to 65535 to 0.0.0.0/0. The outbound rule is the *ephemeral-port* rule: the client's source port is chosen from a high range, and since a network ACL remembers nothing, the reply must be explicitly allowed. Omitting it makes an otherwise correct design hang.
5. Return traffic through the security groups needs no rule, because they are stateful.

[Result: only the load balancer is exposed; each tier admits only the tier above it; the database has no route out.]{.result}
:::

<figure>
<svg viewBox="0 0 480 258" width="480"><defs></defs><rect class="lg dash" x="4" y="4" width="472" height="248" rx="6"/><text class="sm" x="14" y="16" text-anchor="start">Region (for example ap-south-1)</text><rect class="box" x="10" y="34" width="322" height="212" rx="3"/><text class="lbl" x="18" y="46" text-anchor="start">VPC 10.0.0.0/16</text><rect class="box" x="124" y="22" width="64" height="18" rx="0"/><text class="lbl" x="156" y="34" text-anchor="middle">IGW</text><line class="ln" x1="156" y1="40" x2="156" y2="64"/><text class="sm" x="90" y="60" text-anchor="middle">AZ a</text><rect class="fill" x="18" y="66" width="148" height="60" rx="2"/><text class="sm" x="22" y="76" text-anchor="start">public 10.0.1.0/24</text><rect class="box" x="28" y="98" width="52" height="20" rx="0"/><text class="sm" x="54" y="111" text-anchor="middle">NAT GW</text><rect class="fill" x="18" y="132" width="148" height="48" rx="2"/><text class="sm" x="22" y="142" text-anchor="start">private app 10.0.11.0/24</text><rect class="box" x="28" y="150" width="52" height="22" rx="0"/><text class="lbl" x="54" y="164" text-anchor="middle">EC2</text><rect class="fill" x="18" y="186" width="148" height="52" rx="2"/><text class="sm" x="22" y="196" text-anchor="start">private db 10.0.21.0/24</text><rect class="box" x="28" y="206" width="52" height="22" rx="0"/><text class="lbl" x="54" y="220" text-anchor="middle">RDS</text><line class="lg" x1="54" y1="118" x2="54" y2="150"/><text class="sm" x="246" y="60" text-anchor="middle">AZ b</text><rect class="fill" x="174" y="66" width="148" height="60" rx="2"/><text class="sm" x="178" y="76" text-anchor="start">public 10.0.2.0/24</text><rect class="box" x="184" y="98" width="52" height="20" rx="0"/><text class="sm" x="210" y="111" text-anchor="middle">NAT GW</text><rect class="fill" x="174" y="132" width="148" height="48" rx="2"/><text class="sm" x="178" y="142" text-anchor="start">private app 10.0.12.0/24</text><rect class="box" x="184" y="150" width="52" height="22" rx="0"/><text class="lbl" x="210" y="164" text-anchor="middle">EC2</text><rect class="fill" x="174" y="186" width="148" height="52" rx="2"/><text class="sm" x="178" y="196" text-anchor="start">private db 10.0.22.0/24</text><rect class="box" x="184" y="206" width="52" height="22" rx="0"/><text class="lbl" x="210" y="220" text-anchor="middle">RDS</text><line class="lg" x1="210" y1="118" x2="210" y2="150"/><rect class="box" x="20" y="80" width="296" height="14" rx="2"/><text class="sm" x="168" y="90" text-anchor="middle">Application Load Balancer (spans both public subnets)</text><path class="acc" d="M156,64 L156,80"/><text class="lbl" x="342" y="44" text-anchor="start">Public route table</text><text class="mono" x="342" y="55" text-anchor="start">10.0.0.0/16  local</text><text class="mono" x="342" y="65" text-anchor="start">0.0.0.0/0  igw-…</text><text class="lbl" x="342" y="96" text-anchor="start">App route table (per AZ)</text><text class="mono" x="342" y="107" text-anchor="start">10.0.0.0/16  local</text><text class="mono" x="342" y="117" text-anchor="start">0.0.0.0/0  nat-… (same AZ)</text><text class="lbl" x="342" y="148" text-anchor="start">Database route table</text><text class="mono" x="342" y="159" text-anchor="start">10.0.0.0/16  local</text></svg>
<figcaption><b>Figure 5.16</b> The three-tier VPC of the worked example. A subnet is public only because its route table points at the internet gateway; the private subnets reach the internet through the NAT gateway in their own AZ.</figcaption>
</figure>

| | Security group | Network ACL |
|---|---|---|
| Attached to | network interface (ENI) | subnet |
| State | stateful: replies allowed automatically | stateless: both directions need rules |
| Rule types | allow only | allow and deny |
| Evaluation | all rules together, no order | by rule number, lowest first, first match wins; final deny |
| Default | deny inbound, allow outbound | default ACL allows all; a new custom ACL denies all |
| Can reference | other security groups | address ranges only |

Connecting VPCs is the next question. *VPC peering* joins two VPCs with a private link; it needs non-overlapping address blocks and a route in each VPC's tables. Peering is *not transitive*: if A peers with B and B with C, then A cannot reach C through B, and neither can A use B's internet gateway or VPN. Connecting n VPCs in a full mesh needs n(n − 1)/2 peerings: for 50 VPCs that is 1,225. A *transit gateway* (TGW) is a regional hub-and-spoke router: each VPC, VPN and Direct Connect (§5.13) is an *attachment*, and TGW route tables, with *association* and *propagation*, decide which attachment can reach which, so 50 VPCs need 50 attachments and segmentation is expressed in the route tables. *PrivateLink* exposes one *service* (behind a network load balancer) to another VPC through an *interface endpoint*, a network interface with a private address in the consumer's subnet. It is one-way and works even when the address blocks overlap. *Gateway endpoints* reach S3 and DynamoDB through a route-table entry rather than the Internet.

AWS builds these networks by host-based software: the Nitro cards of each server encapsulate packets in a VPC-aware tunnel, apply security groups and answer ARP requests from a mapping service, which is why a VPC has no broadcast and why the underlying switches stay a plain routed fabric (§5.5). *VPC Flow Logs* record accepted and rejected connections per interface and are the first tool for the diagnoses of [Pillar 11](#ch11){.ref}.

::: lab
`LAB 5.11 · 3 H`  An AWS free-tier account, console or CLI. Create a VPC 10.0.0.0/16 with a public and a private subnet, an IGW, a bastion in the public subnet and an instance in the private subnet, and enable Flow Logs. Then add a network ACL to the public subnet that allows inbound TCP 22 but no outbound ephemeral ports.

```
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 create-route --route-table-id rtb-... --destination-cidr-block 0.0.0.0/0 --gateway-id igw-...
ssh -o ConnectTimeout=5 ec2-user@<bastion-public-ip>
```

**What you should notice:** with the ephemeral rule missing, SSH hangs at the connect stage while the security group looks correct; Flow Logs show an ACCEPT for the inbound packet and no reply, because the NACL silently drops the response. Adding outbound TCP 1024 to 65535 repairs it. **Cost:** a NAT gateway is billed hourly, so use a NAT instance or skip it, and delete everything afterwards.
:::

::: trap
*Claim:* "VPC peering is transitive, and I can add a deny to a security group." *Why it is wrong:* peering joins exactly two VPCs, and security groups contain only allow rules. *Correct statement:* use a transit gateway for many VPCs, a network ACL for an explicit deny, and remember that peered VPCs cannot have overlapping blocks.
:::

::: lens
[AMAZON · MICROSOFT · GOOGLE]{.co}

Amazon's network development engineer loops ask "security group versus network ACL" and the scenario "an instance in a private subnet cannot reach the Internet; list the checks in order" (route table, NAT gateway state and placement, the NAT's own route to the IGW, outbound rules, DNS, then the instance's own firewall). Start from the route and finish at the host.
:::

::: check
1. Why does a /24 subnet in AWS have 251 usable addresses? [^c511-1]
2. Which of the two filters needs an ephemeral-port rule, and why? [^c511-2]
3. How many peerings does a full mesh of 10 VPCs need? [^c511-3]
:::

[^c511-1]: Five addresses are reserved: network, router, DNS, future use and broadcast.
[^c511-2]: The network ACL, because it is stateless and the reply goes to a high source port.
[^c511-3]: 10 × 9 ÷ 2 = 45.

## [5.12]{.sec}Azure: the virtual network [Should · ■■□]{.tag} {#s5-12}

::: bigidea
An Azure virtual network offers the same building blocks as a VPC with different edges: subnets span all zones, one filter (the network security group) is stateful and prioritised, and user-defined routes let the customer force traffic through a firewall.
:::

A *virtual network* (VNet) in Azure is scoped to a region, and, unlike a VPC subnet, a subnet is **not** tied to an availability zone; the resources placed in it choose their zones. Azure reserves five addresses per subnet: the network address, the default gateway (.1), two for Azure DNS (.2 and .3) and the broadcast address. Filtering is done by a *network security group* (NSG), a list of rules that may be attached to a subnet, to a network interface, or to both. An NSG is stateful, so unlike an AWS network ACL it needs no return rule, and it has both allow and deny rules. Each rule has a *priority* from 100 to 4096, and the rules are evaluated from the lowest number upward until one matches, after which evaluation stops. The default rules, with priorities 65000 and above, allow traffic inside the VNet and from the load balancer and deny other inbound traffic. *Application security groups* name sets of interfaces so that rules can refer to roles, and *service tags* name Microsoft-managed address sets such as Storage or AzureCloud.

Routing begins with *system routes*: the VNet's own prefix, peered prefixes and a default route to the Internet. A *user-defined route* (UDR) in a route table overrides them, for instance to send 0.0.0.0/0 to a firewall; a *next hop type* of `VirtualAppliance` names the firewall's private address. When several routes share a prefix, a UDR wins over a BGP route, which wins over a system route; as always, the longest prefix is considered before any of this ([§4.4](#s4-4){.ref}). Where a network virtual appliance (NVA) must learn the VNet's routes and announce its own, the *Azure Route Server* peers with it over BGP (the server uses AS 65515) and injects the learned routes into the VNet, so the UDRs need not be maintained by hand.

::: example
**A hub-and-spoke network.** The hub VNet is 10.100.0.0/16 with `AzureFirewallSubnet` 10.100.1.0/26 (the firewall takes 10.100.1.4) and `GatewaySubnet` 10.100.255.0/27. Two spokes are 10.1.0.0/16 and 10.2.0.0/16 (Figure 5.17).

1. Peering is not transitive, so each spoke is peered with the hub only. Spoke 1 therefore has system routes for 10.1.0.0/16 and 10.100.0.0/16 but none for 10.2.0.0/16.
2. A UDR on every spoke subnet sends 0.0.0.0/0 with next hop `VirtualAppliance` 10.100.1.4.
3. A packet from 10.1.0.5 to 10.2.0.7 matches no system route for 10.2.0.0/16, so it takes the default route, reaches the firewall, which checks its rules and forwards it over the hub-to-spoke-2 peering. Spoke 2 must accept it on the peering link, which needs *Allow forwarded traffic* because the packet did not originate in the hub.
4. The hub's gateway is shared with the spokes by two peering settings: *Allow gateway transit* on the hub side and *Use remote gateway* on each spoke side. Then Campus Net's on-premises network (§5.13) reaches the spokes through the one gateway.
5. For the return traffic the spoke 2 UDR forces the reply through the firewall as well, so the path is symmetric and the stateful firewall sees both directions.

[Result: all spoke-to-spoke and spoke-to-Internet traffic crosses the firewall, because of one default route per spoke.]{.result}
:::

<figure>
<svg viewBox="0 0 480 214" width="480"><defs><marker id="a517" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accf"/></marker></defs><rect class="lg dash" x="160" y="50" width="160" height="150" rx="4"/><text class="lbl" x="240" y="63" text-anchor="middle">Hub VNet 10.100.0.0/16</text><rect class="box" x="176" y="74" width="128" height="30" rx="0"/><text class="lbl" x="240" y="87" text-anchor="middle">AzureFirewallSubnet</text><text class="sm" x="240" y="98" text-anchor="middle">firewall 10.100.1.4</text><rect class="box" x="176" y="118" width="128" height="30" rx="0"/><text class="lbl" x="240" y="131" text-anchor="middle">GatewaySubnet</text><text class="sm" x="240" y="142" text-anchor="middle">VPN / ExpressRoute gateway</text><rect class="box" x="176" y="162" width="128" height="28" rx="0"/><text class="lbl" x="240" y="175" text-anchor="middle">RouteServerSubnet</text><text class="sm" x="240" y="185" text-anchor="middle">BGP with NVAs</text><rect class="box" x="10" y="86" width="110" height="70" rx="4"/><text class="lbl" x="65" y="100" text-anchor="middle">Spoke 1</text><text class="sm" x="65" y="111" text-anchor="middle">10.1.0.0/16</text><text class="sm" x="65" y="133" text-anchor="middle">UDR 0.0.0.0/0</text><text class="sm" x="65" y="143" text-anchor="middle">→ 10.100.1.4</text><rect class="box" x="360" y="86" width="110" height="70" rx="4"/><text class="lbl" x="415" y="100" text-anchor="middle">Spoke 2</text><text class="sm" x="415" y="111" text-anchor="middle">10.2.0.0/16</text><text class="sm" x="415" y="133" text-anchor="middle">UDR 0.0.0.0/0</text><text class="sm" x="415" y="143" text-anchor="middle">→ 10.100.1.4</text><line class="ln" x1="120" y1="121" x2="160" y2="121"/><line class="ln" x1="320" y1="121" x2="360" y2="121"/><text class="sm" x="140" y="115" text-anchor="middle">peering</text><text class="sm" x="340" y="115" text-anchor="middle">peering</text><path class="acc" d="M120,100 L176,92 M304,92 L360,100" marker-end="url(#a517)"/><rect class="box" x="190" y="6" width="100" height="24" rx="10"/><text class="lbl" x="240" y="22" text-anchor="middle">Campus Net on-premises</text><line class="lg dash" x1="240" y1="30" x2="240" y2="118" style="stroke-dasharray:2 2"/><text class="sm" x="246" y="42" text-anchor="start">ExpressRoute / VPN</text></svg>
<figcaption><b>Figure 5.17</b> Hub and spoke. The hub holds the shared services; the spokes peer only with the hub, so spoke-to-spoke traffic (accent) is forced through the firewall by the default route in each spoke.</figcaption>
</figure>

The differences from AWS are what interviews test, and the term-by-term mapping is given in the Revision Spread. The behavioural ones are these.

| Question | AWS | Azure |
|---|---|---|
| Subnet scope | one AZ | whole region (all zones) |
| Stateless filter at the subnet | network ACL | none (an NSG is stateful) |
| Rule order | NACL by number; SG unordered | NSG by priority, lowest first |
| Default internet access | none until IGW and route | outbound by default for most resources (being retired in favour of explicit NAT) |
| Transitivity hub | transit gateway | Virtual WAN hub or hub VNet with firewall and UDRs |
| Fast NIC path | Nitro / ENA | Accelerated Networking (SR-IOV, FPGA SmartNIC) |

Two cautions. *Accelerated Networking* lets the virtual machine's NIC bypass the host's virtual switch for the data path, so the policy that the vSwitch would apply is offloaded to hardware: the same idea as the ASIC pipeline of §5.8. And SNAT port exhaustion (§5.9) appears in Azure when many instances share the outbound address of a load balancer; the cures are more addresses, a NAT gateway, or connection reuse.

::: trap
*Claim:* "NSG rules are checked in the order they were created, like an access list." *Why it is wrong:* they are ordered by priority number, and the lowest number wins; the creation order is irrelevant. *Correct statement:* give specific rules low numbers (100 to 200) and broad rules high ones, leaving gaps for later insertion.
:::

::: check
1. Which Azure object plays the role of the AWS route table's "next hop to a firewall"? [^c512-1]
2. Why must a spoke be peered with the hub and not with other spokes in hub-and-spoke? [^c512-2]
3. What does the lowest priority number mean in an NSG? [^c512-3]
:::

[^c512-1]: A user-defined route with next hop type VirtualAppliance.
[^c512-2]: To force inspection: there is no system route to another spoke, so traffic falls to the default route and the firewall. Peering is also non-transitive.
[^c512-3]: The highest precedence; it is evaluated first and a match stops evaluation.

## [5.13]{.sec}Hybrid connectivity: Direct Connect, ExpressRoute and VPN [Should · ■■□]{.tag} {#s5-13}

::: bigidea
A private circuit to the cloud is an ordinary BGP interconnection, so its availability and path preference are decided by the redundancy you buy and the attributes you set, and an IPsec VPN over the Internet is the cheaper path or the backup.
:::

Campus Net's cloud networks must be reached from its own routers. There are two families of path. A *private circuit*, AWS Direct Connect (DX) or Azure ExpressRoute, is a layer-2 or layer-3 link rented through a carrier from the customer's site or a colocation facility to the provider's edge; it bypasses the public Internet, so it has predictable latency and no Internet exposure, and it is billed by port and traffic. An *IPsec VPN* ([§9.7](#s9-7){.ref}) is an encrypted tunnel over the Internet, quick to set up and cheap but with variable latency and bandwidth. Routing on both is BGP ([§4.7](#s4-7){.ref}), so everything in Pillar 4 about preference, prepending and communities applies.

*ExpressRoute* terminates on a pair of Microsoft routers (MSEE) in a peering location. A circuit has a *primary* and a *secondary* link, each a BGP session over its own /30. Two *peerings* are used: *private peering* reaches VNets with private addresses; *Microsoft peering* reaches Microsoft 365 and Azure public services, and requires public addresses. Microsoft's AS number is 12076. *Direct Connect* offers *virtual interfaces* (VIFs): a *private VIF* reaches a VPC through a virtual private gateway or a Direct Connect gateway; a *transit VIF* reaches a transit gateway; a *public VIF* reaches AWS public endpoints. A Site-to-Site VPN to AWS has two tunnels per connection, each good for up to 1.25 Gb/s, and is the usual backup.

::: example
**ExpressRoute with two links and a VPN backup.** Campus Net (AS 65010) advertises 172.16.0.0/16 on-premises and connects through CE1 and CE2 to the primary link (192.168.10.0/30) and the secondary link (192.168.10.4/30), Figure 5.18.

1. Both sessions are eBGP between AS 65010 and AS 12076. Azure learns 172.16.0.0/16 twice.
2. *Inbound preference* (Azure to campus) is decided by what Campus Net advertises. CE2 prepends its own AS twice on the secondary, giving AS_PATH 65010 65010 65010 against 65010 on the primary. Azure prefers the shorter path, so return traffic uses the primary and falls to the secondary on failure.
3. *Outbound preference* (campus to Azure) is decided by what Campus Net sets. Azure advertises 10.100.0.0/16 on both sessions with equal attributes; the campus routers set LOCAL_PREF 200 on routes learnt from CE1 and 100 on CE2, so outbound traffic also uses the primary.
4. The VPN backup is configured with the same prefix. If it is advertised with the same attributes, the best path may differ in the two directions and the traffic is asymmetric, which a stateful firewall in the path drops. Make the VPN less preferred in both directions: prepend towards Azure and set a lower LOCAL_PREF on the campus side.
5. Never advertise a *more specific* prefix over the VPN than over ExpressRoute. The longest prefix is chosen before any preference attribute is read ([§4.4](#s4-4){.ref}), so a /24 on the VPN beats a /16 on ExpressRoute and moves the traffic onto the backup.

[Result: primary preferred in both directions by prepending (inbound) and LOCAL_PREF (outbound); the VPN is a last resort with equal-length prefixes.]{.result}
:::

<figure>
<svg viewBox="0 0 480 180" width="480"><defs><marker id="a518" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker></defs><rect class="lg dash" x="6" y="50" width="90" height="100" rx="4"/><text class="lbl" x="51" y="63" text-anchor="middle">Campus Net</text><text class="sm" x="51" y="73" text-anchor="middle">AS 65010</text><rect class="box" x="18" y="82" width="66" height="20" rx="0"/><text class="lbl" x="51" y="96" text-anchor="middle">CE1</text><rect class="box" x="18" y="114" width="66" height="20" rx="0"/><text class="lbl" x="51" y="128" text-anchor="middle">CE2</text><rect class="lg dash" x="124" y="50" width="90" height="100" rx="20"/><text class="sm" x="169" y="100" text-anchor="middle">Connectivity</text><text class="sm" x="169" y="110" text-anchor="middle">provider</text><rect class="lg dash" x="250" y="50" width="100" height="100" rx="4"/><text class="lbl" x="300" y="63" text-anchor="middle">Microsoft edge</text><text class="sm" x="300" y="73" text-anchor="middle">AS 12076</text><rect class="box" x="264" y="82" width="72" height="20" rx="0"/><text class="lbl" x="300" y="96" text-anchor="middle">MSEE-1</text><rect class="box" x="264" y="114" width="72" height="20" rx="0"/><text class="lbl" x="300" y="128" text-anchor="middle">MSEE-2</text><rect class="box" x="380" y="70" width="92" height="60" rx="4"/><text class="lbl" x="426" y="90" text-anchor="middle">VNet gateway</text><text class="sm" x="426" y="102" text-anchor="middle">10.100.0.0/16</text><text class="sm" x="426" y="114" text-anchor="middle">(hub)</text><line class="ln" x1="84" y1="92" x2="264" y2="92"/><line class="acc" x1="84" y1="124" x2="264" y2="124"/><line class="ln" x1="336" y1="92" x2="380" y2="92"/><line class="ln" x1="336" y1="124" x2="380" y2="124"/><text class="sm" x="174" y="86" text-anchor="middle">primary 192.168.10.0/30</text><text class="acct" x="174" y="142" text-anchor="middle">secondary 192.168.10.4/30</text><text class="sm" x="240" y="170" text-anchor="middle">eBGP on each link; the on-premises side prepends on the secondary to make the primary preferred inbound.</text></svg>
<figcaption><b>Figure 5.18</b> ExpressRoute private peering. Two BGP sessions, one per link, run between the customer edge and a redundant pair of Microsoft routers; the pair protects against a device failure, not against loss of the peering location.</figcaption>
</figure>

BFD can be enabled on ExpressRoute's private peering so that a failure is detected in a second or so instead of at the hold timer. Limits matter in design: each peering accepts only a documented maximum number of advertised prefixes and tears down the session above it, so large enterprises summarise; check the provider's current limits rather than trusting numbers in a book.

| Need | Choice |
|---|---|
| Quick start, low bandwidth, tolerates jitter | IPsec VPN |
| Predictable latency, high bandwidth, compliance | Direct Connect / ExpressRoute |
| Many branches, application-aware steering | SD-WAN, with VPN or private circuits as transport |
| Highest availability | two private circuits in different locations, plus a VPN |

::: trap
*Claim:* "One ExpressRoute circuit is redundant, because it has two links." *Why it is wrong:* both links usually terminate in the same peering location, so a facility failure or a carrier fibre cut can remove both. *Correct statement:* a circuit protects against a device failure; for site-level redundancy buy a second circuit in another location. Advertising the same prefixes over a VPN and ExpressRoute without setting preferences is a second trap, because it gives asymmetric routing.
:::

::: lens
[MICROSOFT · AMAZON]{.co}

Microsoft's cloud network engineer postings list VNets, ExpressRoute, Private Link, UDRs, VPN and NSGs, plus IS-IS, BGP and MPLS for the backbone. Typical scenarios: "design ExpressRoute with VPN failover and keep the routing symmetric" (the example above) and "on-premises advertises 10.0.0.0/8 and a VNet uses 10.1.0.0/16" (Q5.38). Amazon asks the Direct Connect equivalents and BGP troubleshooting.
:::

::: check
1. How do you make the primary link preferred for traffic from Azure to the campus? [^c513-1]
2. Why can a VPN backup advertising a /24 defeat an ExpressRoute that advertises a /16? [^c513-2]
3. How many tunnels does an AWS Site-to-Site VPN connection provide? [^c513-3]
:::

[^c513-1]: Prepend the AS path on the secondary advertisement so that the primary has the shorter path.
[^c513-2]: Longest-prefix match precedes every BGP preference; the more specific /24 wins.
[^c513-3]: Two.

## [5.14]{.sec}The life of a request in the cloud [Must · ■□□]{.tag} {#s5-14}

::: bigidea
One HTTPS request from a phone to a virtual machine uses every mechanism of this chapter in turn, and each hop adds or removes a header, so the request is best learnt as a table of hops.
:::

The student portal of Campus Net is hosted in a cloud region behind a CDN. A student in Chennai opens `https://portal.campus.example`. Figure 5.19 shows the header stack at each stage and the table lists the hops.

<figure>
<svg viewBox="0 0 480 178" width="480"><defs><marker id="a519" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker></defs><rect class="box" x="12" y="14" width="56" height="24" rx="2"/><text class="sm" x="40" y="30" text-anchor="middle">Phone</text><rect class="box" x="92" y="14" width="56" height="24" rx="2"/><text class="sm" x="120" y="30" text-anchor="middle">Edge PoP</text><rect class="box" x="172" y="14" width="56" height="24" rx="2"/><text class="sm" x="200" y="30" text-anchor="middle">Regional LB</text><rect class="box" x="252" y="14" width="56" height="24" rx="2"/><text class="sm" x="280" y="30" text-anchor="middle">Leaf / fabric</text><rect class="box" x="332" y="14" width="56" height="24" rx="2"/><text class="sm" x="360" y="30" text-anchor="middle">Host vSwitch</text><rect class="box" x="412" y="14" width="56" height="24" rx="2"/><text class="sm" x="440" y="30" text-anchor="middle">VM</text><line class="ln" x1="68" y1="26" x2="92" y2="26" marker-end="url(#a519)"/><line class="ln" x1="148" y1="26" x2="172" y2="26" marker-end="url(#a519)"/><line class="ln" x1="228" y1="26" x2="252" y2="26" marker-end="url(#a519)"/><line class="ln" x1="308" y1="26" x2="332" y2="26" marker-end="url(#a519)"/><line class="ln" x1="388" y1="26" x2="412" y2="26" marker-end="url(#a519)"/><rect class="box" x="43" y="50" width="74" height="15" rx="0"/><text class="sm" x="80" y="60.5" text-anchor="middle">Eth</text><rect class="box" x="43" y="65" width="74" height="15" rx="0"/><text class="sm" x="80" y="75.5" text-anchor="middle">IP → anycast</text><rect class="box" x="43" y="80" width="74" height="15" rx="0"/><text class="sm" x="80" y="90.5" text-anchor="middle">TCP 443</text><rect class="box" x="43" y="95" width="74" height="15" rx="0"/><text class="sm" x="80" y="105.5" text-anchor="middle">TLS</text><rect class="box" x="123" y="50" width="74" height="15" rx="0"/><text class="sm" x="160" y="60.5" text-anchor="middle">IP → VIP</text><rect class="box" x="123" y="65" width="74" height="15" rx="0"/><text class="sm" x="160" y="75.5" text-anchor="middle">TCP 443</text><rect class="box" x="123" y="80" width="74" height="15" rx="0"/><text class="sm" x="160" y="90.5" text-anchor="middle">TLS (new)</text><rect class="hl" x="203" y="50" width="74" height="15" rx="0"/><text class="sm" x="240" y="60.5" text-anchor="middle">outer IP → host</text><rect class="box" x="203" y="65" width="74" height="15" rx="0"/><text class="sm" x="240" y="75.5" text-anchor="middle">inner IP → VIP</text><rect class="box" x="203" y="80" width="74" height="15" rx="0"/><text class="sm" x="240" y="90.5" text-anchor="middle">TCP 443</text><rect class="box" x="203" y="95" width="74" height="15" rx="0"/><text class="sm" x="240" y="105.5" text-anchor="middle">TLS</text><rect class="box" x="283" y="50" width="74" height="15" rx="0"/><text class="sm" x="320" y="60.5" text-anchor="middle">Eth</text><rect class="box" x="283" y="65" width="74" height="15" rx="0"/><text class="sm" x="320" y="75.5" text-anchor="middle">IP VTEP→VTEP</text><rect class="box" x="283" y="80" width="74" height="15" rx="0"/><text class="sm" x="320" y="90.5" text-anchor="middle">UDP 4789</text><rect class="hl" x="283" y="95" width="74" height="15" rx="0"/><text class="sm" x="320" y="105.5" text-anchor="middle">VXLAN VNI</text><rect class="box" x="283" y="110" width="74" height="15" rx="0"/><text class="sm" x="320" y="120.5" text-anchor="middle">inner Eth + IP</text><rect class="box" x="283" y="125" width="74" height="15" rx="0"/><text class="sm" x="320" y="135.5" text-anchor="middle">TCP, TLS</text><rect class="box" x="363" y="50" width="74" height="15" rx="0"/><text class="sm" x="400" y="60.5" text-anchor="middle">Eth</text><rect class="box" x="363" y="65" width="74" height="15" rx="0"/><text class="sm" x="400" y="75.5" text-anchor="middle">IP → VM</text><rect class="box" x="363" y="80" width="74" height="15" rx="0"/><text class="sm" x="400" y="90.5" text-anchor="middle">TCP 443</text><rect class="box" x="363" y="95" width="74" height="15" rx="0"/><text class="sm" x="400" y="105.5" text-anchor="middle">TLS</text><text class="sm" x="240" y="168" text-anchor="middle">Headers grow as the packet enters the data centre and shrink as it reaches the VM.</text></svg>
<figcaption><b>Figure 5.19</b> Header stacks along the path of one HTTPS request (shaded rows are encapsulation added inside the provider). The inner packet is untouched from the edge to the VM.</figcaption>
</figure>

| # | Hop and device | What happens | Lookup or decision | See |
|---|---|---|---|---|
| 1 | Phone and resolver | DNS query; the name is a CNAME to the CDN, the answer is an anycast address 192.0.2.10 with a short TTL | resolver cache; EDNS Client Subnet | [§3.10](#s3-10){.ref} |
| 2 | Phone to ISP | TCP SYN to 192.0.2.10:443; the ISP may translate the source address | default route; NAT | [§3.6](#s3-6){.ref} |
| 3 | ISP and transit routers | the packet follows BGP to the nearest announcement, the Mumbai site | longest prefix in the FIB | §5.10, §5.8 |
| 4 | Edge PoP | the server's kernel completes the handshake; TLS ends here; layer-7 rules read the Host and path; cache miss | accept queue; cache key | [§7.10](#s7-10){.ref}, [§9.4](#s9-4){.ref} |
| 5 | Edge to region | a new, pooled connection crosses the provider backbone; each router hashes the 5-tuple over equal paths | ECMP | §5.3 |
| 6 | Regional edge router | the VIP is announced by the balancer tier; ECMP picks one balancer instance | ECMP hash | §5.9 |
| 7 | Layer-4 balancer | consistent hash and connection table choose a backend; the packet is wrapped in an outer IP header addressed to that host | Maglev table | §5.9 |
| 8 | Leaf, spine, leaf | the underlay carries the wrapped packet; the outer UDP source port spreads flows over spines | eBGP routes, ECMP | §5.4, §5.5 |
| 9 | Host NIC or vSwitch | the outer header is removed, the virtual-network identifier selects the tenant, security-group rules are evaluated and a flow entry is created | exact match on a flow table | §5.11, §5.12 |
| 10 | Virtual machine | the NIC driver hands the packet to the kernel, the TCP stack and the application's `accept` | socket table | [§7.10](#s7-10){.ref} |
| 11 | Reply | the VM answers; the stateful flow entry admits the reply; with DSR it goes straight to the fabric, otherwise back through the balancer | flow table; routing | §5.9 |
| 12 | Return to the phone | the edge re-encrypts, caches if allowed, and the response retraces the Internet path, which may be different | BGP, possibly asymmetric | [§4.7](#s4-7){.ref} |

When it breaks, the cause is nearly always on this list. Five failures recur, with the first check for each; the method for isolating them is the subject of [Pillar 11](#ch11){.ref}.

| Symptom | Likely cause | First check |
|---|---|---|
| Private instance cannot reach the Internet | no default route to a NAT gateway, or the NAT gateway sits in a subnet without an IGW route | route table of both subnets |
| Connection hangs after the handshake; ping works | MTU blackhole through an overlay or VPN (§5.5) | `ping -M do -s 1422`; lower the MSS |
| Ingress works, replies vanish | network ACL missing the ephemeral-port rule (a security group is stateful) | Flow Logs: ACCEPT then nothing |
| Works one way, fails when a second path appears | asymmetric routing through a NAT or firewall that tracks state | compare the paths of both directions |
| Two VPCs or a VNet and on-premises cannot talk | overlapping address ranges, or peering is not transitive | compare the CIDRs; check the routes in both directions |

::: lens
[GOOGLE · MICROSOFT · AMAZON]{.co}

"What happens when I type an address" is asked at every company ([§3.11](#s3-11){.ref} answers it for a campus). The cloud version is the follow-up for Google, Microsoft and Amazon: be ready to add the anycast front door, the layer-7 and layer-4 balancers, the overlay in the fabric, and the host's virtual switch. Name the lookup at each hop, as the table does, and say where state lives (the connection table, the flow table, the NAT table).
:::

::: check
1. Where does TLS usually end in this path, and why there? [^c514-1]
2. Which header lets the leaf-spine fabric spread tenant flows? [^c514-2]
3. Why may the reply take a different path from the request? [^c514-3]
:::

[^c514-1]: At the edge: it is close to the user, so the handshake is short, and it can read the request for caching and routing.
[^c514-2]: The outer UDP source port, a hash of the inner flow.
[^c514-3]: Each direction is routed independently by BGP and ECMP, and DSR deliberately sends the reply on another route.

:::
