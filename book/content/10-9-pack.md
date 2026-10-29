::: {.p10}

::: pack
## Revision Spread {#rv10}

::: revision
::: top
**Ten facts.** (1) Automation moves intent from heads to scripts to templates and data to models in Git to a feedback loop (L0 to L4); the gain is review, replay and evidence. (2) JSON, YAML and XML carry the same tree; YAML for people, JSON for APIs, XML where namespaces are needed; always `safe_load` and validate. (3) Paramiko is raw SSH; Netmiko adds prompts, paging and config mode; `send_config_set` does not save. (4) Parse text only when no API exists: TextFSM, TTP, Genie, regex last; zero rows parsed is an error. (5) Jinja2 plus a validated YAML source of truth renders configs; `StrictUndefined`, `trim_blocks`. (6) NAPALM: getters, then `load_*_candidate`, `compare_config`, `commit_config`, `rollback`; replace deletes what is missing. (7) Ansible resource modules are idempotent; command modules are not; `--check --diff -l host`. (8) YANG defines the tree; NETCONF (SSH 830, XML, candidate and commit), RESTCONF (HTTPS, verbs) and gNMI (gRPC, streams) carry it. (9) `SAMPLE` for counters, `ON_CHANGE` for state; telemetry pushes, SNMP polls. (10) Git is the only way in; pipeline: lint, schema, test, Batfish, twin, approve, canary, post-check, rollback.

**Three figures to redraw.** The maturity ladder (Figure 10.1), the NETCONF layers (Figure 10.2) and the GitOps pipeline with its gates (Figure 10.4).
:::

### Which tool when?

| Need | Choose | Why |
|---|---|---|
| One-off command on a Linux host, or SFTP | Paramiko | raw SSH, full control |
| Show or change on many CLI devices | Netmiko | prompts, paging, vendors handled |
| Same API across vendors, safe diff and rollback | NAPALM | getters and candidate workflow |
| Inventory plus Python logic, concurrency | Nornir | threads, filters, plug-ins |
| Operator-readable checklist, vendor modules | Ansible | declarative, idempotent resource modules |
| Atomic multi-step change, device supports it | NETCONF | candidate, validate, commit |
| Simple read or edit from any HTTP client | RESTCONF | verbs and JSON |
| Counters, state, events at scale | gNMI | streams, OpenConfig paths |
| Config text from data | Jinja2 + YAML/NetBox | review and reuse |
| Pre-change reachability and ACL analysis | Batfish | offline, whole-network |
| Behaviour test of a change | containerlab + pytest/pyATS | digital twin |

### NETCONF operations and datastores

| Operation | Purpose | Notes |
|---|---|---|
| `get` / `get-config` | read state and config / config only | subtree or XPath filter |
| `edit-config` | change a datastore | `operation`: merge, replace, create, delete, remove |
| `copy-config`, `delete-config` | whole-datastore copy or delete | running to startup |
| `lock` / `unlock` | exclusive write access | pair them, release on error |
| `validate` | check without applying | needs `:validate` |
| `commit` | candidate to running | `confirmed` reverts on timeout |
| `discard-changes` | candidate reset to running | the abort path |
| `close-session` / `kill-session` | end own or another session | |

| Datastore | Meaning | Capability |
|---|---|---|
| `running` | active configuration | base |
| `candidate` | scratch copy, applied on commit | `:candidate` |
| `startup` | loaded at boot | `:startup` |

### Protocol comparison and ports

| | NETCONF | RESTCONF | gNMI |
|---|---|---|---|
| Transport | SSH subsystem | HTTPS | gRPC, HTTP/2, TLS |
| Port | 830 | 443 | 9339 (IANA); EOS 6030; SR Linux 57400 |
| Encoding | XML | JSON / XML | protobuf, JSON_IETF |
| Atomic change | yes | no | `Set` per request |
| Streaming | notifications | SSE (limited) | `Subscribe` |
| RFC / spec | 6241, 6242 | 8040 | OpenConfig gNMI spec |

| RESTCONF verb | NETCONF |
|---|---|
| GET | get / get-config |
| POST | edit-config create |
| PUT | edit-config replace |
| PATCH | edit-config merge |
| DELETE | edit-config delete |

URI: `https://HOST/restconf/data/MODULE:CONTAINER/LIST=KEY/LEAF`; `/` in a key is `%2F`; media type `application/yang-data+json`.

### Code and command cards

