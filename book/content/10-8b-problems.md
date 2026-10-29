::: {.p10}

::: pack
## Problem Set, continued: protocols, design and incident questions {#ps10b}

::: problems

::: q
### Q10.16 What are NETCONF datastores, and why is a candidate valuable?
[CISCO · JUNIPER · NOKIA · TECH-2 · ■■□ · S]{.meta}

[30-second answer: `running` is the active configuration, `startup` is loaded at boot, `candidate` is an editable scratch copy that has no effect until committed. It lets several edits be made, validated and applied as one atomic change, or discarded.]{.short}

**Answer.** Without a candidate, each `edit-config` hits the live configuration at once, so a change of five steps is visible half-done. With one, the sequence is lock, edit, validate, commit, unlock; an error leads to `discard-changes`, and running was never touched. `confirmed-commit` adds a timer that reverts unless the commit is confirmed, which protects against a change that cuts the management path. **Follow-ups.** Which devices lack it? Many IOS XE releases are `writable-running` only. **Mistakes.** Assuming every device has a candidate; check the capability in the hello.
:::

::: q
### Q10.17 Map RESTCONF HTTP methods to NETCONF operations.
[CISCO · JUNIPER · TECH-1 · ■■□ · S]{.meta}

[30-second answer: GET is `get`/`get-config`; POST is `edit-config` with `create`; PUT is `replace`; PATCH is `merge`; DELETE is `delete`.]{.short}

