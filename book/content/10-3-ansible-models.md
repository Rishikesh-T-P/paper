::: {.p10}

## [10.9]{.sec}Ansible for networks [Should · ■■□]{.tag} {#s10-9}

*Ansible* is an agentless automation tool: the control machine reads a YAML *playbook*, connects to each device in an *inventory* and runs *tasks*, each calling a *module*. For network devices nothing is installed on the target, because the connection plug-in speaks SSH (`ansible.netcommon.network_cli`), NETCONF (`netconf`) or HTTPS (`httpapi`). Modules are shipped in *collections* per vendor: `cisco.ios`, `arista.eos`, `junipernetworks.junos`. The playbook is a printed checklist that every shift follows, readable by people who do not program.

```
# inventory.yml
all:
  children:
    access:
      hosts:
        acc1: {ansible_host: 10.255.0.21}
        acc2: {ansible_host: 10.255.0.22}
        acc3: {ansible_host: 10.255.0.23}
      vars:
        ansible_network_os: cisco.ios.ios
        ansible_connection: ansible.netcommon.network_cli
        ansible_user: netops
        ansible_password: "{{ vault_netops_password }}"   # from ansible-vault, never plain text
```

The playbook makes sure VLANs 10, 20 and 30 exist with the right names on every access switch, and sets one interface description. A *play* selects hosts; *tasks* run in order; each module call states a desired result, and the module decides whether anything must change.

```
# vlans.yml
- name: Campus Net access VLANs
  hosts: access
  gather_facts: false
  tasks:
    - name: Ensure VLANs exist
      cisco.ios.ios_vlans:
        config:
          - {vlan_id: 10, name: SALES, state: active}
          - {vlan_id: 20, name: ENG,   state: active}
          - {vlan_id: 30, name: GUEST, state: active}
        state: merged

    - name: Describe the uplink
      cisco.ios.ios_config:
        parents: interface GigabitEthernet1/1/1
        lines: [description trunk-to-dist1]
        save_when: modified
```

Run it twice. The first run changes the switches that lack the VLANs; the second must change nothing, and that is the test of *idempotence*, the property that applying the same change twice leaves the same state as applying it once.

```
$ ansible-playbook -i inventory.yml vlans.yml
TASK [Ensure VLANs exist] ***   changed: [acc1]   changed: [acc2]   ok: [acc3]
TASK [Describe the uplink] ***  changed: [acc1]   changed: [acc2]   changed: [acc3]
PLAY RECAP  acc1 : ok=2 changed=2   acc2 : ok=2 changed=2   acc3 : ok=2 changed=1
$ ansible-playbook -i inventory.yml vlans.yml
PLAY RECAP  acc1 : ok=2 changed=0   acc2 : ok=2 changed=0   acc3 : ok=2 changed=0
```

