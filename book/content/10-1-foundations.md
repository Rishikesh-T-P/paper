::: {.chapter .p10}
::: opener
[Part I · Pillar 10]{.part-label}

[10]{.num}

# Network Automation and Programmability {#ch10}

[From typing on one switch to pushing, checking and rolling back configuration on fifty devices from Git, and defending every choice in an interview.]{.promise}

1. [10.1 Why automate, and the maturity ladder]{} [MUST]{}
2. [10.2 JSON, YAML and XML]{} [MUST]{}
3. [10.3 Paramiko: SSH from first principles]{} [OPTIONAL]{}
4. [10.4 Netmiko: multi-vendor SSH]{} [MUST]{}
5. [10.5 Parsing CLI output]{} [SHOULD]{}
6. [10.6 Jinja2 and the source of truth]{} [MUST]{}
7. [10.7 NAPALM]{} [SHOULD]{}
8. [10.8 Nornir]{} [OPTIONAL]{}
9. [10.9 Ansible for networks]{} [SHOULD]{}
10. [10.10 YANG data models]{} [MUST]{}
11. [10.11 NETCONF and RESTCONF]{} [MUST]{}
12. [10.12 gNMI and streaming telemetry]{} [SHOULD]{}
13. [10.13 Git for network engineers]{} [MUST]{}
14. [10.14 CI/CD and testing]{} [SHOULD]{}
15. [10.15 Safety at scale]{} [OPTIONAL]{}
:::

<style>.p10 pre{font-size:7pt;line-height:1.38}</style>