**Answer.** The URI is `/restconf/data/<module>:<path>`, list keys after `=`, with `/` in a key encoded as `%2F`. The media type is `application/yang-data+json` or `+xml`. Unlike NETCONF there is no lock, candidate or commit: each call takes effect immediately, so RESTCONF is not suitable for a multi-step atomic change. PATCH is the usual choice for "set this leaf" because it leaves siblings alone, whereas PUT replaces the target resource ([10.11](#s10-11){.ref}). **Mistakes.** Using PUT on a whole interface when only the description was meant, which resets its other leaves.
:::

::: q
### Q10.18 Streaming telemetry versus SNMP polling: why did hyperscalers move?
[GOOGLE · MICROSOFT · ARISTA · TECH-2 · ■■□ · S]{.meta}

[30-second answer: polling shows only what happens at the instants of the poll and costs the device a request per object per poll; streaming pushes updates at seconds' granularity or on change, with a structured YANG model, over a reliable transport.]{.short}

**Answer.** Events shorter than the poll interval are invisible to polling; a link that flaps in 30 s between five-minute polls leaves no trace. Polling 100,000 objects per device from several systems loads the control-plane CPU, whereas one subscription batches updates. SNMP traps are UDP and may be lost; `ON_CHANGE` updates ride TCP. The data are named by YANG paths rather than OIDs, so one OpenConfig path serves several vendors ([10.12](#s10-12){.ref}). **Follow-ups.** Does it replace SNMP? Not entirely: traps and legacy systems remain, and the two coexist for years. **Mistakes.** Claiming telemetry is "faster" without saying why.
:::

::: q
### Q10.19 Explain gNMI subscription modes. ON_CHANGE or SAMPLE?
[GOOGLE · ARISTA · JUNIPER · NOKIA · TECH-2 · ■■□ · S]{.meta}

[30-second answer: `STREAM` continues until cancelled, `ONCE` returns the current values and closes, `POLL` returns values on each client request. Within a stream, `SAMPLE` sends at an interval and `ON_CHANGE` sends only when the value changes. Use `SAMPLE` for counters and `ON_CHANGE` for state.]{.short}

**Answer.** Counters change every packet, so `ON_CHANGE` would flood; only a time series with an interval is meaningful. Operational state (`oper-status`, BGP session state, LLDP neighbours) changes rarely and matters at once, so `ON_CHANGE` gives delay of about a second and almost no traffic. `TARGET_DEFINED` lets the device choose per leaf. A heartbeat interval re-sends unchanged values so that a collector can tell silence from a dead stream. **Mistakes.** `ON_CHANGE` on counters; very short sample intervals on thousands of ports.
:::

::: q
### Q10.20 Ansible or Python scripts: when would you pick each?
[CISCO · JUNIPER · NOKIA · TECH-1 · ■■□ · S]{.meta}

[30-second answer: Ansible for repeatable, declarative checklists that operators who do not program must run, using vendor collections and idempotent modules. Python for logic with branches, calls to other systems, and unit tests.]{.short}

| Criterion | Ansible | Python (Netmiko, NAPALM, Nornir) |
|---|---|---|
| Team skill | operators, YAML | programmers |
| Task shape | state the desired end | loop, decide, compute |
| Idempotence | by module | by your code |
| Testing | `--check`, molecule | `pytest`, mocks |
| Error handling | blocks, `rescue` | exceptions, any logic |

**Answer.** Most teams use both: Ansible runs the standard changes and a Python tool decides what to run. **Mistakes.** Writing loops and conditionals in YAML until the playbook is an unreadable program; or writing Python to do what a resource module already does idempotently.
:::

::: q
### Q10.21 What goes into a CI pipeline for network configuration changes?
[CISCO · AMAZON · GOOGLE · TECH-2 · ■■□ · S]{.meta}

[30-second answer: lint, schema validation, render, unit tests on the rendered text, static analysis with Batfish, a digital-twin lab test, a diff artefact for the reviewer, an approval gate, canary deployment, post-checks and automatic rollback.]{.short}

**Answer.** Order stages from cheap to expensive so that most failures happen in seconds ([10.14](#s10-14){.ref}). Each stage has a named defect: lint (syntax), schema (a VLAN 4096), unit test (a dropped `no shutdown`), Batfish (an undefined route-map), lab (BGP does not establish), post-check (route count fell). The pipeline posts the rendered diff on the pull request. **Follow-ups.** What do you not test? Hardware limits and optics; the canary covers them. **Mistakes.** A pipeline that only lints.
:::

::: q
### Q10.22 Design a rollout of new NTP and AAA configuration to 5,000 devices on three vendors with automatic rollback.
[AMAZON · CISCO · GOOGLE · HM · ■■■ · T]{.meta}

[30-second answer: model the data once in a source of truth, render per vendor, test in a digital twin, then roll out in waves (1, 1 %, 10 %, the rest) with a concurrency cap, per-device pre/post-checks, and a device-side timer that reverts the change if management access is lost.]{.short}

**Approach.** (i) *Data*: one YAML for NTP servers, TACACS+ servers and keys' references, with per-site overrides. (ii) *Render*: a Jinja2 template per OS family (IOS XE, EOS, Junos), unit-tested on rendered text. (iii) *Test*: Batfish for syntax and references; containerlab for each family. (iv) *Rollout*: AAA is the dangerous half, because a wrong key locks everybody out, including the automation. Therefore NTP first, then AAA with the old servers kept as fallback and local-user fallback. (v) *Rollback*: `reload in` or `commit confirmed` or `commit timer` armed before the push, cancelled only after a post-check that logs in *again with the new method* and reads NTP status. (vi) *Pace*: 5,000 devices at 8 per batch of 20 s is 5000 / 8 × 20 = 12,500 s, about 3.5 h; with 32 workers, under an hour, still below the AAA server's session limit. Waves with a soak time dominate the schedule.

**Answer.** Stop at the first failure in a wave; record all results; leave the pipeline's own jump host out of the first wave so that someone can repair the rest. **Follow-ups.** What if a device is offline? Mark it pending and converge it later; a declarative push is idempotent. **Mistakes.** Changing AAA and NTP in one step; testing only the success path of authentication.
:::

::: q
### Q10.23 Your automation pushed a bad ACL that isolated 30 sites. Walk through response and process changes.
[AMAZON · MICROSOFT · GOOGLE · HM · ■■■ · T]{.meta}

[30-second answer: stop the pipeline, restore service first (revert the commit and redeploy, or use out-of-band access), communicate, then run a blameless post-mortem and add the missing control: a diff guard, a canary and a post-check.]{.short}

**Approach.** *Contain*: pause all jobs so that nothing else changes; identify the change by the commit and tag. *Restore*: `git revert` the commit and run the pipeline against the 30 sites in groups; where management is cut, use the out-of-band console or the device-side timer, if one was armed. *Communicate*: a status page and named owner every 30 minutes. *Learn*: the timeline from logs (who approved what, which tests passed, which did not exist). *Fix the process*: a rule to refuse diffs that touch management ACLs; Batfish `testFilters` for management reachability in CI; a first wave of one site with a post-check from the management network; a revert timer. **Mistakes.** Blaming the engineer; fixing the ACL forward under pressure instead of reverting to the last known good state ([11.1](#s11-1){.ref}).
:::

::: q
### Q10.24 How would you test a configuration change before production?
[CISCO · ARISTA · AMAZON · TECH-2 · ■■■ · S]{.meta}

[30-second answer: a digital twin in containerlab for behaviour, Batfish for whole-network analysis offline, unit tests of the rendered text, then a canary with pre/post-checks and rollback in production.]{.short}

**Answer.** The four layers catch different faults. Unit tests catch template errors in milliseconds. Batfish evaluates routing and filters from configuration files and answers "can GUEST reach SALES?" without a device. The twin runs real control-plane software, so protocol sessions form and pings cross. The canary meets what no emulation has: hardware limits, real optics, real traffic. State the limits honestly: a twin has different performance and some features do not exist in the container images ([10.14](#s10-14){.ref}). **Mistakes.** Treating a green lab as proof; testing only the happy path.
:::

::: q
### Q10.25 Design telemetry that detects micro-bursts on 10,000 ports and alerts within 30 s. Estimate the data.
[GOOGLE · MICROSOFT · ARISTA · HM · ■■■ · T]{.meta}

[30-second answer: sampling counters every 10 s cannot see a burst of milliseconds, so use device-side detection (queue-depth thresholds, drop counters, or a burst-event feature) streamed `ON_CHANGE`, plus 10 s counter samples for context. About 4,000 samples per second, about 35 GB a day raw, and an alert path of about 20 s.]{.short}

**Approach.** *What to measure*: a micro-burst is a short queue fill: it shows as tail drops or a high queue-depth watermark, not as average utilisation (a 10 s mean of a 5 ms burst at line rate is 0.05 %). So subscribe to drop counters and the queue high-watermark per port. *Volume*: 10,000 ports × 4 leaves (in-octets, out-octets, discards, queue watermark) every 10 s is 4,000 updates/s; at 100 B each that is 400 kB/s, 34.6 GB/day raw. A time-series database stores a sample in about 1.5 B, so 4,000 × 86,400 × 1.5 B ≈ 0.5 GB/day. *Capacity*: 10,000 ports on 48-port devices is about 210 devices; four `gnmic` collectors at roughly 50 devices each. *Latency budget*: 10 s sample interval, plus 2 s transport and write, plus an alert rule evaluating over 15 s, gives about 27 s, inside 30 s.

**Answer.** Show the pipeline of Figure 10.3 and say where it scales: collectors are sharded by device, the database by time and label. Alert on rate of drops, not on a single sample, to avoid noise. **Follow-ups.** What if the device cannot detect bursts? Mirror to a probe, or use shorter sample intervals on a small set of suspect ports. **Mistakes.** Promising to see milliseconds with 10 s sampling.
:::

::: q
### Q10.26 Write a Python `Device` class with `connect`, `get_interfaces` and `push_config(dry_run=True)`, and unit-test it without devices.
[AMAZON · CISCO · ARISTA · TECH-2 · ■■■ · S]{.meta}

[30-second answer: inject the connection factory so tests can pass a fake, keep parsing in a pure function, and make `dry_run` the default so that sending needs an explicit decision. Tests then assert on calls and results without the network.]{.short}

**Approach.** Three decisions make it testable: *dependency injection* (the constructor accepts a `connector`), *pure parsing* (a function from text to data) and *safe default* (`dry_run=True`). The test double records what was sent.

```python
from __future__ import annotations
import unittest

def parse_brief(text: str) -> dict[str, dict]:
    """Parse 'show ip interface brief' into {name: {ip, status, proto}}."""
    out = {}
    for line in text.splitlines()[1:]:
        parts = line.split()
        if len(parts) < 6:
            continue
        status = " ".join(parts[4:-1])                    # "administratively down" has two words
        out[parts[0]] = {"ip": parts[1], "status": status, "proto": parts[-1]}
    return out

class Device:
    def __init__(self, name: str, host: str, connector=None, device_type: str = "cisco_ios"):
        self.name, self.host, self.device_type = name, host, device_type
        self._connector, self._conn = connector, None

    def connect(self, **creds) -> None:
        if self._connector is None:
            from netmiko import ConnectHandler            # imported late: tests need no library
            self._connector = ConnectHandler
        self._conn = self._connector(device_type=self.device_type, host=self.host, **creds)

    def get_interfaces(self) -> dict[str, dict]:
        return parse_brief(self._conn.send_command("show ip interface brief"))

    def push_config(self, lines: list[str], dry_run: bool = True) -> str:
        if dry_run:
            return "\n".join(lines)                        # show what would be sent; send nothing
        return self._conn.send_config_set(lines)

class FakeConn:
    def __init__(self, **kw):
        self.kw, self.sent = kw, []
    def send_command(self, cmd):
        return ("Interface IP-Address OK? Method Status Protocol\n"
                "Vlan10 192.168.10.2 YES manual up up\n"
                "Gi1/0/2 unassigned YES unset administratively down down\n")
    def send_config_set(self, lines):
        self.sent.append(lines)
        return "ok"

class DeviceTest(unittest.TestCase):
    def setUp(self):
        self.dev = Device("acc1", "10.255.0.21", connector=FakeConn)
        self.dev.connect(username="u", password="p")
    def test_parse(self):
        ifs = self.dev.get_interfaces()
        self.assertEqual(ifs["Gi1/0/2"]["status"], "administratively down")
        self.assertEqual(ifs["Vlan10"]["ip"], "192.168.10.2")
    def test_dry_run_sends_nothing(self):
        self.dev.push_config(["vlan 40"])
        self.assertEqual(self.dev._conn.sent, [])
    def test_real_push_sends_once(self):
        self.dev.push_config(["vlan 40"], dry_run=False)
        self.assertEqual(self.dev._conn.sent, [["vlan 40"]])

if __name__ == "__main__":
    unittest.main()
```

**Follow-ups.** Context-manager support and a `disconnect` in `finally`; `unittest.mock.patch("netmiko.ConnectHandler")` is the alternative to injection. **Mistakes.** Importing the library at module top so that tests need it; defaulting `dry_run` to `False`.
:::

::: q
### Q10.27 How do you handle secrets in automation repositories and CI?
[AMAZON · GOOGLE · MICROSOFT · TECH-2 · ■■■ · S]{.meta}

[30-second answer: never in Git. Keep credentials in a secrets manager or in CI-encrypted secrets, inject them as environment variables at run time, scope them to the minimum, prefer short-lived tokens, scan commits for keys, and rotate at once if one leaks.]{.short}

**Answer.** Layers: (i) `.gitignore` for `.env` and vault files; (ii) a pre-commit hook (`detect-secrets`) and a CI scan; (iii) Ansible Vault or HashiCorp Vault for stored values, with the vault password held by CI, not in the repository; (iv) a service account per pipeline with TACACS+ command authorisation limited to what the job needs, so that a leaked credential has a small reach ([9.12](#s9-12){.ref}); (v) masked variables so that logs do not print them; (vi) a documented rotation. A secret that reached history is considered public: rotate first, rewrite history second. **Mistakes.** Putting the password in the inventory "for the lab"; echoing environment variables in CI logs.
:::

::: q
### Q10.28 Explain GitOps for networks and drift detection.
[GOOGLE · AMAZON · CISCO · TECH-2 · ■■■ · T]{.meta}

[30-second answer: Git holds the intended state; only the pipeline holds device credentials; every change is a pull request. A scheduled job compares the devices with what Git renders; the difference is drift, which is reported or reconciled.]{.short}

**Answer.** The loop is: Git, pipeline, device, observation, back to Git. Drift arises from emergency CLI changes, failed pushes and software upgrades. The comparison renders the intended file and diffs it against `get_config` (the function in [10.13](#s10-13){.ref}), ignoring volatile lines. Policy decides the response: alert only, open a ticket, or re-apply the intended state at the next window. Reconciliation without review can overwrite a legitimate emergency fix, so many teams first raise a pull request that adopts or reverts the change. **Mistakes.** Auto-reconciling during an incident; comparing unnormalised text and drowning in false positives.
:::

::: q
### Q10.29 What is SDN? Where do OpenFlow and P4 fit, and what do hyperscalers run?
[GOOGLE · BROADCOM · MICROSOFT · TECH-2 · ■■■ · T]{.meta}

[30-second answer: SDN separates the control plane (decisions) from the data plane (forwarding) and exposes the network through software APIs. OpenFlow programs flow tables from a controller; P4 describes the forwarding pipeline itself. Hyperscalers mostly run BGP-based fabrics with central automation and telemetry.]{.short}

**Answer.** OpenFlow (2008 onward) gave controllers a way to install match-action rules, but table sizes and scale limited it in general networks. P4 programs the parser and match-action stages of a programmable ASIC, for new headers and in-network telemetry. In production, Google's WAN and data-centre work used custom controllers, and most hyperscaler data centres use eBGP underlays ([5.4](#s5-4){.ref}) with automation, intent verification and gNMI telemetry, so "SDN" in practice is software-driven operation more than OpenFlow ([5.7](#s5-7){.ref}). **Mistakes.** Equating SDN with OpenFlow.
:::

::: q
### Q10.30 A vendor has no API and a quirky CLI whose pager and prompts appear mid-output. Build a robust driver.
[AMAZON · CISCO · JUNIPER · TECH-2 · ■■■ · T]{.meta}

[30-second answer: write a small driver on Netmiko's base class around one function that sends a command and reads in a loop, answering the pager, accepting confirmations only from an allow-list, and returning only when the prompt regex matches at the end; give it a deadline, and test it with a fake channel.]{.short}

**Approach.** Never `sleep` a fixed time. Read in a loop with a short idle step; on each pass look only at the *tail* of the buffer. If it shows a pager marker send a space and delete the marker; if it shows a confirmation, answer only when the command is in an allow-list (an automatic `y` to `reload` would be dangerous); if a prompt ends the buffer, strip the echoed command and return. Use a monotonic clock for the deadline and raise on timeout. Injecting `write`, `read`, `sleep` and `now` makes the function testable.

```python
import re
import time

PROMPT = re.compile(r"[\w.\-]+(\(config[^)]*\))?[#>]\s*$")
MORE = re.compile(r"--More--|<--- More --->")
CONFIRM = re.compile(r"\[confirm\]|\(y/n\)\s*$", re.I)
SAFE_CONFIRM = {"clear counters", "copy running-config startup-config"}

def run_command(write, read, cmd, timeout=30.0, idle=0.2, sleep=time.sleep, now=time.monotonic):
    write(cmd + "\n")
    buf, deadline = "", now() + timeout
    while now() < deadline:
        sleep(idle)
        buf += read()
        tail = buf[-120:]
        if MORE.search(tail):
            buf = MORE.sub("", buf)
            write(" ")
        elif CONFIRM.search(tail):
            if cmd not in SAFE_CONFIRM:
                raise RuntimeError(f"unexpected confirmation for {cmd!r}")
            write("y\n")
            buf += "\n"
        elif PROMPT.search(buf.rstrip("\r\n").splitlines()[-1] if buf.strip() else ""):
            lines = buf.splitlines()
            return "\n".join(l for l in lines[1:-1])       # drop echoed command and final prompt
    raise TimeoutError(f"no prompt after {timeout}s for {cmd!r}: ...{buf[-60:]!r}")

# --- test with a scripted fake channel ------------------------------------------------------
chunks = iter(["show log\r\nline 1\r\n--More--", "line 2\r\n", "line 3\r\nsw1#"])
sent, clock = [], iter(range(100))
out = run_command(sent.append, lambda: next(chunks, ""), "show log",
                  sleep=lambda s: None, now=lambda: float(next(clock)))
assert sent == ["show log\n", " "], sent
assert out.splitlines() == ["line 1", "line 2", "line 3"], out
```

**Answer.** In a Netmiko subclass of `CiscoSSHConnection`, call `run_command(self.write_channel, self.read_channel, cmd)` from the method that replaces `send_command`, and put `terminal length 0` (or the vendor's equivalent) in `session_preparation` so the pager rarely appears. Add bounded retries on `TimeoutError` only for read-only commands. **Follow-ups.** Unknown prompts? Set the prompt regex per platform, learn the base prompt after login. **Mistakes.** `time.sleep(5)` after every command; auto-answering every confirmation; matching the prompt anywhere in the buffer, which a log line containing `#` will trigger.
:::

:::
:::

:::
