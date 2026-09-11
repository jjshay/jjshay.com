"""Validate the repository's project brief and machine-readable evidence index."""
import json
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
errors = []
def check(condition, message):
    if not condition:
        errors.append(message)
try:
    project = json.loads((root / "project.json").read_text())
    brief = (root / "docs/PROJECT_BRIEF.md").read_text()
    readme = (root / "README.md").read_text()
    for key in ("schema_version", "name", "title", "category", "summary", "status", "reviewed_on", "evidence", "validation", "limitations"):
        check(bool(project.get(key)), f"Missing project field: {key}")
    check(project.get("schema_version") == 1, "Unsupported schema version")
    check(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", project.get("reviewed_on", ""))), "Review date must be YYYY-MM-DD")
    headings = ['At a glance', 'Problem and intended value', 'Architecture and data flow', 'Implementation evidence', 'Setup and operation', 'Validation and outcomes', 'Decisions and limitations', 'Interview talking points', 'Next improvements', 'Related projects']
    for heading in headings:
        marker = "## " + heading + "\n"
        check(marker in brief, f"Missing brief heading: {heading}")
        if marker in brief:
            body = brief.split(marker, 1)[1].split("\n## ", 1)[0].strip()
            check(len(body) >= 20, f"Empty brief section: {heading}")
    check("docs/PROJECT_BRIEF.md" in readme, "README must link to project brief")
    for evidence in project.get("evidence", []):
        path = evidence.get("path", "")
        check(bool(path) and not Path(path).is_absolute() and ".." not in Path(path).parts, f"Invalid evidence path: {path}")
        target = root / path
        check(target.is_file(), f"Missing evidence file: {path}")
        check(bool(evidence.get("role")), f"Missing evidence role: {path}")
    for link in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", brief):
        if link.startswith(("https://", "http://", "mailto:", "#")):
            continue
        from urllib.parse import unquote
        target = (root / "docs" / unquote(link.split("#", 1)[0])).resolve()
        check(target.is_relative_to(root), f"Link escapes repository: {link}")
        check(target.exists(), f"Broken brief link: {link}")
except (OSError, ValueError, TypeError, KeyError) as exc:
    errors.append(str(exc))
if errors:
    print("Project documentation check failed:\n" + "\n".join("- " + e for e in errors))
    sys.exit(1)
print(f"Project documentation valid: {project['name']}")
