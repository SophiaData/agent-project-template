# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
"""Execute declared quality gates, optionally selecting checks from a Git diff."""
import argparse
from functools import lru_cache
import fnmatch
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE_EXTENSIONS = {'.py', '.ipynb', '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs',
                     '.sql', '.hql', '.hive', '.ddl', '.dml', '.java', '.scala', '.kt',
                     '.go', '.rs', '.sh', '.rb', '.r', '.php', '.cs', '.cpp', '.c',
                     '.h', '.hpp'}
SKIP_DIRECTORIES = {'.git', '.github', '.agents', '.venv', 'venv', 'node_modules',
                    'dist', 'build', 'target', 'coverage', '__pycache__',
                    '.pytest_cache', '.mypy_cache', '.next', '.nuxt', 'vendor', 'docs'}
TEMPLATE_TOOLS = {'scripts/run_quality.py', 'scripts/verify_project.py',
                  'scripts/configure_project.py', 'tests/test_template_contract.py'}
ALLOWED_CATEGORIES = {'test', 'lint', 'typecheck', 'build', 'sql'}
PLACEHOLDERS = {'PROJECT_NAME', 'PROJECT_TYPE'}
ALLOWED_CHECK_KEYS = {'category', 'argv', 'paths'}


def has_application_code(root=ROOT):
    for current, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRECTORIES]
        for name in names:
            file = Path(current) / name
            if file.suffix.lower() not in SOURCE_EXTENSIONS:
                continue
            if file.relative_to(root).as_posix() not in TEMPLATE_TOOLS:
                return True
    return False


def validate_paths(paths, index):
    """Validate relative POSIX glob patterns used to select a quality check."""
    if not isinstance(paths, list) or not paths:
        raise ValueError(f'quality_checks[{index}].paths must be a nonempty array')
    for pattern in paths:
        if not isinstance(pattern, str) or not pattern.strip():
            raise ValueError(f'quality_checks[{index}].paths must contain nonempty strings')
        if pattern.startswith('/') or '\\' in pattern or '\0' in pattern:
            raise ValueError(f'quality_checks[{index}].paths must use relative POSIX patterns')
        parts = pattern.split('/')
        if any(part in {'', '.', '..'} for part in parts):
            raise ValueError(f'quality_checks[{index}].paths contains an unsafe path segment')
        if any('**' in part and part != '**' for part in parts):
            raise ValueError(f'quality_checks[{index}].paths must use ** as a complete path segment')


def validate_policy(policy, has_code):
    if policy.get('schema_version') != 2:
        raise ValueError('schema_version must be 2')
    if policy.get('release_mode') != 'manual' or policy.get('require_checks_when_code_exists') is not True:
        raise ValueError('release_mode must be manual and source checks mandatory')
    commands = policy.get('quality_checks')
    if not isinstance(commands, list):
        raise ValueError('quality_checks must be an array')
    kinds = set()
    for i, entry in enumerate(commands):
        if (not isinstance(entry, dict) or not {'category', 'argv'}.issubset(entry)
                or not set(entry).issubset(ALLOWED_CHECK_KEYS)):
            raise ValueError(f'quality_checks[{i}] must contain category and argv, with optional paths')
        kind, argv = entry['category'], entry['argv']
        if not isinstance(kind, str) or kind not in ALLOWED_CATEGORIES:
            raise ValueError(f'quality_checks[{i}] has unsupported category')
        if not isinstance(argv, list) or not argv or not all(isinstance(a, str) and a for a in argv):
            raise ValueError(f'quality_checks[{i}] argv must contain nonempty tokens')
        if argv[0] in {'true', 'echo', 'printf', ':'} or '-c' in argv:
            raise ValueError(f'quality_checks[{i}] looks like a placeholder/no-op')
        if 'paths' in entry:
            validate_paths(entry['paths'], i)
        kinds.add(kind)
    if has_code:
        if policy.get('project_name') in PLACEHOLDERS or policy.get('project_type') in PLACEHOLDERS:
            raise ValueError('configure project name and type before shipping source')
        if 'test' not in kinds:
            raise ValueError('application source requires at least one test check')
    return commands


