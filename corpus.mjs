import { sortRows, destinationLabel } from "./barilla-ui.mjs";
let rows = [],
  key = "task_id",
  direction = 1;
const numeric = (value) =>
  typeof value === "number" && Number.isFinite(value) ? value.toFixed(2) : "—";
function render() {
  const query = document.getElementById("search").value.toLowerCase();
  const filtered = rows.filter((row) =>
    [row.task_id, row.desired_id, row.place_pallet, destinationLabel(row.tag)]
      .join(" ")
      .toLowerCase()
      .includes(query),
  );
  document.getElementById("message").textContent =
    `${filtered.length} / ${rows.length} historical tasks`;
  const body = document.getElementById("rows");
  body.replaceChildren();
  for (const row of sortRows(filtered, key, direction)) {
    const tr = document.createElement("tr");
    if (row.red) tr.className = "flagged";
    const values = [
      row.task_id,
      row.desired_id.slice(0, 8),
      destinationLabel(row.tag),
      row.place_pallet || "—",
      row.box_number ?? "—",
      row.status || "—",
      (row.flags || []).join(", ") || "—",
      numeric(row.compute_s),
      numeric(row.traj_time_s),
      numeric(row.mileage_sum_rad),
    ];
    values.forEach((value, index) => {
      const td = document.createElement("td");
      if ([0, 4, 7, 8, 9].includes(index)) td.className = "number";
      if (index === 0 || index === 1) {
        const a = document.createElement("a");
        a.href = "index.html#" + encodeURIComponent(row.desired_id);
        a.textContent = value;
        td.append(a);
      } else td.textContent = value;
      tr.append(td);
    });
    body.append(tr);
  }
  document
    .querySelectorAll("[data-key]")
    .forEach((button) =>
      button.parentElement.setAttribute(
        "aria-sort",
        button.dataset.key === key
          ? direction === 1
            ? "ascending"
            : "descending"
          : "none",
      ),
    );
}
document.getElementById("search").addEventListener("input", render);
document.querySelectorAll("[data-key]").forEach((button) =>
  button.addEventListener("click", () => {
    direction = key === button.dataset.key ? -direction : 1;
    key = button.dataset.key;
    render();
  }),
);
try {
  const response = await fetch("palletize_corpus.json");
  if (!response.ok) throw Error("Unable to load historical corpus");
  const data = await response.json();
  rows = data.rows;
  render();
} catch (error) {
  document.getElementById("message").textContent = error.message;
}
