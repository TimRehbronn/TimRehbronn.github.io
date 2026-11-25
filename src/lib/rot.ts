// Minimal 3-D rotation math for the explainers: vectors, 3x3 matrices (row-major), Hamilton quaternions [w, x, y, z].

export type V3 = [number, number, number];
export type M3 = [number, number, number, number, number, number, number, number, number];
export type Q = [number, number, number, number];

export const add = (a: V3, b: V3): V3 => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
export const sub = (a: V3, b: V3): V3 => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
export const scale = (a: V3, s: number): V3 => [a[0] * s, a[1] * s, a[2] * s];
export const dot = (a: V3, b: V3) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
export const cross = (a: V3, b: V3): V3 => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
export const norm = (a: V3) => Math.hypot(a[0], a[1], a[2]);

export const I3: M3 = [1, 0, 0, 0, 1, 0, 0, 0, 1];
export const mv = (m: M3, v: V3): V3 => [
  m[0] * v[0] + m[1] * v[1] + m[2] * v[2],
  m[3] * v[0] + m[4] * v[1] + m[5] * v[2],
  m[6] * v[0] + m[7] * v[1] + m[8] * v[2],
];
export function mm(a: M3, b: M3): M3 {
  const r = new Array(9).fill(0) as M3;
  for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) for (let k = 0; k < 3; k++) r[i * 3 + j] += a[i * 3 + k] * b[k * 3 + j];
  return r;
}
export const tr = (m: M3): M3 => [m[0], m[3], m[6], m[1], m[4], m[7], m[2], m[5], m[8]];

export const rx = (a: number): M3 => { const c = Math.cos(a), s = Math.sin(a); return [1, 0, 0, 0, c, -s, 0, s, c]; };
export const ry = (a: number): M3 => { const c = Math.cos(a), s = Math.sin(a); return [c, 0, s, 0, 1, 0, -s, 0, c]; };
export const rz = (a: number): M3 => { const c = Math.cos(a), s = Math.sin(a); return [c, -s, 0, s, c, 0, 0, 0, 1]; };
/** Body-to-navigation DCM from ZYX Euler angles (roll φ, pitch θ, yaw ψ). */
export const euler = (roll: number, pitch: number, yaw: number) => mm(rz(yaw), mm(ry(pitch), rx(roll)));

/** Rotation matrix for a rotation vector (Rodrigues' formula). */
export function rexp(a: V3): M3 {
  const t = norm(a);
  if (t < 1e-12) return [1, -a[2], a[1], a[2], 1, -a[0], -a[1], a[0], 1];
  const k = scale(a, 1 / t), c = Math.cos(t), s = Math.sin(t), v = 1 - c;
  const [x, y, z] = k;
  return [
    c + x * x * v, x * y * v - z * s, x * z * v + y * s,
    y * x * v + z * s, c + y * y * v, y * z * v - x * s,
    z * x * v - y * s, z * y * v + x * s, c + z * z * v,
  ];
}

export const qmul = (a: Q, b: Q): Q => [
  a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3],
  a[0] * b[1] + a[1] * b[0] + a[2] * b[3] - a[3] * b[2],
  a[0] * b[2] - a[1] * b[3] + a[2] * b[0] + a[3] * b[1],
  a[0] * b[3] + a[1] * b[2] - a[2] * b[1] + a[3] * b[0],
];
export const qconj = (a: Q): Q => [a[0], -a[1], -a[2], -a[3]];
export const qnormalize = (a: Q): Q => { const n = Math.hypot(...a); return [a[0] / n, a[1] / n, a[2] / n, a[3] / n]; };
export function qexp(v: V3): Q {
  const t = norm(v);
  if (t < 1e-12) return qnormalize([1, v[0] / 2, v[1] / 2, v[2] / 2]);
  const s = Math.sin(t / 2) / t;
  return [Math.cos(t / 2), v[0] * s, v[1] * s, v[2] * s];
}
/** Rotation angle (rad) of a unit quaternion. */
export const qangle = (q: Q) => 2 * Math.atan2(Math.hypot(q[1], q[2], q[3]), Math.abs(q[0]));
export function qmat(q: Q): M3 {
  const [w, x, y, z] = q;
  return [
    1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y),
    2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x),
    2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y),
  ];
}
/** Spherical interpolation between unit quaternions. */
export function slerp(a: Q, b: Q, t: number): Q {
  let d = a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3];
  let bb = b;
  if (d < 0) { d = -d; bb = [-b[0], -b[1], -b[2], -b[3]]; }
  if (d > 0.9995) return qnormalize([a[0] + t * (bb[0] - a[0]), a[1] + t * (bb[1] - a[1]), a[2] + t * (bb[2] - a[2]), a[3] + t * (bb[3] - a[3])]);
  const th = Math.acos(d), s = Math.sin(th);
  const wa = Math.sin((1 - t) * th) / s, wb = Math.sin(t * th) / s;
  return [wa * a[0] + wb * bb[0], wa * a[1] + wb * bb[1], wa * a[2] + wb * bb[2], wa * a[3] + wb * bb[3]];
}
export function matq(m: M3): Q {
  const t = m[0] + m[4] + m[8];
  if (t > 0) {
    const s = Math.sqrt(t + 1) * 2;
    return qnormalize([0.25 * s, (m[7] - m[5]) / s, (m[2] - m[6]) / s, (m[3] - m[1]) / s]);
  }
  if (m[0] > m[4] && m[0] > m[8]) {
    const s = Math.sqrt(1 + m[0] - m[4] - m[8]) * 2;
    return qnormalize([(m[7] - m[5]) / s, 0.25 * s, (m[1] + m[3]) / s, (m[2] + m[6]) / s]);
  }
  if (m[4] > m[8]) {
    const s = Math.sqrt(1 + m[4] - m[0] - m[8]) * 2;
    return qnormalize([(m[2] - m[6]) / s, (m[1] + m[3]) / s, 0.25 * s, (m[5] + m[7]) / s]);
  }
  const s = Math.sqrt(1 + m[8] - m[0] - m[4]) * 2;
  return qnormalize([(m[3] - m[1]) / s, (m[2] + m[6]) / s, (m[5] + m[7]) / s, 0.25 * s]);
}

/**
 * Simple orthographic camera for drawing 3-D scenes on a canvas.
 * World axes follow the NED convention used in the post (x north, y east, z down);
 * the camera looks at the origin from azimuth `az` and elevation `el` (radians, el > 0 = from above).
 */
export function camera(az: number, el: number, scalePx: number, cx: number, cy: number) {
  // screen right = r, screen up = u, depth towards viewer = d
  const ca = Math.cos(az), sa = Math.sin(az), ce = Math.cos(el), se = Math.sin(el);
  // viewer direction in world (NED): horizontal direction (ca, sa, 0) lifted by el (up = -z)
  const d: V3 = [ca * ce, sa * ce, -se];
  const up: V3 = [0, 0, -1];
  let r = cross(up, d); const rn = norm(r); r = scale(r, 1 / rn);
  const u = cross(d, r);
  return {
    project: (p: V3) => ({ x: cx + dot(p, r) * scalePx, y: cy - dot(p, u) * scalePx, z: dot(p, d) }),
    view: d,
  };
}
