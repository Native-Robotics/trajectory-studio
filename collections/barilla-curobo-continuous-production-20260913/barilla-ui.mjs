export function trajectoryLabel(row) {
  const id = String(row.id || row.desired_id || "");
  const suffix = id.match(/-(ref|curobo)$/)?.[0] || "";
  return id.slice(0, 8) + suffix;
}

export function destinationLabel(tag = "") {
  const last = String(tag).split(",").at(-1);
  if (/pick/i.test(last)) return "to-pick-point";
  if (/wait/i.test(last)) return "to wait node";
  if (/place/i.test(last)) return "to-place";
  return "";
}
function numberCompare(a, b, direction = 1) {
  const knownA = typeof a === "number" && Number.isFinite(a),
    knownB = typeof b === "number" && Number.isFinite(b);
  if (!knownA || !knownB) return Number(knownB) - Number(knownA);
  return (a - b) * direction;
}
export function sortRows(rows, key = "box", direction = 1, context = rows) {
  if (rows.length && context.length && context.every(row => row.pair_id)) {
    const groups = new Map();
    for (const row of context) {
      if (!groups.has(row.pair_id)) groups.set(row.pair_id, []);
      groups.get(row.pair_id).push(row);
    }
    const representatives = [...groups.values()].map(group => {
      const row = group.find(item => item.id.endsWith("-curobo")) || group[0];
      const {pair_id, ...representative} = row;
      return {...representative, id: pair_id};
    });
    const visible = new Set(rows);
    return sortRows(representatives, key, direction, representatives).flatMap(row =>
      groups.get(row.id).filter(item => visible.has(item)).sort((a, b) =>
        Number(a.id.endsWith("-ref")) - Number(b.id.endsWith("-ref")) ||
        a.id.localeCompare(b.id)),
    );
  }
  // A pick can already name the next box/pallet. Associate it with the last
  // placement in recorded chronology instead of subtracting from that label.
  const cycle = new Map();
  let placement = null;
  if (key === "box")
    for (const row of [...context].sort((a, b) =>
      numberCompare(a.task_id, b.task_id),
    )) {
      const destination = destinationLabel(row.tag);
      if (destination === "to-place") placement = row;
      cycle.set(
        row,
        placement &&
          ["to-place", "to wait node", "to-pick-point"].includes(destination)
          ? placement
          : row,
      );
    }
  return [...rows].sort((a, b) => {
    let difference;
    if (key === "box") {
      const ca = cycle.get(a) || a,
        cb = cycle.get(b) || b;
      difference =
        String(ca.place_pallet || "~").localeCompare(
          String(cb.place_pallet || "~"),
        ) * direction ||
        numberCompare(ca.box_number, cb.box_number, direction) ||
        numberCompare(ca.task_id, cb.task_id, direction) ||
        numberCompare(a.task_id, b.task_id);
    } else
      difference = numberCompare(
        a[
          key === "mileage"
            ? "mileage_sum_rad"
            : key === "compute"
              ? "compute_s"
              : key
        ],
        b[
          key === "mileage"
            ? "mileage_sum_rad"
            : key === "compute"
              ? "compute_s"
              : key
        ],
        direction,
      );
    return (
      difference ||
      String(a.id || a.desired_id).localeCompare(String(b.id || b.desired_id))
    );
  });
}
export function arrowDelta(event) {
  if (
    event.altKey ||
    event.ctrlKey ||
    event.metaKey ||
    event.shiftKey ||
    event.target?.isContentEditable ||
    ["INPUT", "TEXTAREA", "SELECT"].includes(event.target?.tagName)
  )
    return 0;
  return event.key === "ArrowDown" ? 1 : event.key === "ArrowUp" ? -1 : 0;
}
export function installPanelResize(root) {
  const key = "barilla-panel-widths";
  let widths = { left: 300, right: 560 };
  try {
    const saved = JSON.parse(localStorage.getItem(key));
    if (saved && Number.isFinite(saved.left) && Number.isFinite(saved.right))
      widths = saved;
  } catch {}
  const apply = () => {
    const available = Math.max(600, root.clientWidth - 364);
    widths.left = Math.max(220, Math.min(widths.left, available - 360));
    widths.right = Math.max(
      360,
      Math.min(widths.right, available - widths.left),
    );
    root.style.setProperty("--barilla-left", widths.left + "px");
    root.style.setProperty("--barilla-right", widths.right + "px");
  };
  const save = () => {
    try {
      localStorage.setItem(key, JSON.stringify(widths));
    } catch {}
  };
  for (const side of ["left", "right"]) {
    const handle = document.getElementById("resize-" + side);
    handle.addEventListener("pointerdown", (event) => {
      event.preventDefault();
      handle.focus({ preventScroll: true });
      handle.setPointerCapture(event.pointerId);
      const x = event.clientX,
        initial = widths[side];
      const move = (e) => {
        widths[side] = initial + (e.clientX - x) * (side === "left" ? 1 : -1);
        apply();
      };
      const stop = () => {
        handle.removeEventListener("pointermove", move);
        handle.removeEventListener("pointerup", stop);
        handle.removeEventListener("pointercancel", stop);
        save();
      };
      handle.addEventListener("pointermove", move);
      handle.addEventListener("pointerup", stop, { once: true });
      handle.addEventListener("pointercancel", stop, { once: true });
    });
    handle.addEventListener("keydown", (event) => {
      if (!["ArrowLeft", "ArrowRight"].includes(event.key)) return;
      event.preventDefault();
      widths[side] +=
        (event.key === "ArrowRight" ? 20 : -20) * (side === "left" ? 1 : -1);
      apply();
      save();
    });
  }
  window.addEventListener("resize", apply);
  apply();
}

export function formatFlags(flags = []) {
  return (
    flags
      .map((flag) => (typeof flag === "string" ? flag : flag.code))
      .filter(Boolean)
      .join(", ") || "—"
  );
}
