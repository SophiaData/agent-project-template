# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
"""Execute declared quality gates; never infer success from an empty test list."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE_EXTENSIONS = {'.py', '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.sql',
                     '.java', '.scala', '.kt', '.go', '.rs', '.sh', '.rb', '.php',
                     '.cs', '.cpp', '.c', '.h', '.hpp'}
SKIP_DIRECTORIES = {'.git', '.github', '.agents', '.venv', 'venv', 'node_modules',
                    'dist', 'build', 'target', 'coverage', '__pycache__',
                    '.pytest_cache', '.mypy_cache', '.next', '.nuxt', 'vendor', 'docs'}
TEMPLATE_TOOLS = {'scripts/run_quality.py', 'scripts/verify_project.py',
                  'scripts/configure_project.py', 'tests/test_template_contract.py'}
ALLOWED_CATEGORIES = {'test', 'lint', 'typecheck', 'build', 'sql'}
PLACEHOLDERS = {'PROJECT_NAME', 'PROJECT_TYPE'}


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
        if not isinstance(entry, dict) or set(entry) != {'category', 'argv'}:
            raise ValueError(f'quality_checks[{i}] must contain category and argv only')
        kind, argv = entry['category'], entry['argv']
        if kind not in ALLOWED_CATEGORIES:
            raise ValueError(f'quality_checks[{i}] has unsupported category')
        if not isinstance(argv, list) or not argv or not all(isinstance(a, str) and a for a in argv):
            raise ValueError(f'quality_checks[{i}] argv must contain nonempty tokens')
        # Obvious no-op checks must not count as test evidence. This is not a
        # semantic proof that an arbitrary test command is meaningful.
        if argv[0] in {'true', 'echo', 'printf', ':'} or '-c' in argv:
            raise ValueError(f'quality_checks[{i}] looks like a placeholder/no-op')
        kinds.add(kind)
    if has_code:
        if policy.get('project_name') in PLACEHOLDERS or policy.get('project_type') in PLACEHOLDERS:
            raise ValueError('configure project name and type before shipping source')
        if 'test' not in kinds:
            raise ValueError('application source requires at least one test check')
    return commands


def main():
    policy = json.loads((ROOT / 'project-policy.json').read_text(encoding='utf-8'))
    commands = validate_policy(policy, has_application_code())
    if not commands:
        print('No application source yet: governance-only template stage; no tests claimed.')
        return 0
    for i, check in enumerate(commands, 1):
        argv = check['argv']
        print(f"Running {i}/{len(commands)} [{check['category']}]: {argv[0]}", flush=True)
        try:
            result = subprocess.run(argv, cwd=ROOT, check=False, timeout=600)
        except (OSError, subprocess.TimeoutExpired) as exc:
            sys.exit(f'ERROR: check {i} could not complete: {exc}')
        if result.returncode:
            sys.exit(f'ERROR: check {i} returned {result.returncode}')
    print(f'{len(commands)} configured checks passed; meaning of checks still requires review.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        sys.exit(f'ERROR: {error}')
