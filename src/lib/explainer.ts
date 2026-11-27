// Shared helpers for interactive explainer figures (canvas drawing, colors, randomness).

export type Palette = { fg: string; soft: string; muted: string; border: string; strong: string; accent: string; bg: string; surface: string };

export function palette(): Palette {
  const s = getComputedStyle(document.documentElement);
  const v = (n: string) => s.getPropertyValue(n).trim();
  return {
    fg: v('--fg'), soft: v('--fg-soft'), muted: v('--muted'), border: v('--border'),
    strong: v('--border-strong'), accent: v('--accent'), bg: v('--bg'), surface: v('--bg'),
  };
}

/** Keeps a canvas sharp on high-DPI screens. `ratio` = height / width. Calls draw() after each resize. */
export function setupCanvas(canvas: HTMLCanvasElement, ratio: number | ((w: number) => number), draw: () => void) {
  const ctx = canvas.getContext('2d')!;
  const size = { w: 0, h: 0 };
  const resize = () => {
    const dpr = window.devicePixelRatio || 1;
    const w = canvas.clientWidth;
    if (!w) return;
    const h = Math.round(typeof ratio === 'number' ? w * ratio : ratio(w));
    canvas.style.height = `${h}px`;
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    size.w = w; size.h = h;
    draw();
  };
  // defer to the next frame and ignore height-only changes, so setting the height does not re-trigger the observer
  let lastW = -1, pending = 0;
  new ResizeObserver(() => {
    if (canvas.clientWidth === lastW || pending) return;
    pending = requestAnimationFrame(() => { pending = 0; lastW = canvas.clientWidth; resize(); });
  }).observe(canvas);
  whenFonts(resize);
  return { ctx, size, resize };
}

/** Runs `tick(dt)` every animation frame while the element is on screen and `isRunning()` is true. */
export function animate(el: Element, tick: (dt: number) => void, isRunning: () => boolean = () => true) {
  let visible = false, last = 0, raf = 0;
  const loop = (t: number) => {
    raf = 0;
    if (!visible || !isRunning()) { last = 0; return; }
    const dt = last ? Math.min((t - last) / 1000, 0.05) : 0;
    last = t;
    tick(dt);
    raf = requestAnimationFrame(loop);
  };
  const kick = () => { if (!raf && visible && isRunning()) raf = requestAnimationFrame(loop); };
  new IntersectionObserver((es) => { visible = es[0].isIntersecting; kick(); }).observe(el);
  return { kick };
}

export const reducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

export function arrow(ctx: CanvasRenderingContext2D, x0: number, y0: number, x1: number, y1: number, color: string, width = 2, head = 8) {
  const dx = x1 - x0, dy = y1 - y0, len = Math.hypot(dx, dy);
  if (len < 0.5) return;
  const ux = dx / len, uy = dy / len, hh = Math.min(head, len * 0.6);
  ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = width;
  ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1 - ux * hh * 0.7, y1 - uy * hh * 0.7); ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x1 - ux * hh - uy * hh * 0.45, y1 - uy * hh + ux * hh * 0.45);
  ctx.lineTo(x1 - ux * hh + uy * hh * 0.45, y1 - uy * hh - ux * hh * 0.45);
  ctx.closePath(); ctx.fill();
}

export const SANS = "Arial, 'Helvetica Neue', Helvetica, 'Liberation Sans', sans-serif";

// ---- LaTeX-like math on canvas, drawn with the KaTeX fonts ----------------------------------
// Supported: letters (italic), digits/operators (upright), \greek, \b{bold vector}, \r{upright},
// \, (thin space), _x / _{..} subscripts, ^x / ^{..} superscripts.
const GREEK: Record<string, string> = {
  alpha: 'α', beta: 'β', gamma: 'γ', delta: 'δ', varepsilon: 'ε', epsilon: 'ϵ', theta: 'θ', lambda: 'λ',
  sigma: 'σ', phi: 'ϕ', varphi: 'φ', psi: 'ψ', omega: 'ω', mu: 'μ', pi: 'π', tau: 'τ', eta: 'η', rho: 'ρ', xi: 'ξ', nu: 'ν', kappa: 'κ', zeta: 'ζ', chi: 'χ', iota: 'ι',
  Delta: 'Δ', Omega: 'Ω', Gamma: 'Γ', Theta: 'Θ', Lambda: 'Λ', Sigma: 'Σ', Phi: 'Φ', Psi: 'Ψ', Pi: 'Π',
};
const SYMBOLS: Record<string, string> = { pm: '±', mp: '∓', times: '×', cdot: '·', approx: '≈', leq: '≤', geq: '≥', infty: '∞', to: '→', propto: '∝', partial: '∂', neq: '≠', perp: '⊥', parallel: '∥', otimes: '⊗', ast: '∗' };
type Face = 'it' | 'rm' | 'bf' | 'bi';
type Atom = { t: string; f: Face; s: 0 | 1 | -1; stack?: boolean };

