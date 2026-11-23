"""Generate teaser SVGs (320x200): SIMPLE-C, MSTNet, ICMASS 2025, ICECET 2023, Formula Student,
harbor navigation and inland vessel trajectory prediction.

Usage: python3 scripts/paper-thumbnails.py public/images/publications
"""
import math, random, sys
OUT = sys.argv[1]
# Monochrome + single orange accent, matching the site
BLUE, ORANGE, FG, MUTED = '#b4bac2', '#fd7422', '#ededed', '#6b6f75'

def hull(cx, cy, L, W, ang, **kw):
    # ship outline pointing +x, rotated by ang (deg)
    pts = [(-L/2, -W/2), (L*0.22, -W/2), (L/2, 0), (L*0.22, W/2), (-L/2, W/2)]
    a = math.radians(ang)
    p = [(cx + x*math.cos(a) - y*math.sin(a), cy + x*math.sin(a) + y*math.cos(a)) for x, y in pts]
    attrs = ' '.join(f'{k.replace("_","-")}="{v}"' for k, v in kw.items())
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in p)}" {attrs}/>'

# ---------------------------------------------------------------- ICMASS
def icmass():
    s = []
    s.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="640" height="400">')
    s.append('<defs><radialGradient id="w" cx="45%" cy="60%" r="80%"><stop offset="0" stop-color="#141517"/><stop offset="1" stop-color="#050505"/></radialGradient>'
             f'<radialGradient id="fov" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{ORANGE}" stop-opacity=".22"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>'
             '<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#2a2f37" stroke-width="2"/></pattern></defs>')
    s.append('<rect width="320" height="200" fill="url(#w)"/>')
    # land / quays (harbor basin)
    land = '#15181d'
    s.append(f'<path d="M0 0 H320 V38 H210 L196 52 H120 V30 H0 Z" fill="{land}"/>')
    s.append(f'<path d="M0 30 H120 V52 H58 V200 H0 Z" fill="{land}"/>')
    s.append(f'<path d="M260 200 V150 L290 138 H320 V200 Z" fill="{land}"/>')
    for d in ['M0 30 H120 V52 H58 V200', 'M320 38 H210 L196 52 H120', 'M260 200 V150 L290 138 H320']:
        s.append(f'<path d="{d}" fill="none" stroke="#3a414c" stroke-width="1.2"/>')
    s.append('<rect x="0" y="0" width="58" height="200" fill="url(#hatch)" opacity=".5"/>')
    # moored ships detected as static convex obstacles
    s.append(hull(140, 61, 34, 9, 0, fill='#2a2f37'))
    s.append(f'<polygon points="121,55 158,55 160,61 158,67 121,67" fill="none" stroke="{ORANGE}" stroke-width="1.3" stroke-dasharray="2.5 1.5"/>')
    s.append(hull(70, 120, 30, 8, 90, fill='#2a2f37'))
    s.append(f'<polygon points="64,104 76,104 76,136 70,137 64,136" fill="none" stroke="{ORANGE}" stroke-width="1.3" stroke-dasharray="2.5 1.5"/>')
    # ego vessel (Deneb) sensor field of view
    ex, ey = 118, 150
    s.append(f'<circle cx="{ex}" cy="{ey}" r="70" fill="url(#fov)"/>')
    for r in (22, 40, 58):
        s.append(f'<circle cx="{ex}" cy="{ey}" r="{r}" fill="none" stroke="{ORANGE}" stroke-opacity=".18" stroke-width=".6"/>')
    # lidar points on quay walls inside fov
    random.seed(3)
    for _ in range(140):
        a = random.uniform(0, 2*math.pi); r = random.uniform(10, 60)
        x, y = ex + r*math.cos(a), ey + r*math.sin(a)
        on_wall = (abs(x-58) < 2.2 and y > 52) or (abs(y-52) < 2.2 and 58 < x < 196) or (abs(x-120) < 2 and y < 52)
        if on_wall:
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r=".8" fill="{ORANGE}" opacity=".85"/>')
    for i in range(60):
        y = 60 + i*2.3
        if math.hypot(58-ex, y-ey) < 62:
            s.append(f'<circle cx="{58+random.uniform(-.6,.6):.1f}" cy="{y:.1f}" r="1.1" fill="{ORANGE}" opacity=".85"/>')
    for i in range(70):
        x = 70 + i*1.9
        if math.hypot(x-ex, 52-ey) < 62:
            s.append(f'<circle cx="{x:.1f}" cy="{52+random.uniform(-.6,.6):.1f}" r="1.1" fill="{ORANGE}" opacity=".85"/>')
    # planned trajectories
    s.append(f'<path d="M{ex+17} {ey} C 175 150, 200 120, 236 100 S 290 78, 312 76" fill="none" stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    s.append(f'<path d="M262 116 C 230 124, 190 112, 170 96 S 120 86, 92 84" fill="none" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    s.append(f'<path d="M300 170 C 270 172, 240 166, 220 150" fill="none" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="2 3" opacity=".7"/>')
    # vessels
    s.append(hull(ex, ey, 42, 12, 0, fill=ORANGE))
    s.append(hull(276, 113, 26, 8, 190, fill=BLUE))
    s.append(hull(306, 170, 22, 7, 180, fill='none', stroke=BLUE, stroke_width='1.2', stroke_dasharray='2 1.5'))
    # communication links to shore-based central planner
    px, py = 236, 20
    s.append(f'<g stroke="{FG}" stroke-opacity=".55" stroke-width=".8" stroke-dasharray="1 2.5" fill="none">'
             f'<path d="M{px} {py+8} L{ex} {ey-8}"/><path d="M{px} {py+8} L276 106"/><path d="M{px} {py+8} L304 164"/></g>')
    s.append(f'<g fill="none" stroke="{FG}" stroke-width="1.1" stroke-linecap="round"><path d="M{px} {py+9} V{py-2}"/>'
             f'<path d="M{px-5} {py-6} a7 7 0 0 0 0 9"/><path d="M{px+5} {py-6} a7 7 0 0 1 0 9"/>'
             f'<path d="M{px-9} {py-9} a12 12 0 0 0 0 15"/><path d="M{px+9} {py-9} a12 12 0 0 1 0 15"/></g>')
    s.append(f'<circle cx="{px}" cy="{py-3}" r="1.8" fill="{FG}"/>')
    s.append('</svg>')
    return '\n'.join(s)

# ---------------------------------------------------------------- ICECET
def icecet():
    random.seed(11)
    s = []
    s.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="640" height="400">')
    s.append('<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d0e0f"/><stop offset="1" stop-color="#030303"/></linearGradient></defs>')
    s.append('<rect width="320" height="200" fill="url(#bg)"/>')

    def scene(dx):
        """A BEV lidar scan in local coords (0..150 x 0..100), ego at (20,50) driving +x."""
        pts = []
        for i in range(70):                     # road edges / curbs
            x = i * 2.2 - dx
            if 0 <= x <= 150:
                pts.append((x, 20 + random.uniform(-.7, .7), 'road'))
                pts.append((x, 80 + random.uniform(-.7, .7), 'road'))
        for ring in (26, 52):       # ground rings
            for k in range(0, 360, 9):
                a = math.radians(k)
                x, y = 20 + ring*math.cos(a), 50 + ring*0.85*math.sin(a)
                if 0 <= x <= 150 and 22 < y < 78:
                    pts.append((x, y, 'ring'))
        cx, cy = 96 - dx*0.4, 40                # car ahead
        for _ in range(45):
            pts.append((cx + random.uniform(-9, 9), cy + random.choice([-4, 4]) + random.uniform(-.6, .6), 'car'))
            pts.append((cx - 9 + random.uniform(-.6, .6), cy + random.uniform(-4, 4), 'car'))
        ox, oy = 62 - dx*0.4, 64                # second vehicle
        for _ in range(25):
            pts.append((ox + random.uniform(-7, 7), oy - 3.5 + random.uniform(-.5, .5), 'car2'))
        for _ in range(70):                     # rain / fog clutter near the sensor
            r = abs(random.gauss(0, 18)); a = random.uniform(0, 2*math.pi)
            x, y = 20 + r*math.cos(a), 50 + r*math.sin(a)
            if 0 <= x <= 150 and 0 <= y <= 100:
                pts.append((x, y, 'noise'))
        return pts, (cx, cy)

    # frames back to front: t-4k ... t ; skipped frames dashed & empty
    frames = [(-4, True), (-3, False), (-2, True), (-1, False), (0, True)]
    M = 'matrix(1.22 0 0.62 0.6 0 0)'
    for idx, (k, used) in enumerate(frames):
        ox, oy = 36 - idx*8, 16 + idx*28
        op = 0.35 + 0.65 * (idx / 4)
        s.append(f'<g transform="translate({ox} {oy}) {M}" opacity="{op:.2f}">')
        if used:
            s.append(f'<rect width="150" height="100" fill="#0b0c0d" stroke="{BLUE}" stroke-opacity=".5" stroke-width="1.2"/>')
            pts, (cx, cy) = scene(-k * 6)
            for x, y, kind in pts:
                col = {'road': BLUE, 'ring': '#34383d', 'car': FG, 'car2': FG, 'noise': '#7c8794'}[kind]
                r = 1.7 if kind in ('car', 'car2') else 1.25
                o = .55 if kind == 'noise' else .9
                s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}" opacity="{o}"/>')
            if k == 0:
                s.append(f'<rect x="{cx-11:.1f}" y="{cy-6:.1f}" width="22" height="12" fill="{ORANGE}" fill-opacity=".12" stroke="{ORANGE}" stroke-width="2.6"/>')
                s.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx+11:.1f}" y2="{cy:.1f}" stroke="{ORANGE}" stroke-width="1.6"/>')
                s.append(f'<rect x="{62-9:.1f}" y="{64-6:.1f}" width="18" height="11" fill="none" stroke="{ORANGE}" stroke-width="2.2" stroke-opacity=".85"/>')
            s.append(f'<polygon points="13,44 27,50 13,56" fill="{ORANGE}"/>')
        else:
            s.append(f'<rect width="150" height="100" fill="none" stroke="{MUTED}" stroke-opacity=".6" stroke-width="1" stroke-dasharray="4 4"/>')
        s.append('</g>')
    # time axis with skipped frames
    ax = 303
    s.append(f'<line x1="{ax}" y1="30" x2="{ax}" y2="176" stroke="{MUTED}" stroke-width="1"/>')
    s.append(f'<polygon points="{ax-3},174 {ax+3},174 {ax},181" fill="{MUTED}"/>')
    for idx, (k, used) in enumerate(frames):
        y = 33 + idx*28
        if used:
            s.append(f'<circle cx="{ax}" cy="{y}" r="4" fill="{ORANGE if k == 0 else BLUE}"/>')
        else:
            s.append(f'<circle cx="{ax}" cy="{y}" r="3.5" fill="#050505" stroke="{MUTED}" stroke-dasharray="1.5 1.5"/>')
    s.append(f'<text x="{ax-9}" y="{33+4*28+4}" text-anchor="end" font-family="Helvetica, Arial, sans-serif" font-size="10" font-weight="700" fill="{ORANGE}">t</text>')
    # rain streaks over everything
    for _ in range(46):
        x, y = random.uniform(0, 300), random.uniform(-10, 190); l = random.uniform(6, 12)
        s.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x-l*0.35:.1f}" y2="{y+l:.1f}" stroke="#c8ccd2" stroke-opacity="{random.uniform(.15,.4):.2f}" stroke-width=".8" stroke-linecap="round"/>')
    s.append('</svg>')
    return '\n'.join(s)

