# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
"""Verify the reusable engineering standards template contract."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = '.agents/skills'
SKILL_REGISTRY = '.agents/skills/README.md'
SKILL_NAME_RE = re.compile(r'[a-z][a-z0-9-]*')
ROLE_ASSIGNMENT_RE = re.compile(
    r'(?i)\b(?:gpt|claude|codex|deepseek|dsh)\b\s*(?:is|as|acts as|serves as|负责|担任|=|:)\s*'
    r'(?:planner|implementer|reviewer|规划|开发|审核|审查)\b'
)
ROOT_AGENT_SECTIONS = (
    'Before changing code', 'Engineering rules', 'Delivery boundaries',
    'Quality commands', 'Reusable workflows',
)
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
    SKILL_REGISTRY, 'docs/agent-governance.md',
]

def _parse_skill_metadata(body):
    """Return (name, description, content) from the supported SKILL.md header."""
    match = re.match(
        r'\A---\r?\nname: ([a-z][a-z0-9-]*)\r?\ndescription: ([^\r\n]+)\r?\n---\r?\n',
        body,
    )
    if not match:
        return None
    return match.group(1), match.group(2).strip(), body[match.end():]


def verify_agent_instructions(root, errors):
    """Verify the instruction hierarchy and agent-neutral compatibility entry points."""
    agent_file = root / 'AGENTS.md'
    if agent_file.is_file():
        body = agent_file.read_text(encoding='utf-8')
        for section in ROOT_AGENT_SECTIONS:
            if not re.search(rf'(?m)^## {re.escape(section)}\s*(?=\r?\n|\Z)', body):
                errors.append(f'AGENTS.md missing required section: {section}')
        if len(body.splitlines()) > 120:
            errors.append('AGENTS.md is no longer a concise standing-order entry point')
        if ROLE_ASSIGNMENT_RE.search(body):
            errors.append('AGENTS.md assigns fixed roles to a model or agent')
    claude_file = root / 'CLAUDE.md'
    if claude_file.is_file():
        body = claude_file.read_text(encoding='utf-8')
        if 'AGENTS.md' not in body:
            errors.append('CLAUDE.md must point to the shared AGENTS.md source')
        if 'shared source of repository rules' not in body:
            errors.append('CLAUDE.md must declare AGENTS.md as the shared rule source')
        if ROLE_ASSIGNMENT_RE.search(body):
            errors.append('CLAUDE.md assigns fixed roles to a model or agent')
        if len(body.splitlines()) > 40:
            errors.append('CLAUDE.md compatibility entry point is too large; keep engineering rules in AGENTS.md')
    return errors


def verify_skills(root, errors):
    """Discover every project Skill and verify metadata plus the canonical registry."""
    skills_root = root / SKILL_ROOT
    registry = root / SKILL_REGISTRY
    if not skills_root.is_dir():
        errors.append(f'Missing: {SKILL_ROOT}')
        return errors
    if not registry.is_file():
        errors.append(f'Missing: {SKILL_REGISTRY}')
        return errors

    discovered = {}
    for entry in sorted(skills_root.iterdir(), key=lambda item: item.name):
        if not entry.is_dir():
            continue
        if not SKILL_NAME_RE.fullmatch(entry.name):
            errors.append(f'Invalid Skill directory name: {entry.relative_to(root).as_posix()}')
            continue
        skill_file = entry / 'SKILL.md'
        if not skill_file.is_file():
            errors.append(f'Skill directory missing SKILL.md: {entry.relative_to(root).as_posix()}')
            continue
        body = skill_file.read_text(encoding='utf-8')
        metadata = _parse_skill_metadata(body)
        rel = skill_file.relative_to(root).as_posix()
        if metadata is None:
            errors.append(f'Bad skill metadata: {rel}')
            continue
        name, description, content = metadata
        if name != entry.name:
            errors.append(f'Skill name does not match directory: {rel}')
        if not description:
            errors.append(f'Skill description is empty: {rel}')
        if not content.strip() or not re.search(r'(?m)^# .+\S.*(?=\r?\n|\Z)', content):
            errors.append(f'Skill body must contain a non-empty level-1 heading: {rel}')
        if ROLE_ASSIGNMENT_RE.search(body):
            errors.append(f'Skill assigns fixed roles to a model or agent: {rel}')
        discovered[entry.name] = rel

    registry_body = registry.read_text(encoding='utf-8')
    registry_pattern = re.compile(
        r'(?m)^\s*-\s+\[([a-z][a-z0-9-]*)\]\(([^)]+)\)\s+—\s+(.+?)\s*(?=\r?\n|\Z)'
    )
    registered = {}
    for name, target, description in registry_pattern.findall(registry_body):
        if name in registered:
            errors.append(f'Duplicate Skill registry entry: {name}')
        registered[name] = target
        expected = f'{name}/SKILL.md'
        if target.split('#', 1)[0] != expected:
            errors.append(f'Skill registry target mismatch: {name} => {target}')
        if not description.strip():
            errors.append(f'Skill registry description is empty: {name}')

    missing = sorted(set(discovered) - set(registered))
    orphaned = sorted(set(registered) - set(discovered))
    for name in missing:
        errors.append(f'Skill missing from registry: {name}')
    for name in orphaned:
        errors.append(f'Skill registry points to missing directory: {name}')
    return errors


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
        for href in re.findall(r'!?\[[^]]*\]\(([^)]+)\)', body):
            link = href.split('#', 1)[0].split('?', 1)[0].split(' "', 1)[0]
            if not link or link.startswith(('https:', 'http:', 'mailto:')):
                continue
            location = (file.parent / unquote(link)).resolve()
            if not location.is_relative_to(root) or not location.exists():
                errors.append(f'Broken/unsafe link: {rel} => {href}')
    verify_agent_instructions(root, errors)
    verify_skills(root, errors)
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