function readGroup(src: string, i: number): [string, number] {
  if (src[i] === '{') { let d = 1, j = i + 1; for (; j < src.length && d; j++) { if (src[j] === '{') d++; else if (src[j] === '}') d--; } return [src.slice(i + 1, j - 1), j]; }
  if (src[i] === '\\') { const m = /^\\[a-zA-Z]+/.exec(src.slice(i)); if (m) return [m[0], i + m[0].length]; return [src.slice(i, i + 2), i + 2]; }
  return [src[i], i + 1];
}
function parseTex(src: string, shift: 0 | 1 | -1 = 0): Atom[] {
  const out: Atom[] = [];
  let i = 0, lastScript: 0 | 1 | -1 = 0;
  while (i < src.length) {
    const c = src[i];
    if (c === '_' || c === '^') {
      const [g, j] = readGroup(src, i + 1);
      const sh = c === '_' ? 1 : -1;
      const atoms = parseTex(g, sh);
      if (atoms.length && lastScript && lastScript !== sh) atoms[0].stack = true;
      out.push(...atoms); lastScript = sh; i = j; continue;
    }
    lastScript = 0;
    if (c === '\\') {
      const m = /^\\([a-zA-Z]+)/.exec(src.slice(i));
      if (!m) { if (src[i + 1] === ',') out.push({ t: '\u2009', f: 'rm', s: shift }); i += 2; continue; }
      const name = m[1]; i += m[0].length;
      if (name === 'b' || name === 'mathbf' || name === 'r' || name === 'mathrm') { const [g, j] = readGroup(src, i); out.push({ t: g, f: name === 'b' || name === 'mathbf' ? 'bf' : 'rm', s: shift }); i = j; continue; }
      if (name === 'bar' || name === 'hat' || name === 'tilde') {
        const [g, j] = readGroup(src, i); i = j;
        const inner = parseTex(g, shift);
        if (inner.length) inner[0] = { ...inner[0], t: inner[0].t + (name === 'bar' ? '\u0304' : name === 'hat' ? '\u0302' : '\u0303') };
        out.push(...inner);
        continue;
      }
      if (name === 'boldsymbol') {
        const [g, j] = readGroup(src, i); i = j;
        for (const a of parseTex(g, shift)) out.push({ ...a, f: a.f === 'it' ? 'bi' : 'bf' });
        continue;
      }
      if (SYMBOLS[name]) { out.push({ t: SYMBOLS[name], f: 'rm', s: shift }); continue; }
      const gk = GREEK[name];
      if (gk) out.push({ t: gk, f: name[0] === name[0].toUpperCase() ? 'rm' : 'it', s: shift });
      continue;
    }
    out.push({ t: c === '-' ? '−' : c, f: /[a-zA-Z]/.test(c) ? 'it' : 'rm', s: shift });
    i++;
  }
  return out;
}
const faceFont = (f: Face, px: number) =>
  f === 'it' ? `italic ${px}px KaTeX_Math` : f === 'bi' ? `italic bold ${px}px KaTeX_Math` : f === 'bf' ? `bold ${px}px KaTeX_Main` : `${px}px KaTeX_Main`;

