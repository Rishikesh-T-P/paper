::: {.p10}

::: pack
## Problem Set {#ps10}

Every interview question of this pillar is solved once, here, in the compact template: a 30-second answer first, then approach, answer, code, follow-ups and mistakes where they apply. Tags give the companies and round where the topic was reported, the difficulty (■□□ easy, ■■□ medium, ■■■ hard) and the evidence (S: a specific question reported by candidates; T: a topic reported, our wording). All code is Python and has been checked for syntax; the tests use only the standard library.

::: problems

::: q
### Q10.1 Why automate networks? Give three benefits and one risk.
[CISCO · AMAZON · JUNIPER · TECH-1 · ■□□ · T]{.meta}

[30-second answer: consistency (one template gives every device the same lines), speed (concurrency turns hours into minutes) and auditability (the change, its input and its output are in Git and logs). The risk is blast radius: a wrong change is applied everywhere just as quickly.]{.short}

**Answer.** Attach a number to each: forty switches by hand take about four hours with a 70 % chance of at least one slip at a 3 % per-switch error rate ([10.1](#s10-1){.ref}); a script takes six minutes. Reproducibility is a fourth benefit, since a change tested in the lab is replayed byte for byte. **Follow-ups.** How do you contain the risk? Dry run, canary, post-checks, rollback ([10.15](#s10-15){.ref}). **Mistakes.** Answering only "it saves time", or ignoring the risk.
:::

::: q
### Q10.2 JSON, YAML or XML for a human-edited inventory?
[CISCO · GOOGLE · TECH-1 · ■□□ · T]{.meta}

[30-second answer: YAML, because it allows comments, has little punctuation and is easy to diff. JSON suits machine-to-machine APIs; XML is used where a protocol requires namespaces, as in NETCONF.]{.short}

**Answer.** All three describe the same tree, and a parser converts between them ([10.2](#s10-2){.ref}). People edit YAML in review, so comments (the reason for an exception) and a clean line-by-line diff matter. YAML's weaknesses are implicit typing (`no` becomes `false`, `010` octal) and whitespace sensitivity, handled by quoting strings, using `safe_load` and validating against a schema. **Mistakes.** Using JSON for a file people must annotate; loading YAML with the unsafe loader.
:::

::: q
### Q10.3 Paramiko or Netmiko: what problem does Netmiko solve?
[CISCO · AMAZON · TECH-1 · ■□□ · S]{.meta}

[30-second answer: Paramiko is raw SSH, so the script must sleep and guess when output ends. Netmiko adds per-vendor knowledge: login sequence, prompt detection, paging off, configuration mode entry and exit, and save.]{.short}

**Answer.** With Paramiko one writes `send`, `sleep`, `recv` and parses the prompt by hand; a slow command is truncated and a fast one wastes time. Netmiko's `send_command` reads until the device prompt returns, so it knows the answer is complete. It also normalises dozens of platforms through `device_type`. **Follow-ups.** When would you still use Paramiko? SFTP and Linux hosts. **Mistakes.** Saying Netmiko is "faster": it is more reliable, not faster.
:::

::: q
### Q10.4 What does `send_config_set` do differently from `send_command`?
[CISCO · AMAZON · ARISTA · TECH-1 · ■□□ · S]{.meta}

[30-second answer: `send_command` runs one operational command and returns its output, waiting for the prompt. `send_config_set` enters configuration mode, sends a list of lines, leaves, and returns the session text; it does not save.]{.short}

**Answer.** The first expects a query; the second changes state. After `send_config_set`, call `save_config()` once the change has been verified, because saving is a separate decision. For a configuration command sent through `send_command`, the device would answer `Invalid input` because the session is not in configuration mode. **Follow-ups.** How do you detect an error in a config push? Inspect the returned text for `Invalid input` or `%` markers, or use `error_pattern`. **Mistakes.** Forgetting that unsaved changes vanish at reload; saving blindly.
:::

::: q
### Q10.5 What is idempotency, and why does it matter for Ansible playbooks?
[CISCO · JUNIPER · NOKIA · TECH-1 · ■□□ · S]{.meta}

[30-second answer: an operation is idempotent if applying it twice leaves the same state as applying it once. It lets a playbook be re-run safely after a failure, and `changed=0` on the second run is the proof.]{.short}

**Answer.** Declarative modules (`ios_vlans`) read the current state and act only on the difference. Command modules (`ios_command`) always run and so always report `changed`. Idempotence matters because automation retries: a half-failed run is repaired by running it again. **Follow-ups.** Which operation is not idempotent? `ip route add` without a check, or appending a line to a list. **Mistakes.** Believing Ansible makes everything idempotent ([10.9](#s10-9){.ref}).
:::

::: q
### Q10.6 What is Git? Fetch versus pull; commit versus push.
[CISCO · AMAZON · GOOGLE · TECH-1 · ■□□ · S]{.meta}

[30-second answer: Git is a distributed version-control system that records every version of the files with author and message. `fetch` downloads remote changes without applying them; `pull` is fetch plus merge. A `commit` saves locally; `push` sends commits to the remote.]{.short}

**Answer.** Distributed means each clone holds the full history, so work continues offline and any clone can restore the repository. A branch is a movable label on commits; a merge or rebase joins branches ([10.13](#s10-13){.ref}). **Mistakes.** Treating a commit as shared before it is pushed; committing secrets.
:::

::: q
### Q10.7 Return the devices whose uptime is under one day, from `show version` text.
[AMAZON · CISCO · TECH-1 · ■■□ · S]{.meta}

[30-second answer: parse the uptime sentence with one regular expression that captures every `N unit` pair, convert units to seconds and compare with 86,400. Handle both IOS ("3 hours, 12 minutes") and EOS ("5 weeks, 4 days") wording.]{.short}

**Approach.** The uptime line lists units in descending order, and any may be absent, so a loop over `(\d+)\s+(year|week|day|hour|minute)s?` is more robust than a fixed pattern. Weights: year 365 days (IOS counts years as 365), week 7 days.

```python
import re

UNIT = {"year": 31536000, "week": 604800, "day": 86400, "hour": 3600, "minute": 60}
LINE = re.compile(r"uptime is (?P<t>.+)", re.I)
PAIR = re.compile(r"(\d+)\s+(year|week|day|hour|minute)s?", re.I)

def uptime_seconds(show_version: str) -> int | None:
    m = LINE.search(show_version)
    if not m:
        return None                                   # unknown: caller decides, never guess
    return sum(int(n) * UNIT[u.lower()] for n, u in PAIR.findall(m.group("t")))

def rebooted_recently(devices: list[dict]) -> list[str]:
    out = []
    for d in devices:
        s = uptime_seconds(d["show_version"])
        if s is not None and s < 86400:
            out.append(d["name"])
    return out

devs = [{"name": "acc1", "show_version": "acc1 uptime is 3 hours, 12 minutes"},
        {"name": "dist1", "show_version": "dist1 uptime is 1 year, 2 weeks, 1 day"},
        {"name": "leaf1", "show_version": "no uptime here"}]
assert rebooted_recently(devs) == ["acc1"]
assert uptime_seconds("x uptime is 1 week, 2 days, 3 hours, 4 minutes") == 604800 + 172800 + 10800 + 240
```

**Complexity.** Linear in the text length. **Follow-ups.** Why `None` for unparsable? Treating "unknown" as "recent" or "old" would hide a parse failure ([10.5](#s10-5){.ref}). **Mistakes.** Parsing only `hours`; forgetting `weeks`, which Cisco prints for uptimes above seven days.
:::

::: q
### Q10.8 Back up 100 devices fast and robustly. How?
[AMAZON · CISCO · MICROSOFT · TECH-1 · ■■□ · S]{.meta}

[30-second answer: a thread pool of about eight workers (the work is waiting on I/O), a timeout and bounded retries with back-off per device, no retry on authentication failure, one result per device without raising, logging, credentials from the environment or a vault, and a Git commit only when the configuration changed.]{.short}

**Approach.** The pool and retry skeleton is the script of [10.4](#s10-4){.ref}. What it lacks, and an interviewer expects, is change detection: two backups differ by timestamps and counters, so naive storage creates noise.

```python
import re, subprocess
from pathlib import Path

VOLATILE = re.compile(r"^(Building configuration|Current configuration|! Last configuration"
                      r"|! NVRAM config|ntp clock-period|! Time:).*$", re.M)

def normalise(cfg: str) -> str:
    return VOLATILE.sub("", cfg).strip() + "\n"

def store_if_changed(repo: Path, name: str, cfg: str) -> bool:
    path = repo / f"{name}.cfg"
    new = normalise(cfg)
    if path.exists() and path.read_text() == new:
        return False                                  # nothing to record
    path.write_text(new)
    subprocess.run(["git", "-C", str(repo), "add", path.name], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", f"{name}: configuration changed"], check=True)
    return True

assert normalise("Building configuration...\nhostname acc1\n") == "\nhostname acc1\n".lstrip("\n")
```

**Answer.** Eight workers is a ceiling set by the AAA server and device control planes, not by the interpreter; 100 devices at 6 s take 100 / 8 × 6 = 75 s. The exit status is non-zero if any device failed, so the scheduler alerts. **Follow-ups.** How do you find that a device changed unexpectedly? The Git history of that file; this is also drift detection. **Mistakes.** Committing secrets that appear in configurations (`username … secret`, SNMP strings): strip or encrypt them before storing.
:::

::: q
### Q10.9 How would you parse unstructured CLI output? Compare regex, TextFSM and Genie.
[CISCO · AMAZON · ARISTA · TECH-2 · ■■□ · S]{.meta}

[30-second answer: prefer an API with structured output; failing that, TextFSM (ntc-templates) for multi-line state-based parsing, Genie for a Cisco estate, TTP when writing your own, and plain regex for a single command on a single release.]{.short}

**Answer.** Regex is fastest to write and the most fragile. TextFSM separates variables from a small state machine, and hundreds of templates exist. Genie parsers are maintained by the vendor and return a consistent schema, at the price of a heavy dependency. Whatever the method, pin the release the parser was tested on and treat zero rows as an error ([10.5](#s10-5){.ref}). **Follow-ups.** What does `use_textfsm=True` do? Netmiko looks up the template for the platform and command in ntc-templates and returns a list of dictionaries. **Mistakes.** Parsing in production without a test that feeds saved real output.
:::

::: q
### Q10.10 Explain Jinja2 with a loop over interfaces.
[GOOGLE · MICROSOFT · AMAZON · TECH-1 · ■■□ · S]{.meta}

[30-second answer: Jinja2 combines a template with data. `{{ x }}` prints a value, `{% for %}` repeats a block, and filters transform values. A loop over a list of port dictionaries produces one `interface` stanza per port.]{.short}

**Answer.** Given `ports: [{name: Gi1/0/1, vlan: 10}, {name: Gi1/0/2, vlan: 20}]`, the template

```
{% for p in ports %}
interface {{ p.name }}
 switchport access vlan {{ p.vlan }}
{% endfor %}
```

renders two stanzas. Use `StrictUndefined` so a missing key is an error, `trim_blocks` for clean whitespace, and validate the data first ([10.6](#s10-6){.ref}). **Follow-ups.** Macros, `include` and inheritance for reuse; filters such as `join`, `sort` and custom ones. **Mistakes.** Putting decisions in the template that belong in the data; rendering unvalidated input.
:::

::: q
### Q10.11 What is a source of truth, and why not the devices' running config?
[GOOGLE · MICROSOFT · AMAZON · TECH-2 · ■■□ · T]{.meta}

[30-second answer: the SoT is the single authoritative record of intended state (a Git repository of YAML, or NetBox). The running config records only what is configured, so any manual error or half-applied change is "correct" by that definition and cannot be detected as drift.]{.short}

**Answer.** Intent and actual state must be separate so that they can be compared. The SoT also holds relations a device does not know: which VLAN belongs to which site, which prefix is allocated to whom. Changes enter through the SoT and the pipeline; devices are checked against it ([10.13](#s10-13){.ref}). **Follow-ups.** What if the SoT and a device disagree? A drift report decides whether to correct the device or to update the SoT, a human decision. **Mistakes.** Treating NetBox as the SoT of configuration text rather than of data.
:::

::: q
### Q10.12 NAPALM `load_merge_candidate` versus `load_replace_candidate`; risks of replace?
[CISCO · ARISTA · JUNIPER · TECH-2 · ■■□ · S]{.meta}

[30-second answer: merge adds the given lines to the running configuration; replace makes the running configuration equal to the given file. Replace deletes anything not in the file, including management access, so a missing line can lock you out.]{.short}

**Answer.** Replace is attractive because the result is exactly the rendered file and drift disappears; its price is that the file must be complete. The control is the diff: `compare_config()` before `commit_config()`, a commit timer or `reload in` for recovery, and a canary ([10.7](#s10-7){.ref}). **Follow-ups.** How does IOS implement replace? SCP plus `configure replace`, which needs the archive feature. **Mistakes.** Rendering a file without the management ACL and AAA lines, then committing it without reading the diff.
:::

::: q
### Q10.13 What is YANG? Explain container, list, leaf and key with an interface example.
[CISCO · JUNIPER · NOKIA · TECH-2 · ■■□ · S]{.meta}

[30-second answer: YANG is a language that defines the schema of configuration and state data: a tree of containers, lists, leaves and types. A `list` such as `interface` holds entries identified by a `key` such as `name`; each entry has leaves like `description` and `enabled`.]{.short}

**Answer.** `/interfaces` is a container; `interface` is a list keyed by `name`, so `interface[name='GigabitEthernet1/0/1']` picks one entry as a primary key picks a row; `description` is a leaf of type string. `config false` marks state (counters, `oper-status`). Models come in IETF, OpenConfig and native families ([10.10](#s10-10){.ref}). **Follow-ups.** Augment and deviation. **Mistakes.** Saying YANG is a protocol; it is a data-modelling language, carried by NETCONF, RESTCONF and gNMI.
:::

::: q
### Q10.14 NETCONF, RESTCONF and gNMI: transport, encoding, use.
[CISCO · JUNIPER · GOOGLE · ARISTA · TECH-2 · ■■□ · S]{.meta}

[30-second answer: NETCONF is XML over SSH (port 830) with candidate datastore and commit, for transactional configuration. RESTCONF is JSON or XML over HTTPS using HTTP verbs, for simple integrations. gNMI is protobuf over gRPC and HTTP/2, for streaming telemetry and configuration at scale.]{.short}

| | NETCONF | RESTCONF | gNMI |
|---|---|---|---|
| Transport | SSH subsystem, TCP 830 | HTTPS, 443 | gRPC/HTTP/2 with TLS, 9339 or vendor port |
| Encoding | XML | JSON or XML | protobuf, JSON_IETF |
| Operations | get, edit-config, commit, lock | GET, POST, PUT, PATCH, DELETE | Capabilities, Get, Set, Subscribe |
| Transactions | yes (candidate, commit) | no, each call applies | `Set` is atomic per request |
| Best for | multi-step safe changes | quick reads and edits, web tooling | telemetry, large fleets |

All three use YANG models, so the content is the same; only the carrier differs ([10.11](#s10-11){.ref}, [10.12](#s10-12){.ref}). **Mistakes.** Calling RESTCONF "REST on the device": it is YANG-driven.
:::

::: q
### Q10.15 Which port does NETCONF use, and what happens in `<hello>`?
[CISCO · JUNIPER · NOKIA · TECH-1 · ■□□ · S]{.meta}

[30-second answer: TCP 830, as the SSH subsystem `netconf`. Each side immediately sends a `<hello>` listing its capabilities (protocol version, optional features such as candidate and validate, and the YANG modules it supports); the session uses the capabilities both share.]{.short}

**Answer.** The client learns what the server can do before sending any request: whether a candidate datastore exists, whether `confirmed-commit` is supported, and which modules to use. The session also carries a session ID in the server's hello. Version 1.1 adds chunked framing after the hello. **Follow-ups.** What if the capability is missing? The client falls back to `running` and takes more care ([10.11](#s10-11){.ref}). **Mistakes.** Saying port 22.
:::

:::
:::

:::
