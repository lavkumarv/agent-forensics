## Summary

What does this change and why?

## Checklist

- [ ] `make check` passes (ruff, mypy --strict, pytest)
- [ ] Core-package coverage stays at or above 90%
- [ ] New code has tests
- [ ] The ledger remains **append-only** (no UPDATE/DELETE of ledger rows)
- [ ] Reads are still logged as first-class events
- [ ] Commits are signed off (DCO): `git commit -s`

## Notes for reviewers

Anything reviewers should focus on, trade-offs, or follow-ups.