# ---------------------------------------------------------------- SIMPLE-C
def simplec():
    random.seed(5)
    s = []
    s.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="640" height="400">')
    s.append('<defs><radialGradient id="sw" cx="60%" cy="45%" r="85%"><stop offset="0" stop-color="#141517"/><stop offset="1" stop-color="#050505"/></radialGradient></defs>')
    s.append('<rect width="320" height="200" fill="url(#sw)"/>')
    # subtle waves
    for k in range(9):
        y = 18 + k*20
        s.append(f'<path d="M150 {y} q 8 -3 16 0 t 16 0 t 16 0 t 16 0 t 16 0 t 16 0 t 16 0 t 16 0 t 16 0" fill="none" stroke="#1f2226" stroke-width=".8" opacity=".7"/>')
    # quay at the bottom-left and the docked vessel (bow pointing right)
    s.append('<path d="M0 178 H150 V200 H0 Z" fill="#15181d"/><path d="M0 178 H150" stroke="#3a414c" stroke-width="1.2"/>')
    s.append('<path d="M-10 118 H70 C 100 118, 120 136, 132 150 C 120 164, 100 176, 70 176 H-10 Z" fill="#2a2f37" stroke="#4a525e" stroke-width="1"/>')
    s.append('<path d="M-10 132 H62 M-10 162 H62" stroke="#3a414c" stroke-width=".8"/>')
    l1, l2 = (112, 128), (112, 172)
    # fields of view (overlapping wedges)
    def wedge(cx, cy, a0, a1, r, col, op):
        a0, a1 = math.radians(a0), math.radians(a1)
        x0, y0 = cx + r*math.cos(a0), cy + r*math.sin(a0)
        x1, y1 = cx + r*math.cos(a1), cy + r*math.sin(a1)
        return f'<path d="M{cx} {cy} L{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f} Z" fill="{col}" fill-opacity="{op}" stroke="{col}" stroke-opacity=".35" stroke-width=".8"/>'
    s.append(wedge(*l1, -70, 25, 175, BLUE, .10))
    s.append(wedge(*l2, -25, 70, 175, ORANGE, .10))
    # target trajectory as seen by each LiDAR (misaligned copies)
    traj = [(200 + 70*math.cos(t)*0.9, 100 + 46*math.sin(t*1.0)) for t in [i*0.09 for i in range(-14, 18)]]
    ang, tx, ty = math.radians(9), 10, -12
    rot = [(205 + (x-205)*math.cos(ang) - (y-100)*math.sin(ang) + tx, 100 + (x-205)*math.sin(ang) + (y-100)*math.cos(ang) + ty) for x, y in traj]
    for x, y in rot:
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="{BLUE}" opacity=".9"/>')
    for x, y in traj:
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="{ORANGE}" opacity=".95"/>')
    # transform arrow R, t
    s.append(f'<path d="M262 70 C 286 74, 292 96, 280 112" fill="none" stroke="{FG}" stroke-width="1.3" marker-end="url(#ah)"/>')
    s.append(f'<defs><marker id="ah" viewBox="0 0 8 8" refX="6" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="{FG}"/></marker></defs>')
    s.append(f'<text x="292" y="94" font-family="Georgia, serif" font-style="italic" font-size="13" fill="{FG}">R, t</text>')
    # the reflective target (warning vest) at the end of the trajectory
    vx, vy = traj[-1]
    vx, vy = vx + 4, vy + 14
    s.append(f'<g transform="translate({vx:.1f} {vy:.1f})"><path d="M-7 -9 L-3 -9 L0 -5 L3 -9 L7 -9 L10 -4 L7 -2 L7 9 L-7 9 L-7 -2 L-10 -4 Z" fill="#ededed" stroke="#050505" stroke-width=".6"/>'
             '<path d="M-7 1 H7 M-7 5 H7" stroke="#fd7422" stroke-width="1.6"/></g>')
    # LiDAR sensors
    for (x, y), col in ((l1, BLUE), (l2, ORANGE)):
        s.append(f'<rect x="{x-4}" y="{y-4}" width="8" height="8" rx="2" fill="#050505" stroke="{col}" stroke-width="2"/>')
    s.append('</svg>')
    return '\n'.join(s)

