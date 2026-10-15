// A_v16: restrained push entry ONLY for horizontal splits containing one presenter.
// Shared by picture composition, film-region masking and the incoming panel's type.
// The insert keeps its final crop throughout the slide; the presenter is re-cropped,
// never squeezed. All geometry is a deterministic function of programme time.
import { clamp, ease } from './engine.js';

export function splitLayout(spec, t, r) {
  const split = spec.split, at = split.at ?? 0.5;
  const horizontal = (split.dir || (r.w > r.h ? 'h' : 'v')) === 'h';
  const extent = Math.round((horizontal ? r.w : r.h) * at);
  const a = horizontal ? { x: r.x, y: r.y, w: extent, h: r.h } : { x: r.x, y: r.y, w: r.w, h: extent };
  const b = horizontal ? { x: r.x + extent, y: r.y, w: r.w - extent, h: r.h } : { x: r.x, y: r.y + extent, w: r.w, h: r.h - extent };
  const presenterA = split.a.kind === 'presenter', presenterB = split.b.kind === 'presenter';
  const animated = horizontal && presenterA !== presenterB && split.entry !== false;
  const duration = Math.max(0.04, split.entry?.duration ?? 0.4);
  const progress = animated ? ease('sineInOut', clamp((t - spec.t0) / duration)) : 1;
  const side = presenterB ? 'left' : 'right';
  let offset = 0, edge = r.x + extent;
  if (animated && presenterA) {
    offset = b.w * (1 - progress);
    b.x += offset; a.w = b.x - r.x; edge = b.x;
  } else if (animated && presenterB) {
    offset = -a.w * (1 - progress);
    a.x += offset; b.x = a.x + a.w; b.w = r.x + r.w - b.x; edge = b.x;
  }
  const insert = animated && presenterB ? a : b;
  const grainRect = horizontal
    ? [clamp((insert.x - r.x) / r.w), 0, clamp((insert.x + insert.w - r.x) / r.w), 1]
    : [0, at, 1, 1];
  return { a, b, horizontal, animated, progress, side, offset, edge, grainRect,
    typeMotion: animated && progress < 1 ? { side, offset, edge: r.x + extent, t0: spec.t0, t1: spec.t1 } : null };
}
