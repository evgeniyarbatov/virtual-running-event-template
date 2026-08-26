# Roadmap

## Why keep going

A template only pays for itself once instances stop drifting from it. Right now, fixing something here doesn't reach `[private]` or `[private]`/`[private]` unless it's redone by hand in each. This repo is the leverage point for all of them at once, or it's nothing more than the first copy.

## What it opens up

A real scaffold command (`make new-event NAME=...`) turns "start a new symbolic-route event" from a multi-day repo build into a five-minute setup. That's what makes an idea like `[private]`'s own Mars-rover-route brainstorm actually cheap enough to try instead of staying a TODO comment forever.

## Capability this builds

Template-driven development — designing for reuse before the second copy exists, not patching it in after the third one has already drifted.

## Connects to

- **[private]**, **[private]**, **[private]** — the known instances (or near-instances) of this shape; a CI pass here should backport to all three.

---

## Prior notes

# Roadmap

A template repo: config-driven static site + route pipeline (GPX → polyline/stats → progress marker) for a virtual running event, deployed to S3 via Terraform. `[private]` and `[private]` are instances derived from this shape.

## Near-term

- Add CI to run the existing tests on push, then backport to the instances derived from this template.
- Since at least two repos already copy this template by hand, consider whether a `make new-event NAME=...` scaffold step (copy + rename + fresh git history) is worth adding here so instances stay in sync with template fixes.