| Item | Form |
|---|---|
| Netmiko | `with ConnectHandler(device_type="cisco_ios", host=h, username=u, password=p) as c:` then `c.send_command("show ip int br", use_textfsm=True)`, `c.send_config_set([...])`, `c.save_config()` |
| `device_type` | `cisco_ios` (also IOS XE), `cisco_xr`, `cisco_nxos`, `arista_eos`, `juniper_junos`, `linux` |
| NAPALM | `get_network_driver("eos")(hostname=h, username=u, password=p)`; `open()`, getters, `load_merge_candidate(config=)`, `compare_config()`, `commit_config()`, `rollback()`, `close()` |
| Top getters | `get_facts`, `get_interfaces`, `get_interfaces_counters`, `get_interfaces_ip`, `get_lldp_neighbors`, `get_arp_table`, `get_mac_address_table`, `get_bgp_neighbors`, `get_route_to`, `get_config` |
| Ansible | `ansible-playbook -i inventory.yml site.yml --check --diff -l acc1` |
| Ansible states | `merged` add; `replaced` per resource; `overridden` whole feature; `deleted`; `gathered`; `rendered`; `parsed` |
| ncclient | `manager.connect(host=, port=830, username=, password=, hostkey_verify=True)`, `get_config`, `locked(target)`, `edit_config`, `validate`, `commit`, `discard_changes` |
| gnmic | `capabilities`, `get --path P`, `set --update-path P --update-value V`, `subscribe --path P --mode stream --stream-mode sample --sample-interval 10s` |
| Git | `clone`, `switch -c`, `add`, `commit`, `push`, `fetch`, `merge`, `revert`, `tag -a` |
| Rollback timers | IOS `reload in 10` / `reload cancel`; EOS `commit timer 00:10:00`; Junos `commit confirmed`; NETCONF `commit` with `confirmed` |

### YANG tree legend

| Symbol | Meaning |
|---|---|
| `rw` / `ro` | configuration / state |
| `*` | list or leaf-list |
| `?` | optional |
| `[name]` | key of the list |
| `!` | presence container |
| `augment` / `deviation` | another module adds nodes / a vendor departs from the model |

### Safety checklist

Dry run and diff; approval; canary then waves; pre/post-checks; rollback armed before the change; save only after verification; concurrency cap; secrets from a vault; audit log with commit ID; refuse diffs that remove routes or management access.

### Flashcards

| Q | A |
|---|---|
| Ladder steps L0 to L4 | manual, scripted, templated, declarative in Git, closed loop |
| Why not the running config as source of truth? | it records what is configured, not what was meant |
| `yaml.load` versus `safe_load` | the first can construct arbitrary objects; always use `safe_load` |
| YAML `no` unquoted becomes | boolean `false` (YAML 1.1); quote it |
| XML round trip returns booleans as | strings; XML carries no types |
| Paramiko `AutoAddPolicy` risk | accepts any host key: man-in-the-middle |
| `invoke_shell` versus `exec_command` | interactive channel versus one command per channel |
| Netmiko call that saves | `save_config()` |
| Why no retry on authentication failure | each retry is another bad login and may lock the account |
| Thread pool size for backups | small (about 8): capped by AAA and device control planes |
| TextFSM `Record` | writes the current variables as one row |
| `use_textfsm=True` needs | a matching ntc-templates entry for platform and command |
| Jinja2 setting for missing variable error | `undefined=StrictUndefined` |
| `trim_blocks` | removes the newline after a block tag |
| NAPALM merge versus replace | add lines versus make running equal to the file |
| Risk of replace | deletes what is missing, including management access |
| NAPALM five-step flow | load, compare, commit, verify, rollback |
| Ansible module that is not idempotent | `ios_command` (and `raw`); `ios_config` if lines mismatch the echo |
| `overridden` versus `replaced` | whole feature versus listed resource |
| Idempotence test for a playbook | second run shows `changed=0` |
| YANG `list` must have | a `key` (for configuration lists) |
| `config false` means | state data, read-only |
| IETF, OpenConfig, native models | standard basics, operator-led portable, complete but vendor-specific |
| NETCONF port and transport | 830, SSH subsystem |
| What does `<hello>` carry? | capabilities and, from the server, a session ID |
| `delete` versus `remove` | fails if absent versus succeeds either way |
| Why a candidate datastore | atomic, validated, discardable multi-step change |
| RESTCONF PATCH equals | NETCONF merge |
| gNMI four RPCs | Capabilities, Get, Set, Subscribe |
| `ON_CHANGE` fits | oper-status, BGP state, LLDP |
| `SAMPLE` fits | counters at an interval |
| Dial-out means | the device connects to the collector |
| Fetch versus pull | download only versus download and merge |
| Secret committed to Git | rotate it; history keeps the old value |
| Batfish needs | configuration files only; no devices |
| Canary purpose | meet real hardware and traffic with one device first |
:::
:::

:::
