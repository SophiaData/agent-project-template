# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
"""Configure a GitHub-generated project without overwriting custom policy."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def detect_stack(root):
    matches = set()
    if any((root / x).exists() for x in ('pyproject.toml', 'requirements.txt', 'pytest.ini')):
        matches.add('python')
    if (root / 'package.json').exists():
        matches.add('node')
    if any((root / x).exists() for x in ('pom.xml', 'build.gradle', 'build.gradle.kts')):
        matches.add('java')
    if any((root / x).exists() for x in ('dbt_project.yml', 'sql', 'flink', 'hive')):
        matches.add('data')
    return matches.pop() if len(matches) == 1 else ('mixed' if matches else 'generic')


def candidate_checks(root, stack):
    if stack == 'node' and (root / 'package.json').is_file():
        manifest = json.loads((root / 'package.json').read_text(encoding='utf-8'))
        test = manifest.get('scripts', {}).get('test', '')
        if test and 'no test specified' not in test.lower():
            manager = 'pnpm' if (root / 'pnpm-lock.yaml').exists() else 'npm'
            return [{'category': 'test', 'argv': [manager, 'test']}]
    if stack == 'java' and (root / 'pom.xml').is_file():
        return [{'category': 'test', 'argv': ['mvn', 'test']}]
    return []


def main():
    parser = argparse.ArgumentParser(description='Configure project identity and stack metadata')
    parser.add_argument('--name', required=True)
    parser.add_argument('--stack', choices=['auto', 'generic', 'python', 'node', 'java', 'data', 'mixed'], default='auto')
    parser.add_argument('--apply', action='store_true', help='Write placeholder metadata; otherwise dry-run')
    args = parser.parse_args()
    if not args.name.strip() or '\n' in args.name or '\r' in args.name:
        parser.error('invalid project name')
    path = ROOT / 'project-policy.json'
    policy = json.loads(path.read_text(encoding='utf-8'))
    stack = detect_stack(ROOT) if args.stack == 'auto' else args.stack
    if policy['project_name'] not in ('PROJECT_NAME', args.name):
        parser.error('existing project name differs; edit policy intentionally')
    if policy['project_type'] not in ('PROJECT_TYPE', stack):
        parser.error('existing project type differs; edit policy intentionally')
    policy['project_name'], policy['project_type'] = args.name, stack
    if not policy['quality_checks']:
        policy['quality_checks'] = candidate_checks(ROOT, stack)
    readme_path = ROOT / 'README.md'
    readme = readme_path.read_text(encoding='utf-8')
    print(json.dumps({'name': args.name, 'stack': stack, 'quality_checks': policy['quality_checks'], 'apply': args.apply}, indent=2))
    if args.apply:
        path.write_text(json.dumps(policy, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        if 'PROJECT_NAME' in readme or 'PROJECT_TYPE' in readme:
            readme_path.write_text(readme.replace('PROJECT_NAME', args.name).replace('PROJECT_TYPE', stack), encoding='utf-8')
        print('Project metadata configured; review actual checks and CI runtime before merging.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
