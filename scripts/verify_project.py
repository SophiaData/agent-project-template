# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
"""Verify the V2 project governance contract, not application behavior."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'AGENTS.md', 'CLAUDE.md', 'README.md', 'TEMPLATE_VERSION',
    'docs/architecture.md', 'docs/development.md', 'docs/testing.md',
    'docs/template-upgrades.md', '.github/pull_request_template.md',
    '.github/workflows/quality.yml', 'project-policy.json',
    '.agents/skills/project-plan/SKILL.md',
    '.agents/skills/project-implement/SKILL.md',
    '.agents/skills/project-review/SKILL.md',
    '.agents/skills/project-pre-pr/SKILL.md',
]


def verify(root=ROOT):
    errors = []
    for rel in REQUIRED:
        file = root / rel
        if not file.is_file():
            errors.append(f'Missing: {rel}')
            continue
        body = file.read_text(encoding='utf-8')
        if rel.endswith('/SKILL.md'):
            match = re.match(r'\A---\r?\nname: ([a-z][a-z0-9-]*)\r?\ndescription: ([^\r\n]+)\r?\n---\r?\n', body)
            if not match or match.group(1) != file.parent.name:
                errors.append(f'Bad skill metadata: {rel}')
        for href in re.findall(r'!?\[[^]]*\]\(([^)]+)\)', body):
            link = href.split('#', 1)[0].split('?', 1)[0].split(' "', 1)[0]
            if not link or link.startswith(('https:', 'http:', 'mailto:')):
                continue
            location = (file.parent / unquote(link)).resolve()
            if not location.is_relative_to(root.resolve()) or not location.exists():
                errors.append(f'Broken/unsafe link: {rel} => {href}')
    try:
        policy = json.loads((root / 'project-policy.json').read_text(encoding='utf-8'))
        version = (root / 'TEMPLATE_VERSION').read_text(encoding='utf-8').strip()
        if policy.get('schema_version') != 2 or policy.get('template_version') != version:
            errors.append('project-policy.json schema/template version mismatch')
        if policy.get('release_mode') != 'manual' or policy.get('require_checks_when_code_exists') is not True:
            errors.append('Manual release / mandatory checks cannot be disabled')
        if not isinstance(policy.get('quality_checks'), list):
            errors.append('quality_checks must be an array')
    except (OSError, ValueError) as exc:
        errors.append(f'Invalid policy or version: {exc}')
    return errors


if __name__ == '__main__':
    failures = verify()
    for error in failures:
        print('ERROR:', error, file=sys.stderr)
    if failures:
        sys.exit(1)
    print(f'Governance verified: {len(REQUIRED)} required files')
