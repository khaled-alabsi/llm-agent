# Agent Notes

- Code must not rely on hidden fallbacks. Behave deterministically and surface errors explicitly.
- Avoid wrapping imports in try/except blocks; missing dependencies should raise immediately.
- Python work expects a `.venv` inside the repository root.
- Always keep the `docs/` index fresh so new contributors can onboard quickly.
