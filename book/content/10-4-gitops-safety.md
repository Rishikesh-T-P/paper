::: {.p10}

## [10.13]{.sec}Git for network engineers [Must · ■□□]{.tag} {#s10-13}

*Git* is a distributed version-control system: it stores every version of a set of files, who changed them, when and why, and lets several people work on separate copies and merge them. It is the registrar's office for configuration: the old version is always retrievable and each change has a name against it. A *commit* is a saved snapshot with a message; a *branch* is a movable label on a line of commits; a *remote* is a shared copy (GitHub, GitLab) that people `push` to and `pull` from. For network work the repository holds the source of truth ([10.6](#s10-6){.ref}), the templates, the tests and the pipeline definition.

| Task | Command |
|---|---|
| Copy a repository | `git clone URL` |
| Start a change on a branch | `git switch -c feature/vlan-40` |
| See what changed | `git status`, `git diff` |
| Stage and save | `git add sot.yml` then `git commit -m "Add VLAN 40 (LAB) to acc1-acc3"` |
| Publish the branch | `git push -u origin feature/vlan-40` |
| Bring in others' work | `git fetch` (download only) then `git merge`; `git pull` is both |
| Undo a merged change | `git revert COMMIT` (adds a new commit that reverses it) |
| Label a release | `git tag -a v2026.10.29-1 -m "VLAN 40"` |

`git fetch` updates the local copy of the remote branches without touching the working files, so it is always safe; `git pull` is `fetch` followed by a merge, which may stop on a conflict. A `commit` records history locally; a `push` sends it to the remote. *Merge* joins two lines of history with a merge commit; *rebase* replays one branch's commits on top of another for a straight line. Either is acceptable provided the team agrees, and one never rebases commits that others already hold.

**The pull-request workflow** is how a change is reviewed before it can reach a device.

```
main     o---o-----------------M---o       tag v2026.10.29-1 on M
          \                   /
feature    o---o---o---------o             pipeline runs on every push to the branch
```

