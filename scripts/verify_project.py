# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
"""Verify the reusable engineering standards template contract."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DEFENSIVE_PATTERN_FILES = (
    'docs/defensive-patterns/general.md',
    'docs/defensive-patterns/data-engineering.md',
)
PATTERN_SUBSECTIONS = (
    'Applies when',
    'Required invariant',
    'Failure prevented',
    'Evidence',
    'Boundary and exception',
    'Incorrect example',
    'Correct example',
    'Enforcement',
)
REQUIRED = [
    'AGENTS.md', 'CLAUDE.md', 'CONTRIBUTING.md', 'README.md', 'TEMPLATE_VERSION',
    'docs/AGENTS.md', 'docs/architecture.md', 'docs/development.md',
    'docs/coding-standards.md', 'docs/testing.md', 'docs/error-handling.md',
    'docs/documentation.md', 'docs/compatibility.md', 'docs/git-workflow.md',
    'docs/template-upgrades.md', 'docs/decisions/README.md',
    'docs/decisions/template.md', 'docs/standards/README.md',
    'docs/standards/python.md', 'docs/standards/typescript.md',
    'docs/standards/java.md', 'docs/standards/data-engineering.md',
    'docs/defensive-patterns/README.md',
    *DEFENSIVE_PATTERN_FILES,
    '.github/pull_request_template.md', '.github/workflows/quality.yml',
    'project-policy.json',
    '.agents/skills/project-plan/SKILL.md',
    '.agents/skills/project-implement/SKILL.md',
    '.agents/skills/project-review/SKILL.md',
    '.agents/skills/project-pre-pr/SKILL.md',
    '.agents/skills/project-doc-writing/SKILL.md',
    '.agents/skills/project-error-handling/SKILL.md',
    '.agents/skills/project-simplification/SKILL.md',
    '.agents/skills/project-upgrade-guide/SKILL.md',
]


def verify_defensive_patterns(root, errors):
    """Require each defensive-pattern rule to carry the reviewable contract sections."""
    for rel in DEFENSIVE_PATTERN_FILES:
        file = root / rel
        if not file.is_file():
            continue  # The required-file check reports the missing document.
        body = file.read_text(encoding='utf-8')
        headings = list(re.finditer(r'(?m)^## (.+?)\s*$', body))
        if not headings:
            errors.append(f'Defensive patterns contain no rules: {rel}')
            continue
        for index, heading in enumerate(headings):
            end = headings[index + 1].start() if index + 1 < len(headings) else len(body)
            section = body[heading.end():end]
            for required in PATTERN_SUBSECTIONS:
                pattern = rf'(?m)^### {re.escape(required)}\s*$'
                if not re.search(pattern, section):
                    errors.append(
                        f'Defensive pattern missing subsection "{required}": {rel} / {heading.group(1)}'
                    )
    return errors


def verify(root=ROOT):
    errors = []
    root = root.resolve()
    for rel in REQUIRED:
        file = root / rel
        if not file.is_file():
            errors.append(f'Missing: {rel}')
            continue
        body = file.read_text(encoding='utf-8')
        if rel.endswith('/SKILL.md'):
            match = re.match(
                r'\A---\r?\nname: ([a-z][a-z0-9-]*)\r?\ndescription: ([^\r\n]+)\r?\n---\r?\n',
                body,
            )
            if not match or match.group(1) != file.parent.name:
                errors.append(f'Bad skill metadata: {rel}')
        for href in re.findall(r'!?\[[^]]*\]\(([^)]+)\)', body):
            link = href.split('#', 1)[0].split('?', 1)[0].split(' "', 1)[0]
            if not link or link.startswith(('https:', 'http:', 'mailto:')):
                continue
            location = (file.parent / unquote(link)).resolve()
            if not location.is_relative_to(root) or not location.exists():
                errors.append(f'Broken/unsafe link: {rel} => {href}')
    verify_defensive_patterns(root, errors)
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
