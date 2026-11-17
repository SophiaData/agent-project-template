# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
"""Dependency-free minimum governance validation; not a runtime test."""
from pathlib import Path
from urllib.parse import unquote
import re
import sys
import json

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'AGENTS.md', 'CLAUDE.md', 'docs/architecture.md', 'docs/development.md',
    'docs/testing.md', '.github/pull_request_template.md', 'project-policy.json',
    '.agents/skills/project-plan/SKILL.md',
    '.agents/skills/project-implement/SKILL.md',
    '.agents/skills/project-review/SKILL.md',
    '.agents/skills/project-pre-pr/SKILL.md',
]
errors = []
for relative_path in REQUIRED:
    file = ROOT / relative_path
    if not file.is_file():
        errors.append(f'Missing: {relative_path}')
        continue
    body = file.read_text(encoding='utf-8')
    if relative_path.endswith('/SKILL.md'):
        match = re.match(r'\A---\r?\nname: ([a-z][a-z0-9-]*)\r?\ndescription: ([^\r\n]+)\r?\n---\r?\n', body)
        if not match or match.group(1) != file.parent.name:
            errors.append(f'Invalid skill frontmatter: {relative_path}')
    for link in re.findall(r'!?\[[^]]*\]\(([^)]+)\)', body):
        url = link.split('#', 1)[0].split('?', 1)[0].split(' "', 1)[0]
        if not url or url.startswith(('http:', 'https:', 'mailto:', '#')):
            continue
        target = (file.parent / unquote(url)).resolve()
        try:
            target.relative_to(ROOT)
        except ValueError:
            errors.append(f'Outside repo link: {relative_path}: {url}')
            continue
        if not target.exists():
            errors.append(f'Broken link: {relative_path}: {url}')
try:
    policy = json.loads((ROOT / 'project-policy.json').read_text(encoding='utf-8'))
    if policy.get('release_mode') != 'manual':
        errors.append('release_mode must remain manual')
    if policy.get('require_checks_when_code_exists') is not True:
        errors.append('require_checks_when_code_exists must remain true')
    if not isinstance(policy.get('quality_commands'), list):
        errors.append('quality_commands must be a list')
except (OSError, ValueError) as exc:
    errors.append(f'Invalid project-policy.json: {exc}')
if errors:
    for error in errors:
        print('ERROR:', error, file=sys.stderr)
    sys.exit(1)
print(f'Governance checks passed: {len(REQUIRED)} required files')