# ---------------------------------------------------------------- MSTNet
def mstnet():
    random.seed(21)
    s = []
    s.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="640" height="400">')
    s.append('<defs><linearGradient id="mb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d0e0f"/><stop offset="1" stop-color="#030303"/></linearGradient>'
             '<pattern id="mh" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="4" stroke="#3b4048" stroke-width="1.6"/></pattern>'
             f'<marker id="ma" viewBox="0 0 8 8" refX="6" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="{MUTED}"/></marker></defs>')
    s.append('<rect width="320" height="200" fill="url(#mb)"/>')

    def vessels():
        out = []
        for (cx, cy, L, W, a) in [(46, 50, 34, 11, -12), (78, 112, 44, 13, 18), (30, 150, 26, 9, -4)]:
            ar = math.radians(a)
            for _ in range(int(L*1.6)):
                u, v = random.uniform(-L/2, L/2), random.choice([-W/2, W/2]) + random.uniform(-.8, .8)
                if random.random() < .35: u, v = random.choice([-L/2, L/2]), random.uniform(-W/2, W/2)
                out.append((cx + u*math.cos(ar) - v*math.sin(ar), cy + u*math.sin(ar) + v*math.cos(ar)))
        return out

    # left panel: unlabeled scan on a voxel grid with masked voxels
    px, py, pw, ph = 12, 22, 108, 156
    s.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6" fill="#0b0c0d" stroke="#34383d" stroke-width="1"/>')
    g = 12
    pts = [(x, y) for x, y in vessels() if px < x < px+pw and py < y < py+ph]
    occupied = {(int((x-px)//g), int((y-py)//g)) for x, y in pts}
    masked = {c for c in occupied if random.random() < .45}
    for i in range(1, pw//g + 1):
        s.append(f'<line x1="{px+i*g}" y1="{py}" x2="{px+i*g}" y2="{py+ph}" stroke="#1f2226" stroke-width=".5"/>')
    for j in range(1, ph//g + 1):
        s.append(f'<line x1="{px}" y1="{py+j*g}" x2="{px+pw}" y2="{py+j*g}" stroke="#1f2226" stroke-width=".5"/>')
    for (i, j) in masked:
        s.append(f'<rect x="{px+i*g}" y="{py+j*g}" width="{g}" height="{g}" fill="url(#mh)" stroke="{ORANGE}" stroke-opacity=".7" stroke-width=".8"/>')
    for x, y in pts:
        c = (int((x-px)//g), int((y-py)//g))
        if c not in masked:
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.3" fill="{BLUE}"/>')
    # middle: encoder (sparse transformer stack)
    s.append(f'<path d="M124 100 H140" stroke="{MUTED}" stroke-width="1.4" marker-end="url(#ma)"/>')
    for k in range(4):
        x = 146 + k*7
        h = 92 - k*14
        s.append(f'<rect x="{x}" y="{100-h/2}" width="5" height="{h}" rx="2" fill="{FG}" fill-opacity="{.25+.15*k}"/>')
    s.append(f'<path d="M178 100 H194" stroke="{MUTED}" stroke-width="1.4" marker-end="url(#ma)"/>')
    # right panel: detections with oriented boxes
    rx = 198
    s.append(f'<rect x="{rx}" y="{py}" width="{pw}" height="{ph}" rx="6" fill="#0b0c0d" stroke="#34383d" stroke-width="1"/>')
    random.seed(21)
    for x, y in vessels():
        if px < x < px+pw and py < y < py+ph:
            s.append(f'<circle cx="{x-px+rx:.1f}" cy="{y:.1f}" r="1.3" fill="{BLUE}"/>')
    for (cx, cy, L, W, a) in [(46, 50, 34, 11, -12), (78, 112, 44, 13, 18), (30, 150, 26, 9, -4)]:
        cx = cx - px + rx
        s.append(f'<g transform="translate({cx} {cy}) rotate({a})"><rect x="{-L/2-3}" y="{-W/2-3}" width="{L+6}" height="{W+6}" fill="{ORANGE}" fill-opacity=".12" stroke="{ORANGE}" stroke-width="1.8"/>'
                 f'<line x1="0" y1="0" x2="{L/2+3}" y2="0" stroke="{ORANGE}" stroke-width="1.6"/></g>')
    # label-efficiency inset: AP vs. labels (pretrained above scratch)
    ix, iy, iw, ih = rx + 54, 152, 46, 20
    s.append(f'<path d="M{ix} {iy+ih} H{ix+iw} M{ix} {iy+ih} V{iy}" stroke="{MUTED}" stroke-width=".8"/>')
    s.append(f'<path d="M{ix} {iy+ih-6} C {ix+12} {iy+3}, {ix+40} {iy+1}, {ix+iw} {iy}" fill="none" stroke="{ORANGE}" stroke-width="1.6"/>')
    s.append(f'<path d="M{ix} {iy+ih} C {ix+30} {iy+ih-4}, {ix+50} {iy+8}, {ix+iw} {iy+4}" fill="none" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="3 2"/>')
    s.append('</svg>')
    return '\n'.join(s)

# ---------------------------------------------------------------- Formula Student (electric powertrain)
def formula_student():
    s = []
    s.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="640" height="400">')
    s.append('<defs><pattern id="fg" width="16" height="16" patternUnits="userSpaceOnUse"><path d="M16 0H0V16" fill="none" stroke="#1a1c1f" stroke-width=".8"/></pattern></defs>')
    s.append('<rect width="320" height="200" fill="#050505"/><rect width="320" height="200" fill="url(#fg)"/>')
    cx, cy = 160, 100
    # chassis / monocoque outline (top view, nose to the right)
    body = (f'M{cx-112} {cy-20} L{cx-60} {cy-26} L{cx+30} {cy-24} L{cx+92} {cy-10} L{cx+118} {cy-5} '
            f'L{cx+118} {cy+5} L{cx+92} {cy+10} L{cx+30} {cy+24} L{cx-60} {cy+26} L{cx-112} {cy+20} Z')
    s.append(f'<path d="{body}" fill="#101113" stroke="#4a4f56" stroke-width="1.2"/>')
    # rear wing and front wing
    s.append(f'<rect x="{cx-138}" y="{cy-46}" width="16" height="92" fill="#15171a" stroke="#4a4f56" stroke-width="1"/>')
    s.append(f'<rect x="{cx+112}" y="{cy-50}" width="12" height="100" fill="#15171a" stroke="#4a4f56" stroke-width="1"/>')
    # cockpit
    s.append(f'<path d="M{cx+2} {cy-12} h34 a12 12 0 0 1 0 24 h-34 z" fill="#050505" stroke="#4a4f56" stroke-width="1"/>')
    s.append(f'<circle cx="{cx+28}" cy="{cy}" r="5" fill="none" stroke="{MUTED}" stroke-width="1"/>')
    # wheels + wheel-hub motors (4WD)
    wheels = [(cx-82, cy-44), (cx-82, cy+44), (cx+76, cy-44), (cx+76, cy+44)]
    for wx, wy in wheels:
        s.append(f'<rect x="{wx-17}" y="{wy-10}" width="34" height="20" rx="3" fill="#1d1f23" stroke="#5a6068" stroke-width="1"/>')
        s.append(f'<circle cx="{wx}" cy="{wy}" r="6" fill="#050505" stroke="{ORANGE}" stroke-width="2"/>')
        s.append(f'<circle cx="{wx}" cy="{wy}" r="1.8" fill="{ORANGE}"/>')
    # suspension arms
    for wx, wy in wheels:
        y0 = cy - 20 if wy < cy else cy + 20
        s.append(f'<path d="M{wx-10} {y0} L{wx} {wy} L{wx+10} {y0}" fill="none" stroke="#3a3f45" stroke-width="1"/>')
    # accumulator (battery) with cells
    ax, ay, aw, ah = cx-64, cy-16, 56, 32
    s.append(f'<rect x="{ax}" y="{ay}" width="{aw}" height="{ah}" fill="{ORANGE}" fill-opacity=".1" stroke="{ORANGE}" stroke-width="1.6"/>')
    for i in range(1, 7):
        s.append(f'<line x1="{ax + i*aw/7:.1f}" y1="{ay+3}" x2="{ax + i*aw/7:.1f}" y2="{ay+ah-3}" stroke="{ORANGE}" stroke-opacity=".55" stroke-width=".8"/>')
    s.append(f'<line x1="{ax+3}" y1="{cy}" x2="{ax+aw-3}" y2="{cy}" stroke="{ORANGE}" stroke-opacity=".35" stroke-width=".8"/>')
    # inverters
    inv = [(cx-96, cy-8), (cx+52, cy-8)]
    for ix, iy in inv:
        s.append(f'<rect x="{ix}" y="{iy}" width="18" height="16" fill="#050505" stroke="{FG}" stroke-width="1.1"/>')
        s.append(f'<path d="M{ix+4} {iy+11} l3 -6 l3 6 l3 -6" fill="none" stroke="{FG}" stroke-width=".9"/>')
    # HV wiring: accumulator -> inverters -> motors
    hv = f'stroke="{ORANGE}" stroke-width="1.4" fill="none" stroke-dasharray="4 2"'
    s.append(f'<path d="M{ax} {cy} H{cx-78}" {hv}/>')
    s.append(f'<path d="M{ax+aw} {cy} H{cx+52}" {hv}/>')
    s.append(f'<path d="M{cx-87} {cy-8} V{cy-34} H{cx-82} V{cy-38}" {hv}/><path d="M{cx-87} {cy+8} V{cy+34} H{cx-82} V{cy+38}" {hv}/>')
    s.append(f'<path d="M{cx+61} {cy-8} V{cy-30} H{cx+76} V{cy-38}" {hv}/><path d="M{cx+61} {cy+8} V{cy+30} H{cx+76} V{cy+38}" {hv}/>')
    # HV label
    s.append(f'<g transform="translate({cx-36} {cy-30})"><path d="M0 -7 L7 5 H-7 Z" fill="none" stroke="{ORANGE}" stroke-width="1.2"/><path d="M0 -3 L-1.6 1 H1 L-.5 4" fill="none" stroke="{ORANGE}" stroke-width="1"/></g>')
    s.append('</svg>')
    return '\n'.join(s)

# ---------------------------------------------------------------- Robust harbor navigation (factor graph)
def harbor_navigation():
    s = []
    s.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="640" height="400">')
    s.append('<defs><pattern id="hg" width="16" height="16" patternUnits="userSpaceOnUse"><path d="M16 0H0V16" fill="none" stroke="#16181b" stroke-width=".8"/></pattern></defs>')
    s.append('<rect width="320" height="200" fill="#060606"/><rect width="320" height="200" fill="url(#hg)"/>')
    land = '#131417'
    # narrow basin: quay walls top and bottom
    s.append(f'<path d="M0 0 H320 V58 H250 L236 70 H120 L106 58 H0 Z" fill="{land}" stroke="#3a3f45" stroke-width="1"/>')
    s.append(f'<path d="M0 200 V156 H90 L104 146 H214 L226 156 H320 V200 Z" fill="{land}" stroke="#3a3f45" stroke-width="1"/>')
    # cranes / buildings on the quay (block GNSS)
    for x, h in ((128, 30), (176, 38), (222, 26)):
        s.append(f'<rect x="{x}" y="{70-h}" width="14" height="{h}" fill="#1c1e22" stroke="#4a4f56" stroke-width=".8"/>')
        s.append(f'<path d="M{x+7} {70-h} V{70-h-10} M{x-6} {70-h-10} H{x+26}" stroke="#4a4f56" stroke-width="1"/>')
    # satellites
    def sat(x, y):
        return (f'<g transform="translate({x} {y}) rotate(-20)"><rect x="-3" y="-3" width="6" height="6" fill="{FG}"/>'
                f'<rect x="-13" y="-2" width="8" height="4" fill="none" stroke="{FG}" stroke-width=".9"/>'
                f'<rect x="5" y="-2" width="8" height="4" fill="none" stroke="{FG}" stroke-width=".9"/></g>')
    s.append(sat(34, 18)); s.append(sat(296, 16)); s.append(sat(190, 10))
    # trajectory poses
    poses = [(26, 108), (60, 104), (96, 102), (132, 104), (168, 108), (204, 110), (240, 106), (276, 100), (304, 96)]
    sig = [6, 6.5, 9, 12, 15, 17, 11, 7, 6]  # uncertainty grows inside the GNSS-denied section
    for (x, y), r in zip(poses, sig):
        s.append(f'<ellipse cx="{x}" cy="{y}" rx="{r*1.25:.1f}" ry="{r*.8:.1f}" fill="{ORANGE}" fill-opacity=".07" stroke="{ORANGE}" stroke-opacity=".35" stroke-width=".7"/>')
    # GNSS factors only at the open ends; blocked signals in the middle
    for (sx, sy), idx in (((34, 18), 0), ((34, 18), 1), ((296, 16), 7), ((296, 16), 8)):
        x, y = poses[idx]
        s.append(f'<line x1="{sx}" y1="{sy+4}" x2="{x}" y2="{y-6}" stroke="{FG}" stroke-opacity=".5" stroke-width=".8" stroke-dasharray="1.5 2"/>')
        s.append(f'<rect x="{x-2.5}" y="{y-20}" width="5" height="5" fill="{FG}"/><line x1="{x}" y1="{y-15}" x2="{x}" y2="{y-4}" stroke="{FG}" stroke-width=".8"/>')
    for tx, ty in ((168, 46), (190, 40)):
        s.append(f'<line x1="190" y1="14" x2="{tx}" y2="{ty}" stroke="{MUTED}" stroke-width=".8" stroke-dasharray="1.5 2"/>')
        s.append(f'<path d="M{tx-3} {ty-3} l6 6 M{tx+3} {ty-3} l-6 6" stroke="{ORANGE}" stroke-width="1.3"/>')
    # landmark factors (LiDAR / radar / camera) to quay corners
    landmarks = [(106, 58), (120, 70), (236, 70), (104, 146), (214, 146)]
    for lx, ly in landmarks:
        s.append(f'<path d="M{lx} {ly-4} l4 7 h-8 z" fill="none" stroke="{BLUE}" stroke-width="1"/>')
    for (pi, li) in ((2, 0), (3, 1), (3, 3), (4, 3), (5, 2), (5, 4), (6, 2), (4, 4)):
        x, y = poses[pi]; lx, ly = landmarks[li]
        mx, my = (x + lx) / 2, (y + ly) / 2
        s.append(f'<line x1="{x}" y1="{y}" x2="{lx}" y2="{ly}" stroke="{BLUE}" stroke-opacity=".55" stroke-width=".8"/>')
        s.append(f'<rect x="{mx-2}" y="{my-2}" width="4" height="4" fill="#060606" stroke="{BLUE}" stroke-width=".8"/>')
    # odometry / IMU factors between consecutive poses
    for (x0, y0), (x1, y1) in zip(poses, poses[1:]):
        s.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{ORANGE}" stroke-width="1.4"/>')
        s.append(f'<rect x="{(x0+x1)/2-2.5:.1f}" y="{(y0+y1)/2-2.5:.1f}" width="5" height="5" fill="#060606" stroke="{ORANGE}" stroke-width="1"/>')
    for x, y in poses:
        s.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#060606" stroke="{ORANGE}" stroke-width="1.6"/>')
    # vessel at the last pose
    s.append(hull(304, 96, 20, 7, -8, fill=ORANGE))
    s.append('</svg>')
    return '\n'.join(s)

# ---------------------------------------------------------------- Inland vessel trajectory prediction
def inland_prediction():
    random.seed(8)
    s = []
    s.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="640" height="400">')
    s.append('<defs><pattern id="ig" width="16" height="16" patternUnits="userSpaceOnUse"><path d="M16 0H0V16" fill="none" stroke="#16181b" stroke-width=".8"/></pattern></defs>')
    s.append('<rect width="320" height="200" fill="#060606"/><rect width="320" height="200" fill="url(#ig)"/>')
    # river centerline (meander) and banks
    def center(x):
        return 112 + 34 * math.sin((x - 20) / 62) - 8 * math.sin((x - 20) / 23)
    xs = [i * 4 for i in range(0, 82)]
    top = [(x, center(x) - 30) for x in xs]; bot = [(x, center(x) + 30) for x in xs]
    river = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in top) + ' L' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in reversed(bot)) + ' Z'
    s.append(f'<path d="{river}" fill="#0d1012"/>')
    for bank in (top, bot):
        s.append('<path d="M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in bank) + '" fill="none" stroke="#3a3f45" stroke-width="1.2"/>')
    # fairway axis
    s.append('<path d="M' + ' L'.join(f'{x:.1f} {center(x):.1f}' for x in xs) + f'" fill="none" stroke="{MUTED}" stroke-opacity=".5" stroke-width=".7" stroke-dasharray="3 4"/>')
    # river kilometre markers
    for x in (40, 120, 200, 280):
        y = center(x) + 30
        s.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+6}" stroke="{MUTED}" stroke-width="1"/>')
    # AIS history (past positions)
    x0 = 128
    hist = [(x, center(x) + 6 + random.uniform(-1.2, 1.2)) for x in range(20, x0, 9)]
    for i, (x, y) in enumerate(hist):
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="{BLUE}" opacity="{.3 + .6 * i / len(hist):.2f}"/>')
    vy = center(x0) + 6
    # predicted futures: fan of samples + growing uncertainty
    for k in range(-4, 5):
        pts = []
        for j in range(0, 46):
            x = x0 + j * 3.6
            spread = (j / 45) ** 1.5 * 22 * k / 4
            pts.append((x, center(x) + 6 + spread))
        op = .9 if k == 0 else .22
        w = 1.8 if k == 0 else 1
        s.append('<path d="M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + f'" fill="none" stroke="{ORANGE}" stroke-opacity="{op}" stroke-width="{w}"' + (' stroke-dasharray="4 3"' if k == 0 else '') + '/>')
    for j in (15, 30, 45):
        x = x0 + j * 3.6; r = 3 + (j / 45) ** 1.5 * 22
        s.append(f'<ellipse cx="{x:.1f}" cy="{center(x) + 6:.1f}" rx="{r*.55:.1f}" ry="{r:.1f}" fill="none" stroke="{ORANGE}" stroke-opacity=".5" stroke-width=".8"/>')
    # the vessel (long inland barge) with AIS beacon
    ang = math.degrees(math.atan2(center(x0 + 1) - center(x0 - 1), 2))
    s.append(hull(x0, vy, 34, 8, ang, fill=FG))
    s.append(f'<g fill="none" stroke="{BLUE}" stroke-width="1" stroke-linecap="round"><path d="M{x0-4} {vy-12} a6 6 0 0 1 8 0"/><path d="M{x0-7} {vy-16} a10 10 0 0 1 14 0"/></g>')
    s.append(f'<text x="{x0-30}" y="{vy-18}" font-family="Menlo, Consolas, monospace" font-size="8" letter-spacing="1" fill="{BLUE}">AIS</text>')
    s.append('</svg>')
    return '\n'.join(s)

open(f'{OUT}/harbor-navigation.svg', 'w').write(harbor_navigation())
open(f'{OUT}/inland-trajectory-prediction.svg', 'w').write(inland_prediction())
open(f'{OUT}/formula-student.svg', 'w').write(formula_student())
open(f'{OUT}/simple-c.svg', 'w').write(simplec())
open(f'{OUT}/mstnet.svg', 'w').write(mstnet())
open(f'{OUT}/icmass2025.svg', 'w').write(icmass())
open(f'{OUT}/icecet2023.svg', 'w').write(icecet())
print('ok')
