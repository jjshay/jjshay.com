"""Validate project metadata, required sections, and local documentation links."""
import datetime
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote, urlsplit

HEADINGS = ['At a glance', 'Problem and intended value', 'Architecture and data flow', 'Implementation evidence', 'Setup and operation', 'Validation and outcomes', 'Decisions and limitations', 'Interview talking points', 'Next improvements', 'Related projects']

def validate(root):
    root = Path(root).resolve()
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
    def local_target(path, base, label, file_only=False):
        path = unquote(path)
        parts = PurePosixPath(path)
        if not path or parts.is_absolute() or '\\' in path:
            errors.append(f'Invalid local path in {label}: {path}')
            return
        target = (base / path).resolve()
        if not target.is_relative_to(root):
            errors.append(f'Path escapes repository in {label}: {path}')
        else:
            check(target.is_file() if file_only else target.exists(), f'Missing local target in {label}: {path}')
    try:
        project = json.loads((root / 'project.json').read_text())
        if not isinstance(project, dict):
            return ['project.json must be an object']
        check(type(project.get('schema_version')) is int and project['schema_version'] == 1, 'Unsupported schema version')
        for key in ('name', 'title', 'category', 'summary', 'status', 'reviewed_on', 'validation', 'limitations'):
            check(isinstance(project.get(key), str) and bool(project[key].strip()), f'Field must be a nonempty string: {key}')
        try:
            date = project.get('reviewed_on', '')
            check(bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', date)) and datetime.date.fromisoformat(date) <= datetime.date.today(), 'Invalid or future review date')
        except (ValueError, TypeError):
            errors.append('Review date must be a valid YYYY-MM-DD date')
        evidence = project.get('evidence')
        check(isinstance(evidence, list) and bool(evidence), 'Evidence must be a nonempty list')
        if isinstance(evidence, list):
            for item in evidence:
                if not isinstance(item, dict):
                    errors.append('Evidence entries must be objects')
                    continue
                path = item.get('path')
                check(isinstance(item.get('role'), str) and bool(item['role'].strip()), 'Evidence role must be a nonempty string')
                if isinstance(path, str):
                    local_target(path, root, 'evidence', file_only=True)
                else:
                    errors.append('Evidence path must be a string')
        brief = (root / 'docs/PROJECT_BRIEF.md').read_text()
        for heading in HEADINGS:
            marker = '## ' + heading + '\n'
            check(marker in brief, f'Missing brief heading: {heading}')
            if marker in brief:
                check(len(brief.split(marker, 1)[1].split('\n## ', 1)[0].strip()) >= 20, f'Empty brief section: {heading}')
        readme = (root / 'README.md').read_text()
        check('docs/PROJECT_BRIEF.md' in readme, 'README must link to project brief')
        for filename in ('README.md', 'docs/PROJECT_BRIEF.md', 'CONTRIBUTING.md'):
            document = root / filename
            source = document.read_text()
            source = re.sub(r'^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$', '', source, flags=re.M | re.S)
            # Inline links/images and reference destinations; external URLs are not fetched.
            targets = re.findall(r'\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+"[^"\n]*")?\s*\)', source)
            targets += re.findall(r'^\s*\[[^\]]+\]:\s*(<[^>]+>|\S+)', source, flags=re.M)
            for target in targets:
                target = target.strip('<>')
                if target.startswith('#'):
                    continue
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc:
                    check(parsed.scheme in ('https', 'http', 'mailto') and not target.startswith('//'), f'Unsupported link in {filename}: {target}')
                    continue
                if parsed.path:
                    local_target(parsed.path, document.parent, filename)
    except (OSError, ValueError, TypeError, KeyError, RuntimeError) as exc:
        errors.append(str(exc))
    return errors

if __name__ == '__main__':
    failures = validate(Path(__file__).resolve().parents[1])
    if failures:
        print('Project documentation check failed:\n' + '\n'.join('- ' + e for e in failures))
        sys.exit(1)
    print('Project documentation valid')
