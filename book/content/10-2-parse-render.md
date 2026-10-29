::: {.p10}

## [10.5]{.sec}Parsing CLI output: regex, TextFSM, TTP, Genie [Should · ■■□]{.tag} {#s10-5}

Some devices and some commands have no structured output, so the script receives text and must turn it into data. We compare four methods on one command, `show ip interface brief` on `acc1`, and ask a question that a monitoring script really needs: which interfaces are administratively up but have a line protocol that is down? That combination usually means a cable or a far-end fault.

```
Interface              IP-Address      OK? Method Status                Protocol
Vlan1                  unassigned      YES unset  administratively down down
Vlan10                 192.168.10.2    YES manual up                    up
Vlan20                 192.168.20.2    YES manual up                    up
GigabitEthernet1/0/1   unassigned      YES unset  up                    up
GigabitEthernet1/0/2   unassigned      YES unset  down                  down
GigabitEthernet1/1/1   10.0.0.2        YES manual up                    down
```

**Regular expressions.** A named-group pattern, with the `re` module of [2.18](#s2-18){.ref}, is the fastest to write and the first to break. The status column holds one word or two ("administratively down"), so a pattern that assumes single words fails on exactly the rows that matter.

```python
import re
ROW = re.compile(r"^(?P<intf>\S+)\s+(?P<ip>\S+)\s+\w+\s+\w+\s+"
                 r"(?P<status>administratively down|up|down)\s+(?P<proto>up|down)\s*$", re.M)
rows = [m.groupdict() for m in ROW.finditer(raw)]        # raw holds the text above
```

**TextFSM.** A *finite-state machine* reads the text line by line; a template declares the variables (`Value`) and, per state, the line patterns and what to do on a match. The community library *ntc-templates* holds hundreds of such templates for the commonest commands, and Netmiko applies them with `send_command(cmd, use_textfsm=True)`. Reading a template is a skill in itself, so we read one in full.

```
Value Required INTF (\S+)
Value IPADDR (\S+)
Value STATUS (up|down|administratively down)
Value PROTO (up|down)

Start
  ^${INTF}\s+${IPADDR}\s+\w+\s+\w+\s+${STATUS}\s+${PROTO}\s*$$ -> Record
```

Each `Value` line names a variable and gives its regular expression in brackets; `Required` discards a record without it. Under `Start`, the pattern begins with `^`, each `${NAME}` inserts the variable's expression, and `$$` is a literal end-of-line anchor. The header row does not match because `OK?` contains a question mark that `\w+` cannot consume, so no special case is needed. `-> Record` writes one record per match. The Python side is short.

```python
import io, textfsm

with open("show_ip_int_brief.textfsm") as t:
    fsm = textfsm.TextFSM(t)
rows = [dict(zip(fsm.header, r)) for r in fsm.ParseText(raw)]
bad = [r["INTF"] for r in rows if r["STATUS"] == "up" and r["PROTO"] == "down"]
print("up/down:", bad)
```

With the output above, `rows` has six dictionaries and the script prints `up/down: ['GigabitEthernet1/1/1']`: the uplink to `dist1` is enabled but the protocol is down. The same dictionaries are what `use_textfsm=True` returns, with lower-case keys (`intf`, `ipaddr`, `status`, `proto`) in the ntc-templates convention.

**TTP.** The *Template Text Parser* writes the template as the sample itself, replacing the variable parts with `{{ name }}`, which is easier to author and review than a state machine.

```
<group name="interfaces">
{{ intf }}   {{ ip }}   YES {{ method }}   {{ status | ORPHRASE }}   {{ proto }}
</group>
```

`ORPHRASE` lets a value contain spaces. The call is `ttp(data=raw, template=tmpl)`, then `.parse()` and `.result()`; Netmiko accepts `use_ttp=True, ttp_template=path`.

**Genie.** Cisco's *pyATS/Genie* library ships maintained parsers for several hundred commands across IOS XE, NX-OS and others, returning nested dictionaries that follow one schema per command. `device.parse("show ip interface brief")` returns `{"interface": {"Vlan10": {"ip_address": "192.168.10.2", "status": "up", "protocol": "up", ...}}}`, and the same call exists in Netmiko as `use_genie=True`. The cost is a large dependency and Cisco-centred coverage.

| Method | Strength | Weakness | Choose when |
|---|---|---|---|
| Regex | no dependency; quick | fragile on wrapped lines and optional columns | one command, one release, one-off |
| TextFSM / ntc-templates | many templates exist; multi-line state | writing new templates is slow | the command is already in ntc-templates |
| TTP | template looks like the output | smaller community | writing your own, for a vendor without templates |
| Genie | maintained by the vendor; consistent schema | heavy install; Cisco-focused | a Cisco estate already using pyATS |

::: trap
*Claim:* "A parser written against today's output will keep working." *Why it is wrong:* vendors add columns, reword headings and change spacing between releases, and a regular expression that no longer matches simply returns fewer rows, so the script reports a healthy network. *Correct statement:* prefer an API ([10.11](#s10-11){.ref}), pin the software release a parser was tested against, and treat "zero rows parsed" as an error, not as "nothing found".
:::

## [10.6]{.sec}Jinja2 templating and the source of truth [Must · ■■□]{.tag} {#s10-6}

A template separates three things that a hand-edited configuration mixes: the *data* (which VLANs, which ports), the *logic* (what a port configuration looks like) and the *transport* (how the text reaches the device). *Jinja2* is the Python templating language used by Ansible, Nornir and many internal tools. It replaces `{{ expression }}` with a value, runs `{% statement %}` blocks such as `for` and `if`, and applies *filters* with `|`, as in `{{ name | upper }}`. Like a wedding-card template, the names and dates change while the layout stays.

A *source of truth* (SoT) is the single place that records what the network is meant to be. It must be separate from the devices, because a device records only what is configured; a manual change, a typo or a half-applied push is "correct" by that definition. A YAML file in Git is the simplest SoT; *NetBox* (and its relatives Nautobot and Infrahub) adds a database, an API and relationships between devices, prefixes and VLANs. The data below is Campus Net's `sot.yml`.

```
vlans:
  10: {name: SALES}
  20: {name: ENG}
  30: {name: GUEST}
switches:
  acc1:
    uplink: GigabitEthernet1/1/1
    ports:
      - {name: GigabitEthernet1/0/1, vlan: 10, desc: sales-pc-01}
      - {name: GigabitEthernet1/0/2, vlan: 20, desc: eng-pc-07}
      - {name: GigabitEthernet1/0/3, vlan: 30, desc: guest-ap}
  acc2:
    uplink: GigabitEthernet1/1/1
    ports:
      - {name: GigabitEthernet1/0/1, vlan: 10, desc: sales-pc-02}
```

The template `access_switch.j2` follows. The flags `trim_blocks` and `lstrip_blocks`, set in the script, remove the blank line that each `{% … %}` line would leave behind.

```
hostname {{ name }}
!
{% for id, v in vlans.items() | sort %}
vlan {{ id }}
 name {{ v.name }}
{% endfor %}
!
{% for p in ports %}
interface {{ p.name }}
 description {{ p.desc }}
 switchport mode access
 switchport access vlan {{ p.vlan }}
 spanning-tree portfast
 no shutdown
{% endfor %}
interface {{ uplink }}
 description trunk-to-dist1
 switchport mode trunk
 switchport trunk allowed vlan {{ vlans.keys() | sort | join(",") }}
```

The renderer does three jobs in order: load, **validate**, render. Validation matters because a template renders a mistake as faithfully as a fact. `StrictUndefined` makes a missing variable an error rather than an empty string, and the checks below catch a VLAN that is out of range or not declared.

```python
import ipaddress
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from jsonschema import validate

SCHEMA = {"type": "object", "required": ["vlans", "switches"], "properties": {
    "vlans": {"type": "object", "additionalProperties": {
        "type": "object", "required": ["name"], "properties": {"name": {"type": "string"}}}},
    "switches": {"type": "object", "additionalProperties": {
        "type": "object", "required": ["uplink", "ports"], "properties": {
            "ports": {"type": "array", "items": {"type": "object",
                "required": ["name", "vlan", "desc"],
                "properties": {"vlan": {"type": "integer", "minimum": 1, "maximum": 4094}}}}}}}}}

def check(sot: dict) -> list[str]:
    errors = []
    for sw, spec in sot["switches"].items():
        for p in spec["ports"]:
            if p["vlan"] not in sot["vlans"]:
                errors.append(f"{sw} {p['name']}: VLAN {p['vlan']} is not declared in vlans")
    return errors

def main() -> None:
    sot = yaml.safe_load(open("sot.yml"))
    validate(sot, SCHEMA)                                  # raises ValidationError on type or range
    if errs := check(sot):
        raise SystemExit("\n".join(errs))
    env = Environment(loader=FileSystemLoader("templates"), trim_blocks=True,
                      lstrip_blocks=True, undefined=StrictUndefined)
    env.filters["netmask"] = lambda p: str(ipaddress.ip_network(p, strict=False).netmask)
    tpl = env.get_template("access_switch.j2")
    for name, spec in sot["switches"].items():
        text = tpl.render(name=name, vlans=sot["vlans"], **spec)
        open(f"rendered/{name}.cfg", "w").write(text + "\n")

if __name__ == "__main__":
    main()
```

For `acc1` the first lines of `rendered/acc1.cfg` are:

```
hostname acc1
!
vlan 10
 name SALES
vlan 20
 name ENG
vlan 30
 name GUEST
!
interface GigabitEthernet1/0/1
 description sales-pc-01
 switchport mode access
 switchport access vlan 10
```

If a person types `vlan: 40` for a port, the run stops before any file is written, with `acc2 GigabitEthernet1/0/1: VLAN 40 is not declared in vlans`. This is the central economy of templating: the error is found in a file, in seconds, at review time, instead of on a switch, after the change.

Three further features are used constantly. A *filter* is any function applied with `|`; the `netmask` filter registered above turns `10.0.0.0/30` into `255.255.255.252`. A *macro* (`{% macro port(p) %}…{% endmacro %}`) is a function inside a template, used to avoid repeating a block. *Inheritance* (`{% extends "base.j2" %}` with `{% block %}`) lets a platform template override only the lines that differ. Note that whitespace in a template is the whitespace of the output, and IOS treats indentation of sub-commands as significant to a human reader but not to the parser; Arista and Junos templates are less forgiving, so one compares the rendered file with the real configuration before trusting a template.

::: example
**Fix this template.** The following fragment should print one `vlan` stanza per VLAN but prints a stray blank line and fails on `acc2`.

```
{% for id, v in vlans %}
vlan {{ id }}
 name {{ v.name }}
{% endfor %}
```

1. `vlans` is a dictionary; iterating it yields keys only, so unpacking `id, v` fails. The fix is `vlans.items()`.
2. The blank lines come from the newline after each `{% … %}` tag. Set `trim_blocks=True`, or write `{%- … -%}` to strip whitespace on one side.
3. With `StrictUndefined`, `v.name` raises if a VLAN has no `name`; the schema above already requires it.

[Result: `{% for id, v in vlans.items() | sort %}` plus `trim_blocks=True`.]{.result}
:::

::: check
1. Which Jinja2 setting turns a missing variable into an error? [^c10-7]
2. Why validate the data before rendering? [^c10-8]
:::

[^c10-7]: `undefined=StrictUndefined` on the `Environment`.
[^c10-8]: A template renders wrong data as readily as right data; validation moves the failure from the device to the pull request.

## [10.7]{.sec}NAPALM: vendor-neutral getters and safe config replace [Should · ■■□]{.tag} {#s10-7}

*NAPALM* (Network Automation and Programmability Abstraction Layer with Multivendor support) puts one Python API in front of several operating systems. A *driver* per platform (`ios`, `iosxr`, `nxos`, `eos`, `junos`) translates the common calls into whatever that platform offers, as a universal remote controls televisions of different brands. Its two halves are *getters*, which return normalised dictionaries, and a *configuration workflow* with a candidate, a diff, a commit and a rollback.

| Getter | Returns |
|---|---|
| `get_facts()` | vendor, model, OS version, serial, hostname, uptime, interface list |
| `get_interfaces()` | per interface: `is_up`, `is_enabled`, `speed`, `mtu`, `mac_address`, `description` |
| `get_interfaces_counters()` | octets, packets, errors, discards per interface |
| `get_interfaces_ip()` | IPv4 and IPv6 addresses per interface |
| `get_lldp_neighbors()` | neighbour host and port per local interface |
| `get_arp_table()`, `get_mac_address_table()` | ARP and MAC entries |
| `get_bgp_neighbors()` | per VRF: router ID, peers, `is_up`, `remote_as`, address-family prefix counts |
| `get_route_to(destination)` | the routes that match |
| `get_config(retrieve="running")` | the configuration text |
| `is_alive()`, `cli([cmds])`, `ping()` | liveness, raw commands, ping from the device |

The first example compares BGP on `br1` (IOS XE) and `leaf1` (EOS) with the same code. Without NAPALM the script would parse two different outputs ([10.5](#s10-5){.ref}); with it the field names are identical, which is the entire value of the library. The protocol itself is taught in [4.7](#s4-7){.ref}.

```python
import os
from napalm import get_network_driver

def connect(driver_name: str, host: str):
    drv = get_network_driver(driver_name)
    dev = drv(hostname=host, username=os.environ["NET_USER"], password=os.environ["NET_PASS"],
              timeout=30)
    dev.open()
    return dev

for drv, host in [("ios", "10.255.0.1"), ("eos", "10.255.0.31")]:
    dev = connect(drv, host)
    try:
        for vrf, data in dev.get_bgp_neighbors().items():
            for peer, p in data["peers"].items():
                state = "up" if p["is_up"] else "DOWN"
                print(f"{host:12} {vrf:8} {peer:15} AS{p['remote_as']:<6} {state}")
    finally:
        dev.close()
```
```
10.255.0.1   global   203.0.113.1     AS100    up
10.255.0.31  global   10.0.0.1        AS65000  up
```

**The configuration workflow.** Changing a device through NAPALM has five steps, and the order is the safety property.

1. `load_merge_candidate(config=text)` stages *additional* lines; `load_replace_candidate(config=text)` stages a *complete* configuration that will replace the running one.
2. `compare_config()` returns a diff between running and candidate. An empty string means nothing would change.
3. `commit_config()` applies the candidate; `discard_config()` throws it away.
4. The script verifies (a getter, a ping) that the device behaves.
5. `rollback()` returns to the previous configuration if verification fails.

```python
leaf1 = connect("eos", "10.255.0.31")
leaf1.load_merge_candidate(config="ntp server 10.255.0.5\n")
diff = leaf1.compare_config()
print(diff)                                   # shows "+ntp server 10.255.0.5"
if not diff:
    leaf1.discard_config()
elif input("commit? [y/N] ") == "y":
    leaf1.commit_config()
    ok = any("10.255.0.5" in l for l in leaf1.cli(["show ntp associations"])["show ntp associations"].splitlines())
    if not ok:
        leaf1.rollback()                      # back to the pre-commit configuration
leaf1.close()
```

The mechanisms underneath differ, and the difference explains the failure modes. EOS and Junos have native candidate sessions or commit models, so the diff and the rollback are exact. On IOS the driver copies a file to the device by SCP and runs `configure replace` (which requires the archive feature and SCP enabled), so a replace is only as safe as that feature.

::: trap
*Claim:* "`load_replace_candidate` is just a bigger merge." *Why it is wrong:* replace makes the running configuration *equal* to the candidate, so everything absent from the file is removed, including the management ACL, the AAA lines or the SSH keys if the file was rendered without them. The device then loses the very access the script needs to roll back. *Correct statement:* use merge for adding lines; use replace only for a full, rendered configuration that includes management access, read the diff first, and commit with a timer (`commit_config(revert_in=…)` where the driver supports it).
:::

NAPALM also offers `compliance_report()`, which compares getters against a YAML file of expected values (for example, "BGP neighbour 10.0.0.1 is up"), so the same tool is used to enforce intent as well as to push it.

## [10.8]{.sec}Nornir: Python-native inventory and concurrency [Optional · ■■□]{.tag} {#s10-8}

*Nornir* is a framework, not a language: it supplies an *inventory* (hosts, groups, defaults), a *runner* that executes a Python function against every selected host in a thread pool, and *result* objects, while the tasks themselves are ordinary Python. It resembles Ansible's inventory with the full control of Python; the conductor hands each musician the score at once and collects how each performed. Plug-ins add tasks: `nornir_netmiko`, `nornir_napalm`, `nornir_jinja2`, `nornir_utils`.

An attribute is resolved by inheritance: a host's own value wins, then its groups, then the defaults.

```
defaults.yaml   ->  groups.yaml (leaf: platform eos, data.role leaf)  ->  hosts.yaml (leaf1: hostname 10.255.0.31)
```
```
# inventory/hosts.yaml
leaf1:
  hostname: 10.255.0.31
  groups: [leaf]
  data: {asn: 65101, loopback: 10.0.0.11}
leaf2:
  hostname: 10.255.0.32
  groups: [leaf]
  data: {asn: 65102, loopback: 10.0.0.12}

# inventory/groups.yaml
leaf:
  platform: eos
  data: {role: leaf}
```
```
# config.yaml
inventory:
  plugin: SimpleInventory
  options: {host_file: inventory/hosts.yaml, group_file: inventory/groups.yaml, defaults_file: inventory/defaults.yaml}
runner:
  plugin: threaded
  options: {num_workers: 8}
```

The worked task renders a template per host, pushes it as a *dry run*, shows every diff, and commits only if every diff is non-empty or approved and nothing failed.

```python
import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Result, Task
from nornir_jinja2.plugins.tasks import template_file
from nornir_napalm.plugins.tasks import napalm_configure

def deploy(task: Task, dry_run: bool) -> Result:
    rendered = task.run(task=template_file, template="leaf.j2", path="templates", **task.host.data)
    task.run(task=napalm_configure, configuration=rendered.result, dry_run=dry_run, replace=False)
    return Result(host=task.host, result="done")

nr = InitNornir(config_file="config.yaml")
nr.inventory.defaults.username = os.environ["NET_USER"]    # secrets from the environment,
nr.inventory.defaults.password = os.environ["NET_PASS"]    # never from inventory files
leaves = nr.filter(F(role="leaf"))

plan = leaves.run(task=deploy, dry_run=True)
for host, multi in plan.items():
    print(f"=== {host} ===")
    print(multi.failed and multi[0].exception or multi[-1].diff)

if plan.failed:
    raise SystemExit("dry run failed on: " + ", ".join(plan.failed_hosts))
if input("apply to %d leaves? [y/N] " % len(leaves.inventory.hosts)) == "y":
    result = leaves.run(task=deploy, dry_run=False)
    print("failed:", list(result.failed_hosts))
```

`F(role="leaf")` filters on the `data` dictionary, so selecting a *canary* (`F(name="leaf1")`) is one line, which is why a Nornir script grows into the staged rollout of [10.15](#s10-15){.ref} without restructuring. Note that `multi[0]` is the parent task's result and the sub-task results follow it. Choose Nornir over Ansible when the logic is genuinely programmatic (loops with decisions, calls to a database, unit tests); choose Ansible when the team writes declarative tasks and the logic is a checklist ([10.9](#s10-9){.ref}).

:::
