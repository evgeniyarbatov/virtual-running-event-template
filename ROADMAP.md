# Roadmap

A template repo: config-driven static site + route pipeline (GPX → polyline/stats → progress marker) for a virtual running event, deployed to S3 via Terraform. `[private]` and `[private]` are instances derived from this shape.

## Near-term

- Add CI to run the existing tests on push, then backport to the instances derived from this template.
- Since at least two repos already copy this template by hand, consider whether a `make new-event NAME=...` scaffold step (copy + rename + fresh git history) is worth adding here so instances stay in sync with template fixes.
