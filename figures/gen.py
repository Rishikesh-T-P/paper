#!/usr/bin/env python3
"""Generate the corrected secure distributed cloud-based MRAC diagram as SVG."""
import sys

W, H = 1100, 1240
out = []

def add(s):
    out.append(s)

def M(x, mirror):
    return W - x if mirror else x

def box(x, y, w, h, title, sub=None, dash=False, fill="#ffffff", bold=True):
    d = ' stroke-dasharray="7,5"' if dash else ''
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="#222" stroke-width="1.6"{d}/>')
    fw = "bold" if bold else "normal"
    if sub:
        add(f'<text x="{x+w/2}" y="{y+h/2-4}" text-anchor="middle" font-size="17" font-weight="{fw}">{title}</text>')
        add(f'<text x="{x+w/2}" y="{y+h/2+16}" text-anchor="middle" font-size="13" fill="#444">{sub}</text>')
    else:
        add(f'<text x="{x+w/2}" y="{y+h/2+6}" text-anchor="middle" font-size="17" font-weight="{fw}">{title}</text>')

def line(pts, arrow=True, color="#222", dash=False, width=1.6):
    p = " ".join(f"{x},{y}" for x, y in pts)
    a = f' marker-end="url(#ah{"r" if color != "#222" else ""})"' if arrow else ''
    d = ' stroke-dasharray="6,4"' if dash else ''
    add(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{width}"{a}{d}/>')

def dot(x, y, color="#222"):
    add(f'<circle cx="{x}" cy="{y}" r="4" fill="{color}"/>')

def lab(x, y, base, sub="", bar=True, hat=False, anchor="middle", color="#000", size=17):
    b = base + ("̂" if hat else "")
    deco = ' text-decoration="overline"' if bar else ''
    s = f'<tspan baseline-shift="sub" font-size="{int(size*0.7)}">{sub}</tspan>' if sub else ''
    add(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-style="italic" fill="{color}"><tspan{deco}>{b}</tspan>{s}</text>')

add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="DejaVu Serif, serif">')
add('<defs>'
    '<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#222"/></marker>'
    '<marker id="ahr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#c0392b"/></marker>'
    '</defs>')
add(f'<rect width="{W}" height="{H}" fill="#fff"/>')

RED = "#c0392b"  # corrected / newly added connections

# ---------------- Leader ----------------
box(390, 20, 320, 70, "Leader (0)", "reference model: ẋ₀ = Aₘx₀ + Bₘr")
box(510, 120, 80, 36, "Enc", fill="#eef5ff", bold=False)
line([(550, 90), (550, 120)])
lab(565, 112, "x", "0", bar=False, anchor="start", size=15)
line([(550, 156), (550, 250)], arrow=False, color=RED)
lab(565, 205, "x", "0", anchor="start", color=RED)

# ---------------- Cloud ----------------
add('<path d="M60,235 Q60,200 110,205 Q200,170 300,195 Q420,160 550,190 Q680,160 800,195 '
    'Q900,170 990,205 Q1040,200 1040,240 L1040,850 Q1040,880 1000,878 L100,878 Q60,880 60,850 Z" '
    'fill="#f7f7f7" stroke="#555" stroke-width="1.6"/>')
add('<text x="550" y="228" text-anchor="middle" font-size="14" fill="#555">Cloud (all signals encrypted)</text>')

# leader broadcast bus (pinned agents, g_i > 0)
line([(140, 250), (960, 250)], arrow=False, color=RED)
dot(550, 250, RED)

def node(mirror, idx):
    m = lambda x: M(x, mirror)
    # dashed node container
    x0 = min(m(75), m(495))
    add(f'<rect x="{x0}" y="275" width="420" height="560" rx="8" fill="none" stroke="#333" stroke-width="1.4" stroke-dasharray="7,5"/>')
    add(f'<text x="{m(285)}" y="295" text-anchor="middle" font-size="13" fill="#555">cloud node {idx}</text>')

    bx = min(m(160), m(360))
    box(bx, 315, 200, 60, "Observer")
    box(bx, 425, 200, 66, "Local error", "(neighbours + leader)")
    box(bx, 550, 200, 60, "Adaptive law")
    box(bx, 690, 200, 60, "Controller")

    s = "1" if idx == "1" else "N"
    # right side of block (towards graph link) for node 1 is x=360; left for mirror
    edge_in = m(360)   # inner edge (towards centre)
    edge_out = m(160)  # outer edge

    # --- observer -> x_hat bus
    line([(edge_in, 360), (m(400), 360)], arrow=False)
    lab(m(380) + (0 if not mirror else 0), 352, "x", s, hat=True)
    line([(m(400), 360), (m(400), 720)], arrow=False)
    for yy in (448, 580, 720):
        dot(m(400), yy)
        line([(m(400), yy), (edge_in, yy)])
    lab(m(420), 575, "x", s, hat=True, anchor="end" if mirror else "start", size=15)

    # --- x_hat_i exported to graph links (RED: new)
    dot(m(400), 400, RED)
    line([(m(400), 400), (m(515), 400)], color=RED)
    # --- neighbour estimates into local error (RED: new)
    line([(m(515), 472), (edge_in, 472)], color=RED)
    lab(m(470), 467, "x", "j", hat=True, color=RED, size=15)

    # --- leader state into local error (RED: new)
    line([(m(140), 250), (m(140), 458), (edge_out, 458)], color=RED)
    lab(m(133), 400, "x", "0", anchor="start" if mirror else "end", color=RED, size=15)
    lab(m(133), 420, "g", s, bar=False, anchor="start" if mirror else "end", color=RED, size=12)

    # --- error -> adaptive law, error -> controller (RED: new)
    line([(m(260), 491), (m(260), 550)], color=RED)
    lab(m(270), 527, "e", s, anchor="end" if mirror else "start", color=RED, size=15)
    dot(m(260), 520, RED)
    line([(m(260), 520), (m(145), 520), (m(145), 705), (edge_out, 705)], color=RED)
    lab(m(150), 690, "e", s, anchor="start" if not mirror else "end", color=RED, size=13)

    # --- adaptive law -> controller
    line([(m(300), 610), (m(300), 690)])
    lab(m(310), 655, "θ", s, hat=True, anchor="end" if mirror else "start")

    # --- reference r into adaptive law and controller
    line([(m(80), 640), (m(120), 640)], arrow=False)
    lab(m(90), 630, "r", "")
    line([(m(120), 580), (m(120), 735)], arrow=False)
    dot(m(120), 640)
    line([(m(120), 580), (edge_out, 580)])
    line([(m(120), 735), (edge_out, 735)])

    # --- controller output u (to agent via Dec)
    line([(m(260), 750), (m(260), 890)])
    lab(m(270), 790, "u", s, anchor="end" if mirror else "start")
    # u fed back to OBSERVER (RED: moved from adaptive law)
    dot(m(260), 810, RED)
    line([(m(260), 810), (m(450), 810), (m(450), 335), (edge_in, 335)], color=RED)
    lab(m(458), 330, "u", s, color=RED, anchor="end" if mirror else "start", size=15)

    # --- y from Enc into observer
    line([(m(95), 905), (m(95), 345), (edge_out, 345)])
    lab(m(103), 335, "y", s, anchor="end" if mirror else "start")

    # ---------------- Agent + Enc/Dec ----------------
    ax = min(m(150), m(370))
    box(ax, 980, 220, 70, f"Agent {s}", f"ẋ = Ax + B(u + θᵀφ(x)), y = Cx")
    dx = min(m(222), m(298))
    box(dx, 890, 76, 34, "Dec", fill="#eef5ff", bold=False)
    line([(m(260), 924), (m(260), 980)])
    lab(m(270), 960, "u", s, bar=False, anchor="end" if mirror else "start", size=15)
    ex = min(m(57), m(133))
    box(ex, 905, 76, 34, "Enc", fill="#eef5ff", bold=False)
    line([(min(m(150), m(370)) if not mirror else max(m(150), m(370)), 1015), (m(95), 1015), (m(95), 939)])
    lab(m(103), 1005, "y", s, bar=False, anchor="end" if mirror else "start", size=15)

node(False, "1")
node(True, "N")

# graph link block (neighbour exchange)
box(515, 380, 70, 110, "", fill="#fff4f2")
add(f'<text x="550" y="420" text-anchor="middle" font-size="13" fill="{RED}">graph</text>')
add(f'<text x="550" y="440" text-anchor="middle" font-size="16" font-style="italic" fill="{RED}">\U0001D4A2</text>')
add(f'<text x="550" y="460" text-anchor="middle" font-size="12" fill="{RED}">aᵢⱼ</text>')
add('<text x="550" y="600" text-anchor="middle" font-size="26">⋯</text>')
add('<text x="550" y="1020" text-anchor="middle" font-size="26">⋯</text>')

# legend
add('<text x="70" y="1110" font-size="14">Legend:  black = original connection (kept),  '
    f'<tspan fill="{RED}">red = added / corrected connection</tspan>;  '
    '<tspan font-style="italic" text-decoration="overline">z</tspan> = Enc(z), encrypted signal.</text>')
add('<text x="70" y="1135" font-size="14">g<tspan baseline-shift="sub" font-size="10">i</tspan> &gt; 0 only for agents pinned to the leader; '
    'a<tspan baseline-shift="sub" font-size="10">ij</tspan> &gt; 0 for neighbours j ∈ N<tspan baseline-shift="sub" font-size="10">i</tspan> in graph \U0001D4A2.</text>')
add('<text x="550" y="1195" text-anchor="middle" font-size="20" font-weight="bold">Secure distributed cloud-based MRAC architecture</text>')
add('</svg>')

open(sys.argv[1], "w").write("\n".join(out))