def path_matches(path, pattern):
    """Match a Git path against slash-separated globs; ** matches zero or more segments."""
    path_parts = path.split('/')
    pattern_parts = pattern.split('/')

    @lru_cache(maxsize=None)
    def match(path_index, pattern_index):
        if pattern_index == len(pattern_parts):
            return path_index == len(path_parts)
        segment = pattern_parts[pattern_index]
        if segment == '**':
            return (match(path_index, pattern_index + 1)
                    or (path_index < len(path_parts) and match(path_index + 1, pattern_index)))
        return (path_index < len(path_parts)
                and fnmatch.fnmatchcase(path_parts[path_index], segment)
                and match(path_index + 1, pattern_index + 1))

    return match(0, 0)


def get_changed_paths(base, head='HEAD', root=ROOT):
    """Return both sides of renames by disabling rename detection in the Git diff."""
    if (not isinstance(base, str) or not base or base.startswith('-')
            or base.strip() != base or any(char.isspace() for char in base) or '\0' in base):
        raise ValueError('base must be a nonempty Git ref or commit SHA')
    if not isinstance(head, str) or not head or head.startswith('-'):
        raise ValueError('head must be a nonempty Git ref or commit SHA')
    revision = f'{base}...{head}'
    result = subprocess.run(
        ['git', 'diff', '--no-ext-diff', '--no-renames', '--name-only', '-z', revision, '--'],
        cwd=root, check=False, capture_output=True, text=True, encoding='utf-8',
        errors='surrogateescape',
    )
    if result.returncode:
        detail = result.stderr.strip() or f'exit code {result.returncode}'
        raise ValueError(f'cannot resolve Git change scope for {revision}: {detail}')
    return sorted({path for path in result.stdout.split('\0') if path})


def select_checks(commands, changed_paths=None, has_code=False):
    """Select path-scoped checks; unscoped checks always run."""
    if changed_paths is None:
        return list(commands)
    selected = [
        check for check in commands
        if 'paths' not in check
        or any(path_matches(path, pattern)
               for path in changed_paths for pattern in check['paths'])
    ]
    source_changed = any(Path(path).suffix.lower() in SOURCE_EXTENSIONS for path in changed_paths)
    if has_code and source_changed and not any(check['category'] == 'test' for check in selected):
        raise ValueError(
            'application source files changed but no test check matched; '
            'add the source/test paths to a test check or run without --base'
        )
    return selected


def main(argv=None):
    parser = argparse.ArgumentParser(description='Run configured quality checks')
    parser.add_argument(
        '--base',
        help='select path-scoped checks changed from BASE...HEAD; omit to run all configured checks',
    )
    args = parser.parse_args(argv)

    policy = json.loads((ROOT / 'project-policy.json').read_text(encoding='utf-8'))
    code_exists = has_application_code()
    commands = validate_policy(policy, code_exists)
    changed = get_changed_paths(args.base) if args.base else None
    selected = select_checks(commands, changed, code_exists)

    if changed is not None:
        print(f'Git change scope: {len(changed)} changed path(s) from {args.base}...HEAD')
        print(f'Selected {len(selected)} of {len(commands)} configured quality check(s).')
        for check in commands:
            if check not in selected and 'paths' in check:
                print(f"Skipping [{check['category']}]: no changed path matched {check['paths']}")

    if not selected:
        if changed is None:
            print('No application source yet: governance-only template stage; no tests claimed.')
        else:
            print('No configured checks matched the changed paths; no tests are claimed.')
        return 0

    for i, check in enumerate(selected, 1):
        argv = check['argv']
        print(f"Running {i}/{len(selected)} [{check['category']}]: {argv[0]}", flush=True)
        try:
            result = subprocess.run(argv, cwd=ROOT, check=False, timeout=600)
        except (OSError, subprocess.TimeoutExpired) as exc:
            sys.exit(f'ERROR: check {i} could not complete: {exc}')
        if result.returncode:
            sys.exit(f'ERROR: check {i} returned {result.returncode}')
    print(f'{len(selected)} selected checks passed; meaning of checks still requires review.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        sys.exit(f'ERROR: {error}')
