# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
"""Fail closed for real source without configured checks; run checks as argv, not shell."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
policy = json.loads((ROOT / 'project-policy.json').read_text(encoding='utf-8'))
commands = policy.get('quality_commands', [])
source_exts = {
    '.py', '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.sql', '.java',
    '.scala', '.kt', '.go', '.rs', '.sh', '.rb', '.php', '.cs', '.cpp', '.c',
}
# Ignore generated dependencies and the template's own tooling. Traverse all
# other directories, including cmd/, internal/, backend/ and custom sources.
ignored_dirs = {
    '.git', '.github', '.agents', 'node_modules', '.venv', 'venv',
    'dist', 'build', 'target', '__pycache__', '.pytest_cache', '.mypy_cache',
    '.next', '.nuxt', 'coverage', '.tox', 'vendor', 'docs',
}
scaffold_tools = {'scripts/run_quality.py', 'scripts/verify_project.py'}

def has_production_code():
    for file in ROOT.rglob('*'):
        if not file.is_file() or file.suffix.lower() not in source_exts:
            continue
        relative = file.relative_to(ROOT)
        if ignored_dirs.intersection(relative.parts):
            continue
        if relative.as_posix() in scaffold_tools:
            continue
        return True
    return False

production_code = has_production_code()
if not commands:
    if production_code and policy.get('require_checks_when_code_exists', True):
        sys.exit('ERROR: production source detected but quality_commands is empty; configure real checks in project-policy.json')
    print('No production source yet; quality checks not configured. Governance-only stage.')
    sys.exit(0)
for index, command in enumerate(commands, 1):
    if not isinstance(command, list) or not command or not all(isinstance(part, str) and part for part in command):
        sys.exit(f'ERROR: quality_commands[{index - 1}] must be a nonempty array of command tokens')
    print(f'Check {index}/{len(commands)}: {command[0]}', flush=True)
    try:
        result = subprocess.run(command, cwd=ROOT, check=False)
    except OSError as exc:
        sys.exit(f'ERROR: check unavailable: {exc}')
    if result.returncode != 0:
        sys.exit(f'ERROR: check {index} failed with exit code {result.returncode}')
print(f'All {len(commands)} configured quality checks passed.')