A dry run is `ansible-playbook -i inventory.yml vlans.yml --check --diff -l acc1`: `--check` computes the change without applying it, `--diff` prints it, and `-l acc1` limits the run to one host, which is the first canary step ([10.15](#s10-15){.ref}). Secrets are stored with `ansible-vault encrypt_string`, and the run is given `--ask-vault-pass` or a vault-id file kept out of Git.

**Resource modules** (`ios_vlans`, `ios_interfaces`, `ios_l3_interfaces`, `ios_bgp_global`) model one feature as structured data, read the device's current state, and compare it with the request, so they are idempotent by design. Their `state` decides what happens to anything not listed.

| `state` | Effect |
|---|---|
| `merged` | add or update what is listed; leave everything else |
| `replaced` | make each *listed resource* equal to the request (one VLAN or interface at a time) |
| `overridden` | make the *whole feature* equal to the request; remove unlisted resources |
| `deleted` | remove the listed resources (or all of them if none is listed) |
| `gathered` | read the device and return structured data; no change |
| `rendered`, `parsed` | produce CLI from data, or data from CLI text, offline |

::: trap
*Claim:* "Ansible is idempotent by magic." *Why it is wrong:* idempotence belongs to the module, not to the tool. `ios_command` always runs, so it always reports `changed`; `ios_config` compares text lines and reports `changed` every run if a line is written differently from the way the device echoes it (an abbreviated command, a `parents` list that does not match the hierarchy). *Correct statement:* prefer resource modules, write `ios_config` lines exactly as `show running-config` prints them, and treat a second run with `changed` above zero as a bug.
:::

Choose Ansible when the work is a repeatable checklist, the team is not mainly programmers, and vendor modules cover the feature. Choose Python ([10.8](#s10-8){.ref}) when the logic needs loops with decisions, calls to other systems, or unit tests. Many teams use both: Ansible for the standard changes, Python for the tools that wrap them.

## [10.10]{.sec}YANG data models [Must · ■■□]{.tag} {#s10-10}

*YANG* (RFC 7950) is a language for describing a tree of configuration and state data: its names, types and constraints. It is the building plan approved by the authority, and NETCONF, RESTCONF and gNMI are three different lorries that deliver furniture which must fit the plan. A YANG file is called a *module*, and it declares a namespace so that identical names from different modules do not collide. The building blocks are few.

| Statement | Meaning |
|---|---|
| `container` | a named group of children; has no key; at most one instance |
| `list` | a collection of entries, each identified by its `key` leaf (or leaves); a configuration list must have a key |
| `leaf` | one value of one type (`string`, `uint16`, `boolean`, `enumeration`, `inet:ipv4-address`) |
| `leaf-list` | a list of plain values with no sub-structure |
| `typedef`, `grouping`/`uses` | a reusable type; a reusable group of nodes |
| `augment` | one module adds nodes to another module's tree |
| `deviation` | a vendor states that it does not implement a node, or implements it differently |
| `config false` | a read-only node: operational state, such as counters |

A small module for Campus Net's switch ports shows each of them.

```
module campus-demo {
  yang-version 1.1;
  namespace "urn:example:campus-demo";
  prefix cd;
  typedef vlan-id { type uint16 { range "1..4094"; } }
  grouping port-config {
    leaf name        { type string; }
    leaf description { type string; }
    leaf vlan        { type vlan-id; }
  }
  container campus {
    list switch {
      key "hostname";
      leaf hostname { type string; }
      list port { key "name"; uses port-config; }
      leaf uptime { type uint32; config false; }
    }
  }
}
```

The tool `pyang -f tree campus-demo.yang` prints the shape of the data compactly. The symbols are the vocabulary one must be able to read at sight.

```
module: campus-demo
  +--rw campus
     +--rw switch* [hostname]
        +--rw hostname    string
        +--rw port* [name]
        |  +--rw name           string
        |  +--rw description?   string
        |  +--rw vlan?          vlan-id
        +--ro uptime?     uint32
```

| Symbol | Meaning | Symbol | Meaning |
|---|---|---|---|
| `rw` | configuration data (read-write) | `ro` | state data (read-only) |
| `*` | list or leaf-list | `?` | optional node |
| `[name]` | the list's key | `!` | presence container: its existence means something |
| `(choice)` | exactly one of the cases | `augment …` | nodes added by another module |

The IETF module `ietf-interfaces` (RFC 8343), abridged, has the same shape, and its `ietf-ip` augment (RFC 8344) adds the addresses.

```
module: ietf-interfaces
  +--rw interfaces
  |  +--rw interface* [name]
  |     +--rw name           string
  |     +--rw description?   string
  |     +--rw type           identityref
  |     +--rw enabled?       boolean
  |     +--ro oper-status    enumeration
  |     +--ro statistics
  |        +--ro in-octets?   yang:counter64
  augment /if:interfaces/if:interface:
     +--rw ipv4!
        +--rw address* [ip]
           +--rw ip               inet:ipv4-address-no-zone
           +--rw prefix-length?   uint8
```

The tree maps onto the CLI by path. The node `/interfaces/interface[name='GigabitEthernet1/0/1']/description` is the line ` description to-acc1` under `interface GigabitEthernet1/0/1`; `/interfaces/interface[name=…]/ietf-ip:ipv4/address[ip='10.0.0.1']/prefix-length` is the mask of the `ip address` line. The bracketed key `[name=…]` selects one list entry, exactly as a primary key selects one row.

**Three families of models.** *IETF* models (`ietf-interfaces`, `ietf-routing`) are standardised but lag the features of real devices. *OpenConfig* models are written by large operators for operational use, are vendor-neutral and are the usual language of gNMI. *Native* models (`Cisco-IOS-XE-native`, Arista's EOS native) mirror each vendor's CLI one-to-one, so they are complete but not portable.

| Family | Coverage | Portability | Typical use |
|---|---|---|---|
| IETF | basic features | high, but vendors implement subsets | NETCONF/RESTCONF baseline |
| OpenConfig | interfaces, BGP, LLDP, telemetry paths | high across Arista, Juniper, Nokia, Cisco | gNMI telemetry and multi-vendor config |
| Native | everything the device does | none | features absent from the other two |

Modules are found at yangcatalog.org and in each vendor's GitHub repository; the YANG Suite and `pyang` explore them. A *deviation* is the reason that two devices claiming the same model do not behave identically: the first thing to check when a standard path returns an error is that device's deviation file.

::: check
1. In a configuration `list`, what is mandatory? [^c10-9]
2. What does `ro` mean in a tree, and where would it be used? [^c10-10]
:::

[^c10-9]: A `key`, naming the leaf or leaves that identify an entry.
[^c10-10]: Read-only state data, for example `oper-status` and the counters; it cannot be written by `edit-config`.

## [10.11]{.sec}NETCONF and RESTCONF [Must · ■■□]{.tag} {#s10-11}

*NETCONF* (RFC 6241) is a protocol for installing, manipulating and deleting configuration. It runs as an SSH subsystem on **TCP port 830** (RFC 6242), exchanges XML, and treats the configuration as a transaction with a result for every request, like registered post with a receipt. The protocol is layered, and the layers are worth drawing.

<figure>
<svg viewBox="0 0 480 190" width="480"><defs><marker id="a111" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs>
<rect class="box" x="20" y="14" width="210" height="34"/><text class="lbl" x="125" y="29" text-anchor="middle">Content</text><text class="sm" x="125" y="41" text-anchor="middle">configuration and state data</text>
<rect class="box" x="20" y="48" width="210" height="34"/><text class="lbl" x="125" y="63" text-anchor="middle">Operations</text><text class="sm" x="125" y="75" text-anchor="middle">get-config, edit-config, commit, lock</text>
<rect class="box" x="20" y="82" width="210" height="34"/><text class="lbl" x="125" y="97" text-anchor="middle">Messages</text><text class="sm" x="125" y="109" text-anchor="middle">rpc, rpc-reply, notification</text>
<rect class="box" x="20" y="116" width="210" height="34"/><text class="lbl" x="125" y="131" text-anchor="middle">Secure transport</text><text class="sm" x="125" y="143" text-anchor="middle">SSH subsystem, TCP 830 (or TLS)</text>
<rect class="fill" x="290" y="14" width="170" height="34" stroke="#83469A"/><text class="lbl" x="375" y="29" text-anchor="middle">YANG module</text><text class="sm" x="375" y="41" text-anchor="middle">defines what the content may be</text>
<path class="acc" d="M290 31 L232 31" fill="none" marker-end="url(#a111)"/>
<text class="sm" x="290" y="75">XML on the wire; framing</text><text class="sm" x="290" y="86">"chunks" after the hello</text>
<text class="sm" x="290" y="130">RESTCONF reuses the content layer</text><text class="sm" x="290" y="141">over HTTPS (RFC 8040)</text>
<text class="sm" x="125" y="172" text-anchor="middle">Client and server both send &lt;hello&gt; with capabilities first</text>
</svg>
<figcaption><b>Figure 10.2</b> The NETCONF layers (RFC 6241). The YANG module constrains only the top layer; the three layers beneath carry any content.</figcaption>
</figure>

**The hello exchange.** On connecting, each side immediately sends a `<hello>` listing its *capabilities*, URIs naming the protocol version and optional features and every YANG module the server supports. The session proceeds only on the capabilities both sides share, which is how a client learns whether the server has a candidate datastore, supports `:validate` or `:confirmed-commit`, and which models it speaks.

```
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.1</capability>
    <capability>urn:ietf:params:netconf:capability:candidate:1.0</capability>
    <capability>urn:ietf:params:netconf:capability:validate:1.1</capability>
    <capability>http://openconfig.net/yang/interfaces?module=openconfig-interfaces</capability>
  </capabilities>
</hello>
```

**Datastores.** A *datastore* is a complete configuration. `running` is what the device is using; `startup` is what it loads at boot; `candidate` is an editable scratch copy that does nothing until it is committed. The candidate is valuable because several edits can be made, validated and applied together, or discarded, so the change is all-or-nothing; many IOS XE releases offer only `running`, and the client must check the capability.

| Operation | Purpose |
|---|---|
| `<get>` | read configuration and state data |
| `<get-config>` | read configuration only, from a named datastore, optionally filtered |
| `<edit-config>` | change a datastore; the `operation` attribute is `merge` (default), `replace`, `create`, `delete` or `remove` |
| `<copy-config>`, `<delete-config>` | copy or delete a whole datastore (for example running to startup) |
| `<lock>`, `<unlock>` | give one session exclusive write access to a datastore |
| `<validate>` | check a datastore for consistency without applying it |
| `<commit>` | copy candidate to running; with `confirmed` it reverts unless confirmed within a timeout |
| `<discard-changes>` | reset the candidate to the running configuration |
| `<close-session>`, `<kill-session>` | end this or another session |

The difference between `delete` and `remove` is a favourite question: `delete` fails if the node does not exist, `remove` succeeds either way, so `remove` is the idempotent choice for automation.

A safe change is a transaction: **lock** the datastore, **edit** the candidate, **validate**, **commit**, **unlock**; if any step returns an `<rpc-error>`, **discard** the changes and unlock, and the running configuration has never been altered. The `ncclient` library implements this directly.

```python
from ncclient import manager
from ncclient.operations import RPCError

NS = "urn:ietf:params:xml:ns:yang:ietf-interfaces"
SELECT = f'<interfaces xmlns="{NS}"><interface><name>GigabitEthernet1/0/1</name></interface></interfaces>'
CHANGE = f"""<config><interfaces xmlns="{NS}"><interface>
  <name>GigabitEthernet1/0/1</name><description>to-acc1 (uplink)</description>
</interface></interfaces></config>"""

with manager.connect(host="10.255.0.11", port=830, username="netops", password="secret",
                     hostkey_verify=True, device_params={"name": "iosxe"}, timeout=30) as m:
    print([c for c in m.server_capabilities if "ietf-interfaces" in c])   # does it speak the model?
    before = m.get_config(source="running", filter=("subtree", SELECT)).data_xml
    use_candidate = ":candidate" in m.server_capabilities
    target = "candidate" if use_candidate else "running"
    try:
        with m.locked(target):
            m.edit_config(target=target, config=CHANGE, default_operation="merge")
            if use_candidate:
                m.validate(source="candidate")
                m.commit()
    except RPCError as err:
        if use_candidate:
            m.discard_changes()
        raise SystemExit(f"change refused, running config untouched: {err}")
    after = m.get_config(source="running", filter=("subtree", SELECT)).data_xml
    print("changed" if before != after else "no change")
```

Expected result on `dist1`: the capability list contains the `ietf-interfaces` URN, the script prints `changed`, and `show running-config interface Gi1/0/1` shows ` description to-acc1 (uplink)`.

**RESTCONF** (RFC 8040) offers the same YANG data over HTTPS, so any HTTP client works. It is not arbitrary REST: URIs are derived from the model, and the media types are `application/yang-data+json` and `application/yang-data+xml`. The URI pattern is

```
https://<host>/restconf/data/<module>:<container>/<list>=<key>/<leaf>
```

with list keys written after `=`; a `/` inside a key must be percent-encoded (`GigabitEthernet1%2F0%2F1`).

```
$ curl -sk -u netops:$PW -H "Accept: application/yang-data+json" \
    https://10.255.0.11/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1%2F0%2F1
{"ietf-interfaces:interface": {"name": "GigabitEthernet1/0/1", "description": "to-acc1 (uplink)",
 "type": "iana-if-type:ethernetCsmacd", "enabled": true}}
$ curl -sk -u netops:$PW -X PATCH -H "Content-Type: application/yang-data+json" \
    -d '{"ietf-interfaces:interface":{"name":"GigabitEthernet1/0/1","description":"to-acc1"}}' \
    https://10.255.0.11/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1%2F0%2F1 -w '%{http_code}\n'
204
```

(`-k` skips certificate checking and belongs in a lab only; see [9.3](#s9-3){.ref}.) The verbs map to NETCONF operations as follows.

| HTTP | NETCONF equivalent | Meaning in RESTCONF |
|---|---|---|
| GET | `get` / `get-config` | read a resource; `?content=config` or `nonconfig` selects the kind |
| POST | `edit-config` operation `create` | create a child; fails if it exists |
| PUT | `edit-config` operation `replace` | replace the target resource |
| PATCH | `edit-config` operation `merge` | merge the supplied data |
| DELETE | `edit-config` operation `delete` | remove the resource |

RESTCONF has no candidate datastore, no lock and no commit: each request applies immediately to running. It is therefore simpler for single changes and for people who already know HTTP; NETCONF is the choice when a multi-step change must be atomic.

::: trap
*Claim:* "NETCONF runs on port 22." *Why it is wrong:* port 22 is plain SSH for the CLI. The IANA-assigned port for the NETCONF subsystem is 830, and some devices additionally accept the subsystem on 22. *Correct statement:* NETCONF is SSH subsystem `netconf` on TCP 830; RESTCONF is HTTPS on 443.
:::

::: lens
[CISCO · JUNIPER · NOKIA · GOOGLE]{.co}

"NETCONF versus RESTCONF versus gNMI" is asked by name. A strong answer gives transport, encoding and best use for each (compared in [10.12](#s10-12){.ref}), then states the deciding property: NETCONF for transactional configuration with candidate and commit, RESTCONF for simple HTTP integrations, gNMI for streaming telemetry and for configuration at scale. Expect "what is in the hello?" and "why a candidate datastore?"
:::

## [10.12]{.sec}gNMI and streaming telemetry [Should · ■■□]{.tag} {#s10-12}

For three decades monitoring meant *polling*: a management station asks each device for its counters every five minutes using SNMP. Polling is like calling the plumber every five minutes to ask whether there is a leak. A micro-burst that lasts two seconds, a link that flaps and recovers, a queue that fills for a moment, all fall between two polls and leave no trace. *Streaming telemetry* inverts the model: the device sends the data to a collector at a set interval or when a value changes, like a smart water meter that reports as soon as the flow changes.

| Property | SNMP polling | gNMI streaming |
|---|---|---|
| Direction | collector pulls | device pushes (after one subscription) |
| Granularity | 1 to 5 min typical | 1 to 10 s typical; or on change |
| Data model | MIBs, OIDs | YANG paths, mostly OpenConfig |
| Encoding and transport | ASN.1 BER over UDP | protobuf over gRPC and HTTP/2, TLS |
| Load on the device | one request per object per poll | one subscription, batched updates |
| Events | traps, unreliable (UDP) | `ON_CHANGE` updates, reliable (TCP) |

**gNMI** (the gRPC Network Management Interface) defines four RPCs on one gRPC service, over TCP with TLS. The IANA port is 9339; vendors use their own defaults (Arista EOS 6030, Nokia SR Linux 57400), so confirm on the target.

| RPC | Purpose |
|---|---|
| `Capabilities` | the models, encodings and gNMI version the target supports |
| `Get` | one-shot read of one or more paths |
| `Set` | transactional change with `update`, `replace` and `delete` operations |
| `Subscribe` | open a stream of updates |

A *path* is a slash-separated route through the YANG tree with keys in brackets, for example `/interfaces/interface[name=Ethernet1]/state/counters/in-octets`. *Encodings* are `JSON_IETF` (readable), `PROTO` (compact) and others. A subscription has a *mode*: `STREAM` keeps sending; `ONCE` sends the current values and closes; `POLL` sends values each time the client asks. Within a stream, each path has its own mode.

| Stream mode | Behaviour | Use for |
|---|---|---|
| `SAMPLE` (with an interval) | send the value every N seconds | counters, rates, utilisation |
| `ON_CHANGE` | send only when the value changes | oper-status, BGP state, LLDP neighbours |
| `TARGET_DEFINED` | the device chooses the better of the two per leaf | when one does not know |

In **dial-in** (the model above) the collector opens the gRPC connection to each device and subscribes. In **dial-out** the device opens the connection to a configured collector and pushes; this suits devices behind NAT or firewalls and avoids the collector holding thousands of sessions. The tool `gnmic` is a command-line client and collector.

```
# on leaf1 (Arista cEOS): enable gNMI
management api gnmi
   transport grpc default
$ gnmic -a 10.255.0.31:6030 -u admin -p admin --insecure capabilities
$ gnmic -a 10.255.0.31:6030 -u admin -p admin --insecure get --path /interfaces/interface[name=Ethernet1]/state/oper-status
$ gnmic -a 10.255.0.31:6030 -u admin -p admin --insecure subscribe \
    --path "/interfaces/interface[name=Ethernet1]/state/counters" \
    --mode stream --stream-mode sample --sample-interval 10s
{"source": "10.255.0.31:6030", "subscription-name": "default-1",
 "timestamp": 1792000000000000000, "updates": [{"Path": "interfaces/interface[name=Ethernet1]/state/counters/in-octets", "values": {"...": 9124031}}]}
```

(`--insecure` disables TLS and belongs in the lab only.) Replacing `--stream-mode sample` by `--stream-mode on-change` with the path `/interfaces/interface[name=Ethernet1]/state/oper-status` prints nothing until the port is shut, then prints one update `UP → DOWN` within a second.

<figure>
<svg viewBox="0 0 480 150" width="480"><defs><marker id="a121" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker><marker id="a122" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1A1D23"/></marker></defs>
<rect class="box" x="8" y="22" width="68" height="26"/><text class="lbl" x="42" y="39" text-anchor="middle">leaf1</text>
<rect class="box" x="8" y="60" width="68" height="26"/><text class="lbl" x="42" y="77" text-anchor="middle">leaf2</text>
<rect class="box" x="8" y="98" width="68" height="26"/><text class="lbl" x="42" y="115" text-anchor="middle">spine1</text>
<rect class="box" x="130" y="48" width="78" height="52" rx="2"/><text class="lbl" x="169" y="70" text-anchor="middle">gnmic</text><text class="sm" x="169" y="82" text-anchor="middle">collector</text><text class="sm" x="169" y="92" text-anchor="middle">normalise</text>
<rect class="box" x="262" y="48" width="78" height="52" rx="2"/><text class="lbl" x="301" y="70" text-anchor="middle">Prometheus</text><text class="sm" x="301" y="82" text-anchor="middle">time-series</text><text class="sm" x="301" y="92" text-anchor="middle">database</text>
<rect class="box" x="394" y="22" width="78" height="30" rx="2"/><text class="lbl" x="433" y="41" text-anchor="middle">Grafana</text>
<rect class="box" x="394" y="92" width="78" height="30" rx="2"/><text class="lbl" x="433" y="111" text-anchor="middle">Alertmanager</text>
<path class="acc" d="M130 74 L78 35" fill="none" marker-start="url(#a122)"/><path class="acc" d="M130 74 L78 73" fill="none" marker-start="url(#a122)"/><path class="acc" d="M130 74 L78 111" fill="none" marker-start="url(#a122)"/>
<line class="ln" x1="208" y1="74" x2="260" y2="74" marker-end="url(#a122)"/>
<line class="ln" x1="340" y1="62" x2="392" y2="40" marker-end="url(#a122)"/><line class="ln" x1="340" y1="86" x2="392" y2="104" marker-end="url(#a122)"/>
<text class="sm" x="103" y="20" text-anchor="middle">gNMI Subscribe (dial-in)</text>
<text class="sm" x="234" y="68" text-anchor="middle">scrape :9804</text>
<text class="sm" x="240" y="140" text-anchor="middle">Dial-out reverses the first arrows: devices connect to the collector.</text>
<text class="sm" x="433" y="142" text-anchor="middle">page / ticket</text>
</svg>
<figcaption><b>Figure 10.3</b> A model-driven telemetry pipeline. Devices stream; the collector turns updates into metrics; the database is scraped by Grafana and alert rules.</figcaption>
</figure>

**Sizing a pipeline** is arithmetic, and Q10.25 uses it. A single `SAMPLE` leaf at 10 s produces 6 updates per minute; with 8 counters per port, 10,000 ports and 100 bytes per update, the stream is 10,000 × 8 × 6 × 100 B / 60 s = 0.8 MB/s in steady state, about 70 GB per day before compression, which is why sample intervals, leaf selection and `ON_CHANGE` for state matter. Telemetry does not replace SNMP everywhere: traps and legacy monitoring systems persist, so a real estate runs both for a time.

::: lab
`LAB 10.2 · 60 MIN` Stream and flap. Start the telemetry stack from the containerlab topology (cEOS `leaf1`, `leaf2`; `gnmic`, Prometheus, Grafana containers).

```
gnmic -a leaf1:6030 -u admin -p admin --insecure subscribe \
  --path "/interfaces/interface[name=Ethernet1]/state/oper-status" --stream-mode on-change
# in another terminal:
docker exec clab-campus-leaf1 Cli -c "configure; interface Ethernet1; shutdown"
```
```
... "values": {"interfaces/interface/state/oper-status": "DOWN"}
```

**What you should notice:** the update arrives within about a second of the command, with no poll in between. With `--stream-mode sample --sample-interval 10s` on the counters instead, the same flap shows only as a dip in the next sample.
:::

:::