Every example in this chapter belongs to **Campus Net**. Its access layer is three Cisco IOS XE switches, `acc1` to `acc3`; its distribution layer is `dist1` and `dist2` (IOS XE) and its border router is `br1` (IOS XE). Its data-centre extension ([5.2](#s5-2){.ref}) is two Arista cEOS leaves, `leaf1` and `leaf2`, under one FRR spine, `spine1`. Management addresses are `10.255.0.0/24`, and the VLANs are SALES (10, 192.168.10.0/24) and ENG (20, 192.168.20.0/24). The Python language itself is taught in [2.16](#s2-16){.ref} to [2.18](#s2-18){.ref}, and the shell and `jq` in [8.2](#s8-2){.ref}; this chapter teaches the *network* libraries and the practice around them. Every script has been written to be syntactically valid Python 3.10 or later; the libraries are third-party and must be installed with `pip` in a virtual environment.

## [10.1]{.sec}Why automate, and the maturity ladder [Must · ■□□]{.tag} {#s10-1}

A network is changed by people typing commands, and the commonest cause of an outage is a change that went wrong ([11.1](#s11-1){.ref}). Typing does not scale because each additional device costs the same minutes again, and it does not leave evidence because the only record is the shell history on the engineer's laptop. Automation replaces the typing with a program, and in doing so offers four things: *consistency* (every device receives the same lines), *speed* (forty devices take the time of one), *auditability* (the program, its input and its output are stored) and *repeatability* (a change that worked in the lab can be replayed exactly). The risk is the mirror image: a wrong change is also applied consistently and quickly, which is why §10.15 occupies a section of its own.

::: example
**Adding VLAN 30 (GUEST) to 40 access switches.**

1. By hand. Each switch needs a login, `vlan 30`, `name GUEST`, a trunk check and `write memory`: about six minutes with care. Forty switches take 40 × 6 = 240 min, four hours.
2. Typing errors. Suppose each switch has a 3 % chance of a slip (wrong VLAN on a trunk, a missed save). The chance that *all* forty are right is 0.97^40 ≈ 0.30, so there is a 70 % chance of at least one wrong switch, and an expected 1.2 wrong ones.
3. By script. Each switch takes about 9 s (connect 4 s, configure 5 s). With 8 worker threads the 40 switches finish in 5 rounds × 9 s = 45 s; reading the log and the diff adds about five minutes. The script gives the same lines to every switch, so the typo rate is the rate of one typo, in one file, where a reviewer can see it.

[Result: about 6 min against 4 h, and the residual risk is one reviewable mistake instead of forty unrecorded ones.]{.result}
:::

::: bigidea
Automation does not remove mistakes; it moves them from forty unrecorded keystroke sessions into one artefact that can be reviewed, tested and replayed.
:::

**The maturity ladder.** Teams do not jump to full automation; they climb. We number the steps L0 to L4, and each step is defined by *where the intended state of the network lives*.

<figure>
<svg viewBox="0 0 480 215" width="480"><defs><marker id="a101" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs>
<rect class="box" x="10" y="165" width="88" height="40"/><text class="lbl" x="54" y="181" text-anchor="middle">L0 Manual</text><text class="sm" x="54" y="194" text-anchor="middle">CLI, copy-paste</text>
<rect class="box" x="98" y="135" width="88" height="70"/><text class="lbl" x="142" y="151" text-anchor="middle">L1 Scripted</text><text class="sm" x="142" y="164" text-anchor="middle">Netmiko, Paramiko</text><text class="sm" x="142" y="175" text-anchor="middle">loops over devices</text>
<rect class="box" x="186" y="105" width="88" height="100"/><text class="lbl" x="230" y="121" text-anchor="middle">L2 Templated</text><text class="sm" x="230" y="134" text-anchor="middle">Jinja2 + YAML</text><text class="sm" x="230" y="145" text-anchor="middle">Nornir, Ansible</text><text class="sm" x="230" y="156" text-anchor="middle">source of truth</text>
<rect class="box" x="274" y="75" width="88" height="130"/><text class="lbl" x="318" y="91" text-anchor="middle">L3 Declarative</text><text class="sm" x="318" y="104" text-anchor="middle">intent in Git, CI,</text><text class="sm" x="318" y="115" text-anchor="middle">NETCONF / gNMI,</text><text class="sm" x="318" y="126" text-anchor="middle">pre/post checks</text>
<rect class="fill" x="362" y="45" width="108" height="160" stroke="#83469A"/><text class="lbl" x="416" y="61" text-anchor="middle">L4 Closed loop</text><text class="sm" x="416" y="74" text-anchor="middle">telemetry detects drift</text><text class="sm" x="416" y="85" text-anchor="middle">and failure; the system</text><text class="sm" x="416" y="96" text-anchor="middle">proposes or applies</text><text class="sm" x="416" y="107" text-anchor="middle">the correction</text>
<path class="acc" d="M20 150 L120 120 L215 90 L300 60 L395 30" fill="none" marker-end="url(#a101)"/>
<text class="sm" x="30" y="30">intent lives in: a head</text><text class="sm" x="30" y="41">→ a script → a template + data → a model in Git → a feedback loop</text>
</svg>
<figcaption><b>Figure 10.1</b> The maturity ladder. Each step changes where the intended state is kept, and therefore what can be reviewed, tested and replayed.</figcaption>
</figure>

| Step | Intended state lives in | Typical tools | Fails when |
|---|---|---|---|
| L0 manual | the engineer's head | CLI, notepad | people leave; changes differ per device |
| L1 scripted | a script of commands | Paramiko, Netmiko | the script is run twice or on the wrong model |
| L2 templated | data files plus templates | Jinja2, Ansible, Nornir | the data drift from the devices |
| L3 declarative | models and intent in Git, validated in CI | NETCONF, gNMI, NAPALM, Batfish | the tests do not model the real network |
| L4 closed loop | the running network, watched by telemetry | gNMI, alerting, remediation runbooks | automatic remediation acts on a false signal |

The reference architecture that the rest of the chapter assembles is a loop: the *source of truth* (data in Git, or an inventory such as NetBox) feeds a *renderer* (templates), which feeds a *pipeline* (tests and approval), which pushes over a *transport* (SSH, NETCONF, gNMI) to the devices, whose *telemetry* returns to a collector and, through alerting, back to a person or a pipeline. Sections 10.2 to 10.9 build the left half; 10.10 to 10.12 the transports and the return path; 10.13 to 10.15 the pipeline and its safety.

::: lens
[CISCO · AMAZON · JUNIPER · ARISTA]{.co}

"Why automate?" is asked as a warm-up and judged on specificity. A strong answer names three benefits with a mechanism each (consistency from one template, speed from concurrency, audit from Git) and one risk (blast radius), then adds a number from experience, such as the 4 h against 6 min comparison above. A likely follow-up is "what would you not automate?": one-off emergency changes whose cost of building the tooling exceeds the change, and anything nobody can yet test.
:::

::: check
1. At which ladder step does a Jinja2 template with a YAML file first appear? [^c10-1]
2. Why is "the device's running config" a poor place to keep intent? [^c10-2]
:::

[^c10-1]: L2. The data and the logic are separate files, so the data can be reviewed and the template reused.
[^c10-2]: It records what is configured, not what was meant; a manual change, a typo or a partial failure are all silently "correct" by that definition.

## [10.2]{.sec}JSON, YAML and XML [Must · ■□□]{.tag} {#s10-2}

CLI output is text written for a human reading a terminal: columns align by spaces, headings vary between releases and a script must guess where a field starts. *Structured data* names every field and nests related ones, so a program asks for `interface["description"]` instead of counting columns. Three formats appear in network work, and all three describe the same tree of keys, lists and values. *JSON* is the default of web APIs and maps directly onto Python dictionaries and lists. *YAML* is a superset that is pleasant to edit by hand and is used for inventories and playbooks. *XML* is verbose but supports namespaces, which NETCONF needs to say which YANG module a tag belongs to ([10.10](#s10-10){.ref}).

Consider one interface on `dist1`, first as the CLI shows it and then in the three formats.

```
interface GigabitEthernet1/0/1
 description to-acc1
 ip address 10.0.0.1 255.255.255.252
 no shutdown
```
```
{"interface": {"name": "GigabitEthernet1/0/1", "description": "to-acc1",
               "enabled": true, "ipv4": {"address": "10.0.0.1", "prefix-length": 30}}}
```
```
interface:
  name: GigabitEthernet1/0/1
  description: to-acc1
  enabled: true
  ipv4: {address: 10.0.0.1, prefix-length: 30}
```
```
<interface xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
  <name>GigabitEthernet1/0/1</name>
  <description>to-acc1</description>
  <enabled>true</enabled>
  <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
    <address><ip>10.0.0.1</ip><prefix-length>30</prefix-length></address>
  </ipv4>
</interface>
```

| Property | JSON | YAML | XML |
|---|---|---|---|
| Comments | no | yes (`#`) | yes (`<!-- -->`) |
| Human editing | tolerable | best | poor |
| Types | string, number, boolean, null, list, object | the same plus dates; **implicit** typing | all text; types come from the schema |
| Namespaces | no | no | yes |
| Used for | REST, RESTCONF, gNMI JSON, `show … \| json` | inventories, playbooks, CI files | NETCONF, older APIs |
| Python | `json` (standard library) | `yaml` (PyYAML) | `xml.etree`, `xmltodict`, `lxml` |

Conversion between them is a three-line job in Python, because each parser returns the same kind of object.

```python
import json, yaml, xmltodict

with open("interfaces.yml") as f:
    data = yaml.safe_load(f)                  # always safe_load: plain load can run code
for ifc in data["interfaces"]:
    if not ifc.get("enabled", True):          # missing key counts as enabled
        print(ifc["name"], "is administratively down")

print(json.dumps(data, indent=2))             # YAML -> JSON
xml_text = xmltodict.unparse({"interfaces": {"interface": data["interfaces"]}}, pretty=True)
back = xmltodict.parse(xml_text)              # XML -> dict (all values become strings)
```

Given `interfaces.yml` listing `Gi1/0/1` (enabled), `Gi1/0/2` (`enabled: false`) and `Gi1/0/3` (enabled), the script prints `Gi1/0/2 is administratively down`. Note that the XML round trip returns the string `"true"`, not the boolean, because XML carries no types: this is the usual reason a comparison silently fails after a conversion.

**Why structure beats screen-scraping.** A scraper depends on the exact layout of text that the vendor may change in any release; a column that widens, a new header line or a localised message breaks the regular expression, and it breaks silently by returning the wrong field. Structured output depends on a *schema*, which the vendor versions and documents. Hence the order of preference is: (i) a native API returning JSON or XML (`show interfaces | json` on Arista EOS, RESTCONF, NETCONF, gNMI); (ii) a parser with a maintained template ([10.5](#s10-5){.ref}); (iii) a hand-written regular expression, as a last resort.

**Validation.** Data typed by people contain mistakes, and a template renders a mistake as faithfully as a fact. A *schema* states what is allowed, and the check runs before anything touches a device. `jsonschema` validates JSON-shaped data (including loaded YAML) against a schema; `pydantic` does the same with Python classes. A worked example is in [10.6](#s10-6){.ref}.

::: trap
*Claim:* "YAML is just JSON without braces, so indentation is cosmetic." *Why it is wrong:* indentation is the syntax. A tab is illegal, two spaces fewer turn a key from a child into a sibling, and YAML 1.1 loaders read the unquoted words `no`, `off` and `yes` as booleans and `010` as an octal number. *Correct statement:* indent with spaces only, quote any string that could be read as another type (`"no"`, `"010"`) and always read data back with `safe_load` to check what was parsed.
:::

::: check
1. Which of the three formats can carry a namespace, and which protocol needs it? [^c10-3]
2. What does `yaml.safe_load("vlan: 010")` return for `vlan`? [^c10-4]
:::

[^c10-3]: XML; NETCONF, to name the YANG module that each element belongs to.
[^c10-4]: The integer 8 under YAML 1.1 rules (a leading zero means octal); quote the value to keep the string.

## [10.3]{.sec}Paramiko: SSH from first principles [Optional · ■□□]{.tag} {#s10-3}

*Paramiko* is a pure-Python implementation of the SSH protocol. SSH runs over TCP port 22 and proceeds in layers: the transport layer negotiates algorithms and exchanges keys, the user-authentication layer proves the client's identity, and the connection layer multiplexes *channels* over the one session, such as a command (`exec`), a terminal (`shell`) and file transfer (`sftp`). Paramiko exposes each of them, which gives full control and also full responsibility, much as driving a manual car does.

Two ways of running commands matter. `exec_command` opens an `exec` channel, runs one command and closes it; it suits Linux hosts and the few network operating systems that accept it. Most network devices want an interactive terminal, so one opens a `shell` channel with `invoke_shell()`, sends text, waits and reads whatever has arrived. The pager is the first obstacle: IOS stops after one screen with `--More--`, so the script sends `terminal length 0` first.

```python
import time
import paramiko

def run_show(host: str, user: str, password: str, cmd: str) -> str:
    client = paramiko.SSHClient()
    client.load_system_host_keys()                       # trust ~/.ssh/known_hosts
    client.set_missing_host_key_policy(paramiko.RejectPolicy())   # refuse unknown keys
    client.connect(host, username=user, password=password, timeout=10,
                   look_for_keys=False, allow_agent=False)
    try:
        chan = client.invoke_shell()
        chan.send("terminal length 0\n")
        time.sleep(0.5)
        chan.recv(65535)                                 # discard banner and prompt
        chan.send(cmd + "\n")
        time.sleep(1.0)                                  # crude: wait for the device
        out = b""
        while chan.recv_ready():
            out += chan.recv(65535)
        return out.decode(errors="replace")
    finally:
        client.close()

if __name__ == "__main__":
    text = run_show("10.255.0.21", "netops", "secret", "show version")
    with open("acc1-version.txt", "w") as f:
        f.write(text)
```

The weakness is visible in the line marked *crude*: Paramiko does not know where the device's answer ends, so the script sleeps and hopes. A slow `show tech-support` is truncated; a fast command wastes a second. Recognising the prompt is exactly what Netmiko adds, and for that reason one rarely uses Paramiko directly on network devices. It remains the right tool for SFTP transfers (`client.open_sftp().put(local, remote)`) and for Linux hosts.

::: trap
*Claim:* "`AutoAddPolicy` is fine in a lab, so it is fine in the script." *Why it is wrong:* it accepts any host key without checking, so an attacker who intercepts the connection presents his own key and receives the password ([9.8](#s9-8){.ref}). *Correct statement:* load `known_hosts` (or a managed key store) and use `RejectPolicy`, or pin the fingerprint, and accept a new key only through a deliberate, recorded step.
:::

## [10.4]{.sec}Netmiko: multi-vendor SSH made sane [Must · ■■□]{.tag} {#s10-4}

*Netmiko* wraps Paramiko with per-vendor knowledge: how to log in, how to recognise the prompt, how to disable paging, how to enter and leave configuration mode and how to save. It is the automatic gearbox fitted to the manual car. A connection is created by `ConnectHandler` with a `device_type` (`cisco_ios` for IOS and IOS XE, `cisco_xr`, `cisco_nxos`, `arista_eos`, `juniper_junos`, `linux`), and the object then offers the calls below.

| Call | Purpose | Notes |
|---|---|---|
| `send_command(cmd)` | run one show command, return text | waits for the prompt; `read_timeout=` for slow commands; `expect_string=` for odd prompts |
| `send_command_timing(cmd)` | same, but waits on silence | use when no stable prompt appears (confirmations) |
| `send_config_set([lines])` | enter config mode, send lines, leave | does **not** save; returns the session text |
| `send_config_from_file(path)` | as above, lines from a file | |
| `save_config()` | `write memory` or the vendor equivalent | separate step on purpose |
| `enable()` | enter privileged mode | needs `secret=` |
| `disconnect()` | close | use a `with` block |

The distinction that interviewers ask about ([Q10.4](#ps10){.ref}) is that `send_command` expects the *user-mode or privileged prompt* and returns output, while `send_config_set` first enters `configure terminal`, sends each line, and leaves; the lines are configuration, not queries, and nothing is persisted until `save_config()`.

**A multi-device backup.** The task: back up the running configuration of every device in the inventory, in parallel, with a time-stamped file per device, retries for transient timeouts, and a summary at the end. The script reads `inventory.yml` (hostname, address, `device_type`) and takes credentials from the environment, never from the file.

```python
import csv, os, time, logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import yaml
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
OUT = Path("backups") / datetime.now().strftime("%Y%m%d-%H%M%S")
RETRIES, WORKERS = 3, 8

def backup(dev: dict) -> tuple[str, str, str]:
    """Return (name, status, detail). Never raises: one failure must not stop the rest."""
    params = {"device_type": dev["device_type"], "host": dev["host"],
              "username": os.environ["NET_USER"], "password": os.environ["NET_PASS"],
              "conn_timeout": 15}
    for attempt in range(1, RETRIES + 1):
        try:
            with ConnectHandler(**params) as conn:       # disconnects on leaving the block
                cfg = conn.send_command("show running-config", read_timeout=60)
            (OUT / f"{dev['name']}.cfg").write_text(cfg)
            return dev["name"], "ok", f"{len(cfg.splitlines())} lines"
        except NetmikoAuthenticationException:
            return dev["name"], "auth-failed", "not retried: repeated bad logins lock accounts"
        except (NetmikoTimeoutException, OSError) as exc:
            logging.warning("%s attempt %d: %s", dev["name"], attempt, exc)
            time.sleep(2 ** attempt)                     # back off: 2 s, 4 s, 8 s
    return dev["name"], "timeout", f"gave up after {RETRIES} attempts"

def main() -> None:
    devices = yaml.safe_load(open("inventory.yml"))["devices"]
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = [pool.submit(backup, d) for d in devices]
        for fut in as_completed(futures):
            results.append(fut.result())
    with open(OUT / "summary.csv", "w", newline="") as f:
        csv.writer(f).writerows([("device", "status", "detail"), *sorted(results)])
    bad = [r for r in results if r[1] != "ok"]
    logging.info("%d ok, %d failed", len(results) - len(bad), len(bad))
    raise SystemExit(1 if bad else 0)                    # non-zero exit lets CI or cron notice

if __name__ == "__main__":
    main()
```

For `acc1` to `acc3`, `dist1`, `dist2`, `br1`, `leaf1` and `leaf2` the run prints `8 ok, 0 failed` and writes eight `.cfg` files and `summary.csv`. The design decisions are the ones an interviewer probes. *Threads* suit the job because each worker spends nearly all its time waiting for the network, so Python's global interpreter lock, which is released during network waits, does not limit it. *Eight workers* is a cap, not a goal: unlimited parallelism would open hundreds of simultaneous logins and can overload the TACACS+ server ([9.12](#s9-12){.ref}). With 20 devices at 6 s each, serial work takes 120 s and eight workers about 3 rounds × 6 s = 18 s. *Authentication failures are not retried*, because each retry is another bad login. *The function never raises*, so one dead switch does not hide the other seven results. *The exit status* reports failure to the scheduler ([8.4](#s8-4){.ref}).

::: lab
`LAB 10.1 · 45 MIN` Run the backup against a containerlab topology of `leaf1`, `leaf2` (cEOS) and `spine1` (FRR) plus two IOS XE images or sandboxes.

```
export NET_USER=admin NET_PASS=admin
python3 backup.py
```
```
INFO 5 ok, 0 failed
$ cat backups/*/summary.csv
device,status,detail
leaf1,ok,87 lines
```

**What you should notice:** shut one container with `docker stop` and rerun. The script logs three timeouts with growing gaps, reports `timeout` for that device and the other devices still succeed; the exit status is 1.
:::

::: check
1. Which Netmiko call saves the configuration, and why is it separate from `send_config_set`? [^c10-5]
2. Why are threads, not processes, adequate here? [^c10-6]
:::

[^c10-5]: `save_config()`; saving is a decision (one may wish to test first and roll back by reload), so the library does not do it implicitly.
[^c10-6]: The work is waiting on network I/O, during which the interpreter lock is released; processes would add memory and start-up cost for no gain.

:::
