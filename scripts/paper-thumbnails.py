"""Generate the ICMASS 2025 and ICECET 2023 paper teaser SVGs (320x200).

Usage: python3 scripts/paper-thumbnails.py public/images/publications
"""
import math, random, sys
OUT = sys.argv[1]
BLUE, ORANGE, FG, MUTED = '#5cb8ff', '#fd7422', '#ededed', '#6b7280'

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
    s.append('<defs><radialGradient id="w" cx="45%" cy="60%" r="80%"><stop offset="0" stop-color="#0c1824"/><stop offset="1" stop-color="#05080c"/></radialGradient>'
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
    s.append('<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1016"/><stop offset="1" stop-color="#040506"/></linearGradient></defs>')
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
            s.append(f'<rect width="150" height="100" fill="#0e151d" stroke="{BLUE}" stroke-opacity=".5" stroke-width="1.2"/>')
            pts, (cx, cy) = scene(-k * 6)
            for x, y, kind in pts:
                col = {'road': BLUE, 'ring': '#2f5d80', 'car': FG, 'car2': FG, 'noise': '#7c8794'}[kind]
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
            s.append(f'<circle cx="{ax}" cy="{y}" r="3.5" fill="#05080c" stroke="{MUTED}" stroke-dasharray="1.5 1.5"/>')
    s.append(f'<text x="{ax-9}" y="{33+4*28+4}" text-anchor="end" font-family="Helvetica, Arial, sans-serif" font-size="10" font-weight="700" fill="{ORANGE}">t</text>')
    # rain streaks over everything
    for _ in range(46):
        x, y = random.uniform(0, 300), random.uniform(-10, 190); l = random.uniform(6, 12)
        s.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x-l*0.35:.1f}" y2="{y+l:.1f}" stroke="#a9c7e6" stroke-opacity="{random.uniform(.15,.4):.2f}" stroke-width=".8" stroke-linecap="round"/>')
    s.append('</svg>')
    return '\n'.join(s)

open(f'{OUT}/icmass2025.svg', 'w').write(icmass())
open(f'{OUT}/icecet2023.svg', 'w').write(icecet())
print('ok')
