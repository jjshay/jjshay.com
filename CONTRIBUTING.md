# Contributing and maintaining this project

Start with [the project brief](docs/PROJECT_BRIEF.md) and the existing setup instructions in [README.md](README.md).

1. Make one coherent change on a branch. Preserve existing operational behavior unless the change explicitly targets it.
2. Use fixture or sample data. Keep credentials, browser profiles, customer records, recordings, and generated operational exports outside Git.
3. Run the checks appropriate to the changed behavior. State exactly what ran and what needs external credentials or hardware.
4. Update `project.json` and `docs/PROJECT_BRIEF.md` when architecture, setup, status, or limitations change. Link to concrete source files and dated evidence.
5. Run `python3 scripts/check_project_docs.py` before opening a pull request.

A project is documented when another reader can explain its purpose, follow the implementation, identify configuration requirements, reproduce the available checks, and distinguish observed behavior from intended outcomes. Avoid unsupported production, accuracy, revenue, or performance claims. See the brief's next improvements for scoped follow-up work.