type Op = { t: string; font: string; x: number; dy: number };
function layout(ctx: CanvasRenderingContext2D, text: string, size: number, weight: number): { ops: Op[]; w: number } {
  const ops: Op[] = [];
  let x = 0;
  text.split('$').forEach((seg, k) => {
    if (!seg) return;
    if (k % 2 === 0) {
      const font = `${weight} ${size}px ${SANS}`;
      ctx.font = font; ops.push({ t: seg, font, x, dy: 0 }); x += ctx.measureText(seg).width; return;
    }
    const base = size * 1.18, scr = base * 0.7;
    let scriptStart = x, scriptEnd = x;
    for (const a of parseTex(seg)) {
      const px = a.s ? scr : base, font = faceFont(a.f, px);
      ctx.font = font;
      if (a.s) {
        if (a.stack) { scriptEnd = Math.max(scriptEnd, x); x = scriptStart; } else if (!ops.length || ops[ops.length - 1].dy === 0) { scriptStart = x; }
      } else { x = Math.max(x, scriptEnd); scriptStart = scriptEnd = x; }
      ops.push({ t: a.t, font, x, dy: a.s === 1 ? base * 0.26 : a.s === -1 ? -base * 0.36 : 0 });
      x += ctx.measureText(a.t).width + ((a.f === 'it' || a.f === 'bi') && !a.s ? base * 0.03 : 0);
      if (a.s) scriptEnd = Math.max(scriptEnd, x);
    }
    x = Math.max(x, scriptEnd);
  });
  return { ops, w: x };
}

/** Draws a label. Text is set in Arial; parts between $…$ are typeset as math with the KaTeX fonts. */
export function label(ctx: CanvasRenderingContext2D, text: string, x: number, y: number, color: string, opts: { align?: CanvasTextAlign; base?: CanvasTextBaseline; size?: number; mono?: boolean; weight?: number } = {}) {
  const { align = 'left', base = 'middle', size = 12, weight = 400 } = opts;
  const { ops, w } = layout(ctx, text, size, weight);
  const x0 = align === 'center' ? x - w / 2 : align === 'right' || align === 'end' ? x - w : x;
  ctx.fillStyle = color; ctx.textAlign = 'left'; ctx.textBaseline = base;
  for (const o of ops) { ctx.font = o.font; ctx.fillText(o.t, x0 + o.x, y + o.dy); }
  return w;
}

/** Calls `cb` once the KaTeX fonts used for canvas math are available. */
export function whenFonts(cb: () => void) {
  if (!('fonts' in document)) return;
  Promise.all(['italic 16px KaTeX_Math', 'italic bold 16px KaTeX_Math', '16px KaTeX_Main', 'bold 16px KaTeX_Main'].map((f) => document.fonts.load(f))).then(cb, cb);
}

/** Fills elements marked with data-o="name" inside a figure. */
export function outputs(root: Element) {
  const cache = new Map<string, HTMLElement | null>();
  return (name: string, value: string) => {
    if (!cache.has(name)) cache.set(name, root.querySelector<HTMLElement>(`[data-o="${name}"]`));
    const el = cache.get(name);
    if (el && el.textContent !== value) el.textContent = value;
  };
}

/** Small seeded random number generator (mulberry32) with a Gaussian helper. */
export function rng(seed = 1) {
  let a = seed >>> 0;
  const uni = () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const gauss = () => {
    const u = Math.max(uni(), 1e-12), v = uni();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  };
  return { uni, gauss };
}

/** Linear axis mapping helper. */
export const lin = (d0: number, d1: number, r0: number, r1: number) => (x: number) => r0 + ((x - d0) / (d1 - d0)) * (r1 - r0);

/** Picks a "nice" tick step for an axis span. */
export function niceStep(span: number, target = 5) {
  const raw = span / target, p = 10 ** Math.floor(Math.log10(raw)), m = raw / p;
  return (m < 1.5 ? 1 : m < 3.5 ? 2 : m < 7.5 ? 5 : 10) * p;
}

/** Formats a length in metres with a sensible unit. */
export function fmtLen(m: number) {
  const a = Math.abs(m);
  if (a >= 1000) return `${(m / 1000).toFixed(a >= 1e5 ? 0 : 1)} km`;
  if (a >= 1) return `${m.toFixed(a >= 100 ? 0 : 1)} m`;
  return `${(m * 100).toFixed(1)} cm`;
}

/** Wires a range input to an <output> and a callback. Returns the current value getter. */
export function slider(root: Element, name: string, fmt: (v: number) => string, onChange: (v: number) => void) {
  const input = root.querySelector<HTMLInputElement>(`input[name="${name}"]`)!;
  const out = root.querySelector<HTMLOutputElement>(`output[for="${name}"]`);
  const read = () => Number(input.value);
  const sync = () => { if (out) out.textContent = fmt(read()); onChange(read()); };
  input.addEventListener('input', sync);
  sync();
  return { read, set: (v: number) => { input.value = String(v); sync(); }, input };
}

