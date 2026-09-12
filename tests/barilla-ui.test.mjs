import test from "node:test";
import assert from "node:assert/strict";
import {
  sortRows,
  destinationLabel,
  arrowDelta,
  formatFlags,
} from "../barilla-ui.mjs";
test("unknown metrics remain last in either direction", () => {
  for (const direction of [1, -1])
    assert.equal(
      sortRows(
        [
          { id: "a", compute_s: null },
          { id: "b", compute_s: 2 },
        ],
        "compute",
        direction,
      )[1].id,
      "a",
    );
});
test("box order follows pallet, box and original task order", () =>
  assert.deepEqual(
    sortRows(
      [
        { id: "c", place_pallet: "pallet-B", box_number: 1, task_id: 1 },
        { id: "b", place_pallet: "pallet-A", box_number: 2, task_id: 2 },
        { id: "a", place_pallet: "pallet-A", box_number: 2, task_id: 1 },
      ],
      "box",
    ).map((r) => r.id),
    ["a", "b", "c"],
  ));
test("destination uses final tagged operation", () => {
  assert.equal(destinationLabel("MoveToPick"), "to-pick-point");
  assert.equal(destinationLabel("MoveToWait"), "to wait node");
  assert.equal(
    destinationLabel("MoveToExit,MoveToNext,MoveToPlace"),
    "to-place",
  );
});
test("arrows respect editors and modifiers", () => {
  assert.equal(arrowDelta({ key: "ArrowDown", target: { tagName: "DIV" } }), 1);
  for (const target of [
    { tagName: "INPUT" },
    { tagName: "TEXTAREA" },
    { tagName: "SELECT" },
    { isContentEditable: true },
  ])
    assert.equal(arrowDelta({ key: "ArrowUp", target }), 0);
  assert.equal(arrowDelta({ key: "ArrowDown", ctrlKey: true, target: {} }), 0);
});
test("box cycles put following wait and pick after the preceding placement", () => {
  const rows = [
    {
      id: "p4",
      task_id: 2,
      tag: "MoveToPlace",
      box_number: 4,
      place_pallet: "pallet-A",
    },
    {
      id: "w",
      task_id: 3,
      tag: "MoveToWait",
      box_number: 4,
      place_pallet: "pallet-A",
    },
    {
      id: "pick",
      task_id: 4,
      tag: "MoveToPick",
      box_number: 5,
      place_pallet: "pallet-A",
    },
    {
      id: "p5",
      task_id: 5,
      tag: "MoveToPlace",
      box_number: 5,
      place_pallet: "pallet-A",
    },
  ];
  assert.deepEqual(
    sortRows(rows, "box").map((r) => r.id),
    ["p4", "w", "pick", "p5"],
  );
  assert.deepEqual(
    sortRows(rows, "box", -1).map((r) => r.id),
    ["p5", "p4", "w", "pick"],
  );
});
test("cycle association uses chronology across pallet transition", () => {
  const rows = [
    {
      id: "a",
      task_id: 1,
      tag: "MoveToPlace",
      box_number: 20,
      place_pallet: "pallet-A",
    },
    {
      id: "pick",
      task_id: 2,
      tag: "MoveToPick",
      box_number: 1,
      place_pallet: "pallet-B",
    },
    {
      id: "b",
      task_id: 3,
      tag: "MoveToPlace",
      box_number: 1,
      place_pallet: "pallet-B",
    },
  ];
  assert.deepEqual(
    sortRows(rows, "box", -1).map((r) => r.id),
    ["b", "a", "pick"],
  );
});

test("historical object flags display their codes", () => {
  assert.equal(
    formatFlags([
      { code: "slow_compute", compute_s: 83.04, severity: "yellow" },
    ]),
    "slow_compute",
  );
  assert.equal(
    formatFlags([
      { code: "not_solved", status: "IN_PROGRESS", severity: "red" },
    ]),
    "not_solved",
  );
  assert.equal(formatFlags([]), "—");
});
