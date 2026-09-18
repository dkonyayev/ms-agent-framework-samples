These rules apply whenever `Documentation/<topic>/plan.md` exists for the work in hand.

## Session start
1. Re-read `plan.md` from disk: Part 0 and Part 1 in full.
2. Load only the §4A sections, runbooks, and test cases referenced by `Next up`. Do not load the whole plan.
3. Before every edit to any planning document, re-read it from disk. Never write from an in-memory copy — the human may have edited it by hand.

## Standing rules
1. No code or file changes outside `Documentation/<topic>/` until a human authorizes the specific task.
2. Work tasks in listed order. On reaching a Human task or a blocked task, stop and report. Exception: AI tasks whose Status is `🟡 Independent` may proceed while a Human task is outstanding.
3. IDs (`T-`, `D-`, `R-`, `TC-`) are permanent: next number, creation order, never renumbered, deleted, or reused. Filenames are never renamed after creation.
4. Part 1 of `plan.md` is the only source of truth for task status. Runbooks and test cases never introduce tasks, decisions, or requirements.
5. Part 4B is append-only.
6. Nothing is deleted. Cancelled work is struck through and marked superseded; obsolete satellites are marked `Superseded`.
7. Any change to the plan triggers review of every linked runbook and test case in the same turn: update or supersede.
8. Any change to a runbook or test case gets a Decision Log entry naming the file.
9. Detail lives in one place. Cross-reference by ID; never duplicate.
10. Values handed back by the human are written into §4A in the same turn. A runbook is never the only place a value lives.
11. A Build task that changes observable behaviour is not Done until its linked test case logs a pass, unless waived by a `D-` entry.
12. Never commit planning documents to git. The human commits.
13. Use the system date for all date fields; if unavailable, ask.