export type Box = { x: number; y: number; w: number; h: number };
type AxesOpts = {
  xlabel?: string; ylabel?: string;
  xfmt?: (v: number) => string; yfmt?: (v: number) => string;
  xticks?: number; yticks?: number; logY?: boolean; zeroLine?: boolean;
};

/** Draws a plot frame with ticks and returns the data-to-pixel mappings. */
export function axes(ctx: CanvasRenderingContext2D, P: Palette, b: Box, xr: [number, number], yr: [number, number], o: AxesOpts = {}) {
  const { xfmt = (v) => String(+v.toFixed(6)), yfmt = (v) => String(+v.toFixed(6)), xticks = 6, yticks = 4, logY = false } = o;
  const sx = lin(xr[0], xr[1], b.x, b.x + b.w);
  const ly0 = Math.log10(yr[0]), ly1 = Math.log10(yr[1]);
  const sy = logY
    ? (v: number) => b.y + b.h - ((Math.log10(Math.max(v, 1e-30)) - ly0) / (ly1 - ly0)) * b.h
    : lin(yr[0], yr[1], b.y + b.h, b.y);

  ctx.lineWidth = 1;
  // grid + y ticks
  const yt: number[] = [];
  if (logY) for (let e = Math.ceil(ly0); e <= Math.floor(ly1); e++) yt.push(10 ** e);
  else { const st = niceStep(yr[1] - yr[0], yticks); for (let v = Math.ceil(yr[0] / st) * st; v <= yr[1] + 1e-9; v += st) yt.push(v); }
  for (const v of yt) {
    const y = Math.round(sy(v)) + 0.5;
    ctx.strokeStyle = P.border; ctx.beginPath(); ctx.moveTo(b.x, y); ctx.lineTo(b.x + b.w, y); ctx.stroke();
    label(ctx, yfmt(v), b.x - 6, y, P.muted, { align: 'right', size: 10 });
  }
  const xs = niceStep(xr[1] - xr[0], xticks);
  for (let v = Math.ceil(xr[0] / xs) * xs; v <= xr[1] + 1e-9; v += xs) {
    const x = Math.round(sx(v)) + 0.5;
    ctx.strokeStyle = P.border; ctx.beginPath(); ctx.moveTo(x, b.y); ctx.lineTo(x, b.y + b.h); ctx.stroke();
    label(ctx, xfmt(v), x, b.y + b.h + 12, P.muted, { align: 'center', size: 10 });
  }
  if (o.zeroLine && !logY && yr[0] < 0 && yr[1] > 0) {
    ctx.strokeStyle = P.strong; ctx.beginPath(); ctx.moveTo(b.x, Math.round(sy(0)) + 0.5); ctx.lineTo(b.x + b.w, Math.round(sy(0)) + 0.5); ctx.stroke();
  }
  ctx.strokeStyle = P.strong; ctx.strokeRect(b.x + 0.5, b.y + 0.5, b.w - 1, b.h - 1);
  if (o.xlabel) label(ctx, o.xlabel, b.x + b.w, b.y + b.h + 26, P.muted, { align: 'right', size: 10 });
  if (o.ylabel) label(ctx, o.ylabel, b.x + 6, b.y + 10, P.soft, { size: 10 });
  return { sx, sy };
}

/** Draws a polyline through data points, clipped to the box. */
export function series(ctx: CanvasRenderingContext2D, b: Box, xs: ArrayLike<number>, ys: ArrayLike<number>, sx: (v: number) => number, sy: (v: number) => number, color: string, width = 1.75, dash: number[] = [], upTo = xs.length) {
  ctx.save();
  ctx.beginPath(); ctx.rect(b.x, b.y, b.w, b.h); ctx.clip();
  ctx.strokeStyle = color; ctx.lineWidth = width; ctx.setLineDash(dash); ctx.lineJoin = 'round';
  ctx.beginPath();
  let pen = false;
  for (let i = 0; i < Math.min(upTo, xs.length); i++) {
    const y = ys[i];
    if (!Number.isFinite(y)) { pen = false; continue; }
    const X = sx(xs[i]), Y = Math.max(-1e4, Math.min(1e4, sy(y)));
    pen ? ctx.lineTo(X, Y) : ctx.moveTo(X, Y);
    pen = true;
  }
  ctx.stroke();
  ctx.restore();
}