1. Create the branch `feature/vlan-40` and edit `sot.yml` (add VLAN 40 and ports).
2. Commit with a message that says what and why, and push.
3. Open a *pull request* (PR). The pipeline ([10.14](#s10-14){.ref}) lints, renders and tests, and posts the rendered diff as a comment.
4. A reviewer reads the YAML diff *and* the rendered configuration diff, and asks for changes or approves. A protected `main` branch refuses merges without a green pipeline and one approval.
5. Merge; the pipeline deploys. Tag the release so that "what was running last Tuesday" has an exact answer.

**Secrets.** A password committed to Git stays in the history even after the file is edited, and every clone has it; once committed, the only remedy is to *rotate* the secret. Hence `.gitignore` lists `*.vault`, `.env` and `backups/`; a pre-commit hook (`detect-secrets`, `git-secrets`) rejects commits that contain a key; and credentials are injected from the environment or a secrets manager at run time ([10.15](#s10-15){.ref}).

**GitOps** is the practice of making Git the only way to change the network. The repository states the intended configuration; the pipeline is the only actor with device credentials; and a scheduled job compares what the devices run with what Git says. The difference is *drift*, and finding it is as valuable as pushing changes.

```python
import difflib, pathlib
from napalm import get_network_driver

def drift(name: str, driver: str, host: str, user: str, pw: str) -> str:
    dev = get_network_driver(driver)(hostname=host, username=user, password=pw)
    dev.open()
    try:
        running = dev.get_config(retrieve="running")["running"].splitlines()
    finally:
        dev.close()
    intended = pathlib.Path(f"rendered/{name}.cfg").read_text().splitlines()
    return "\n".join(difflib.unified_diff(intended, running, "git", "device", lineterm=""))
```

A non-empty result raises a ticket (or, with approval, re-pushes the intended file). Real configurations contain lines the template does not own, such as certificates and timestamps, so a practical check ignores a list of patterns or compares sections only.

::: check
1. Why is `git revert` preferred to deleting a commit on a shared branch? [^c10-11]
2. A password was committed yesterday and the file was fixed today. Is it safe? [^c10-12]
:::

[^c10-11]: History that others have already pulled must not be rewritten; `revert` adds a new commit, so every clone stays consistent and the audit trail is kept.
[^c10-12]: No. The old commit still holds the password in every clone; rotate the secret, and then remove it from history if policy requires.

## [10.14]{.sec}CI/CD and testing for networks [Should · ■■□]{.tag} {#s10-14}

*Continuous integration* (CI) runs a fixed set of checks automatically on every change; *continuous delivery* (CD) carries a change that has passed those checks to the devices, with a human or a rule approving each gate. The principle is a mock exam before the board exam: a failure in the laboratory costs minutes, the same failure in production costs an outage.

<figure>
<svg viewBox="0 0 480 170" width="480"><defs><marker id="a141" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1A1D23"/></marker><marker id="a142" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs>
<rect class="box" x="6" y="30" width="58" height="34"/><text class="lbl" x="35" y="45" text-anchor="middle">Pull</text><text class="lbl" x="35" y="56" text-anchor="middle">request</text>
<rect class="box" x="84" y="30" width="48" height="34"/><text class="lbl" x="108" y="51" text-anchor="middle">Lint</text>
<rect class="box" x="152" y="30" width="48" height="34"/><text class="lbl" x="176" y="51" text-anchor="middle">Render</text>
<rect class="box" x="220" y="30" width="60" height="34"/><text class="lbl" x="250" y="45" text-anchor="middle">Lab</text><text class="lbl" x="250" y="56" text-anchor="middle">test</text>
<rect class="fill" x="300" y="30" width="56" height="34" stroke="#83469A"/><text class="lbl" x="328" y="45" text-anchor="middle">Approve</text><text class="sm" x="328" y="56" text-anchor="middle">gate</text>
<rect class="box" x="376" y="30" width="50" height="34"/><text class="lbl" x="401" y="45" text-anchor="middle">Canary</text><text class="sm" x="401" y="56" text-anchor="middle">1 device</text>
<rect class="box" x="436" y="30" width="38" height="34"/><text class="lbl" x="455" y="51" text-anchor="middle">Rest</text>
<line class="ln" x1="64" y1="47" x2="82" y2="47" marker-end="url(#a141)"/><line class="ln" x1="132" y1="47" x2="150" y2="47" marker-end="url(#a141)"/><line class="ln" x1="200" y1="47" x2="218" y2="47" marker-end="url(#a141)"/><line class="ln" x1="280" y1="47" x2="298" y2="47" marker-end="url(#a141)"/><line class="ln" x1="356" y1="47" x2="374" y2="47" marker-end="url(#a141)"/><line class="ln" x1="426" y1="47" x2="434" y2="47" marker-end="url(#a141)"/>
<text class="sm" x="108" y="80" text-anchor="middle">yamllint, ruff</text><text class="sm" x="176" y="80" text-anchor="middle">schema, pytest,</text><text class="sm" x="176" y="90" text-anchor="middle">diff artefact</text><text class="sm" x="250" y="80" text-anchor="middle">containerlab,</text><text class="sm" x="250" y="90" text-anchor="middle">Batfish, ping</text><text class="sm" x="328" y="80" text-anchor="middle">human review</text><text class="sm" x="428" y="80" text-anchor="middle">post-checks</text>
<rect class="box" x="6" y="118" width="468" height="30" rx="8" style="stroke-dasharray:3 3"/><text class="lbl" x="240" y="136" text-anchor="middle">Devices → telemetry and drift job → alert or new pull request</text>
<path class="acc" d="M455 66 L455 116" fill="none" marker-end="url(#a142)"/><path class="acc" d="M35 116 L35 66" fill="none" marker-end="url(#a142)"/>
<text class="sm" x="240" y="164" text-anchor="middle">A failed stage stops the line and the change goes back to its author; Git holds the intent throughout.</text>
</svg>
<figcaption><b>Figure 10.4</b> The GitOps pipeline. Gates fail cheaply early; the loop at the bottom closes the ladder of Figure 10.1.</figcaption>
</figure>

**Stages and what each catches.**

| Stage | Tool | Catches |
|---|---|---|
| Lint | `yamllint`, `ansible-lint`, `ruff` | syntax, style, deprecated modules |
| Schema | `jsonschema`, `pydantic` | wrong types, out-of-range VLANs, missing keys |
| Unit test | `pytest` on rendered text | a template that drops a line |
| Static analysis | Batfish | routing and ACL errors across the whole network, offline |
| Lab test | containerlab + pyATS or scripts | behaviour: sessions, reachability |
| Approval | protected environment | the human decision |
| Post-check | pyATS, NAPALM `compliance_report` | the change harmed something |

A unit test on the rendered output is cheap and needs no device. The test below fails the pull request if any rendered access port lacks `no shutdown`.

```python
import pathlib, re
import pytest

CONFIGS = sorted(pathlib.Path("rendered").glob("acc*.cfg"))

@pytest.mark.parametrize("cfg", CONFIGS, ids=lambda p: p.stem)
def test_every_access_port_is_enabled(cfg):
    blocks = re.split(r"(?m)^interface ", cfg.read_text())[1:]
    for block in blocks:
        if "switchport mode access" in block:
            assert " no shutdown" in block, f"{cfg.stem}: {block.splitlines()[0]} stays shut"
```

*Batfish* builds a model of the network from the configuration files alone and answers questions without any device or packet. It finds undefined references, unreachable prefixes and ACLs that block what they should not, and so it checks a change *before* it exists on a device.

```python
from pybatfish.client.session import Session
from pybatfish.datamodel import HeaderConstraints

bf = Session(host="localhost")
bf.set_network("campus")
bf.init_snapshot("snapshots/candidate", name="candidate", overwrite=True)
missing = bf.q.undefinedReferences().answer().frame()
assert missing.empty, missing                       # an ACL or route-map name that does not exist
flow = bf.q.testFilters(headers=HeaderConstraints(srcIps="192.168.30.10", dstIps="192.168.10.5",
                                                   applications="https"), nodes="dist1").answer().frame()
assert (flow["Action"] == "DENIED").all(), "GUEST must not reach SALES"
```

The **lab test** builds a *digital twin*, a small copy of the topology in containers, so the real configuration is applied to something that behaves like the network. *Containerlab* describes the topology in YAML and starts cEOS, FRR and Linux containers in seconds.

```
# lab/campus.clab.yml
name: campus
topology:
  nodes:
    leaf1:  {kind: ceos,  image: ceos:4.32.0F}
    leaf2:  {kind: ceos,  image: ceos:4.32.0F}
    spine1: {kind: linux, image: quay.io/frrouting/frr:9.1.0}
  links:
    - endpoints: ["leaf1:eth1", "spine1:eth1"]
    - endpoints: ["leaf2:eth1", "spine1:eth2"]
```

The pipeline, in GitHub Actions syntax, chains the stages with `needs`; the `production` environment is configured in the repository to require a named approver, which is the gate of Figure 10.4.

```
# .github/workflows/network.yml
name: network-ci
on: {pull_request: {}, push: {branches: [main]}}
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install yamllint ruff && yamllint sot.yml && ruff check .
  render:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt && python render.py && pytest -q tests/unit
      - uses: actions/upload-artifact@v4
        with: {name: rendered, path: rendered/}
  lab-test:
    needs: render
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with: {name: rendered, path: rendered/}
      - run: sudo containerlab deploy -t lab/campus.clab.yml
      - run: python tests/push_and_check.py
      - if: always()
        run: sudo containerlab destroy -t lab/campus.clab.yml --cleanup
  deploy:
    if: github.ref == 'refs/heads/main'
    needs: lab-test
    environment: production
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4
      - run: python deploy.py --canary leaf1 --then-rest
        env: {NET_USER: "${{ secrets.NET_USER }}", NET_PASS: "${{ secrets.NET_PASS }}"}
```

::: example
**A pull request that the lab catches.** A reviewer-approved change to `access_switch.j2` tidies the port block and, by accident, deletes the line ` no shutdown`.

1. The linter and the schema check pass, because the YAML data are unchanged and the template is syntactically valid.
2. The unit test of the previous listing fails on `acc1`: `acc1: GigabitEthernet1/0/1 stays shut`. The pull request is blocked before the lab starts.
3. Suppose that test did not exist. The lab test pushes the configuration to a cEOS host-facing port and its ping from host `h1` to `h2` fails: `0 received, 100% packet loss`. The job fails and `deploy` never runs.

[Result: the defect is found in a container, at the cost of a failed pull request, rather than on thirty access ports on a Monday morning.]{.result}
:::

**Pre- and post-checks.** Before the push the script records a baseline, and after it compares; the comparison is the proof that the change did what was intended and nothing else.

| Check | Before | After | Verdict rule |
|---|---|---|---|
| BGP sessions established | 4 | 4 | must be equal |
| Routes in the global table | 128 | 128 | within ±2 |
| Interfaces up | 24 | 24 | equal, except the one changed |
| Reachability matrix (ping) | all 12 pairs | all 12 pairs | no pair lost |
| Config lines changed | | 3 | equals the reviewed diff |

If any rule fails, the script rolls back ([10.15](#s10-15){.ref}) and exits with an error. Such a pre/post framework is what Cisco's *pyATS* provides: `pre = dev.learn("bgp")` and `post = dev.learn("bgp")` return structured snapshots, and `Diff(pre.info, post.info)` prints only the differences.

::: lens
[CISCO · AMAZON · GOOGLE · ARISTA]{.co}

"What would you put in a CI pipeline for network changes?" The strong answer lists stages in order with the defect each one catches (lint, schema, unit tests, Batfish, digital-twin test, approval, canary, post-check, rollback) and says which stages are cheap and run on every push. A follow-up is "how do you test what you cannot emulate?": hardware features such as ASIC limits and optics are covered by the canary and the post-check, not by the lab.
:::

## [10.15]{.sec}Safety at scale, and the platforms you will meet [Optional · ■■□]{.tag} {#s10-15}

Automation raises the speed of a mistake as well as the speed of a fix, so the safety design matters more than the tool. The principles are few and each answers a way things go wrong.

| Control | Meaning | Prevents |
|---|---|---|
| Idempotence | applying twice equals applying once | duplicate or oscillating changes after a retry |
| Dry run and diff | compute the change, show it, apply nothing | surprises; the reviewer sees the lines |
| Approval gate | a person accepts the diff | an unreviewed change reaching production |
| Canary and waves | one device, then a few, then the rest, with a pause and a check between | a defect hitting everything at once |
| Pre/post-check | measure state before and after | silent damage |
| Automatic rollback | revert when a check fails or access is lost | a long outage after a bad push |
| Concurrency cap | limit simultaneous sessions (for example 8) | overload of AAA servers and device control planes |
| Secrets management | credentials from a vault or CI secret; short-lived where possible | credentials in Git or in logs |
| Audit log | who, what, when, from which commit | an unanswerable post-mortem |

**Rollback** has to work *without* the network the change may have broken. On IOS, `reload in 10` before the change and `reload cancel` after a successful check restore the saved configuration if the device becomes unreachable; EOS has `commit timer 00:10:00` in a configuration session, Junos has `commit confirmed`, and NETCONF has a confirmed-commit ([10.11](#s10-11){.ref}). A NAPALM `rollback()` needs a reachable device, and so cannot rescue the change that cut the path.

**Waves.** A rollout is a sequence of groups with a soak time and a gate between them. For Campus Net's 40 access switches a plan might be:

| Wave | Targets | Soak | Gate to continue |
|---|---|---|---|
| 0 | lab twin | — | CI green |
| 1 | `acc1` (canary) | 10 min | post-checks pass, no new alarms |
| 2 | 4 switches in one building | 15 min | same, plus error counters flat |
| 3 | 10 % of the rest | 15 min | same |
| 4 | remainder, in groups of 10 | 5 min each | same; stop at first failure |

::: example
**A story with five lessons.** A script was run against 120 branch routers. The template had been edited so that the default-route line was dropped, and the script's thread pool was unbounded. It opened 120 sessions at once, took out the TACACS+ server, pushed a configuration that removed `ip route 0.0.0.0 0.0.0.0` and saved it. The branches could not be reached to repair them.

1. *Diff review.* A dry-run diff would have shown `- ip route 0.0.0.0 0.0.0.0 …` on the first device; a rule "refuse any diff that removes a route or more than N lines" would have stopped the run mechanically.
2. *Canary.* The first wave of one router would have lost its default route alone.
3. *Post-check with automatic rollback.* A reachability check from the management system to the router's loopback, with `reload in 10` armed, restores the saved configuration if the check fails.
4. *Concurrency cap.* Eight workers would not have overloaded AAA, and the failure would not have blocked emergency logins.
5. *Save only after verification.* Writing to NVRAM only after the post-check passed means a reload returns the old, working configuration.

[Result: any one of the five contains the damage to one router; together they make this class of incident close to impossible.]{.result}
:::

**Platforms.** Some vendors offer a controller with its own API, so a script talks to the controller rather than to each device. Knowing the names lets one place a platform in a conversation.

| Platform | Vendor | Interface | Role |
|---|---|---|---|
| Catalyst Center (DNA Center) | Cisco | REST, intent API | campus automation and assurance |
| Meraki Dashboard | Cisco | REST (cloud) | cloud-managed access and security |
| CloudVision | Arista | gRPC, REST, Python | change control and telemetry for EOS |
| Junos PyEZ, Apstra | Juniper | NETCONF-based Python library; intent-based data-centre controller | Junos automation |
| NX-API | Cisco | JSON-RPC over HTTP on Nexus | scripting Nexus switches |
| SONiC | open source | Redis, gNMI, REST | the switch OS of several hyperscalers |

*Software-defined networking* separates the control plane from the data plane ([5.7](#s5-7){.ref}); OpenFlow was the first protocol to program forwarding tables directly, P4 describes the forwarding pipeline itself, and in practice the hyperscalers run standard BGP with custom automation and telemetry rather than a central OpenFlow controller. Credentials and key handling in the automation system follow the rules of [9.12](#s9-12){.ref} and [9.13](#s9-13){.ref}; for the live operation of a network that automation has broken, the method of [11.1](#s11-1){.ref} applies.

::: trap
*Claim:* "The script worked in the lab, so it is safe to run on everything." *Why it is wrong:* the lab has no TACACS+ load, no old software release, no device with a hand-made exception and no human traffic. *Correct statement:* production access to a change is earned in waves, with a gate between each, and the first production device is the first real test.
:::

:::
