# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
"""Inspect repository instruction chains without changing host runtime behavior.

This is a deterministic project-side preflight, not a replacement for any
host's instruction loader or a claim about a model's actual compliance.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys


PROFILES = {
    # Canonical shared policy + optional project-local additions.
    'shared': (('AGENTS.md',), ('AGENTS.local.md',)),
    # DSH's project candidates; user-global files are deliberately out of scope.
    'dsh': (('AGENTS.md', 'CLAUDE.md'), ('AGENTS.local.md', 'CLAUDE.local.md')),
    # Codex selects the first non-empty candidate in each directory.
    'codex': (('AGENTS.override.md', 'AGENTS.md'), ()),
    # Claude Code loads its own memory entry points; a shim is not auto-expanded.
    'claude': (('CLAUDE.md',), ('CLAUDE.local.md',)),
}
INSTRUCTION_NAMES = frozenset(name for groups in PROFILES.values()
                              for group in groups for name in group)
DEFAULT_BUDGET = 65536


class InstructionChainError(ValueError):
    """An instruction chain cannot be inspected safely."""


def _inside(path, root):
    return path == root or path.is_relative_to(root)


def _source(root, path):
    """Read an instruction file without following a link outside the checkout."""
    if not path.exists() and not path.is_symlink():
        return None
    if not _inside(path.resolve(), root):
        raise InstructionChainError(f'Instruction source escapes project: {path}')
    if not path.is_file():
        raise InstructionChainError(f'Instruction source is not a file: {path}')
    try:
        raw = path.read_bytes()
        body = raw.decode('utf-8')
    except (OSError, UnicodeError) as exc:
        raise InstructionChainError(f'Cannot read UTF-8 instruction source {path}: {exc}') from exc
    if not body.strip():
        return None
    return {
        'path': path.relative_to(root).as_posix(),
        'scope': path.parent.relative_to(root).as_posix(),
        'bytes': len(raw),
        'digest': hashlib.sha256(body.strip().encode('utf-8')).hexdigest(),
        'content': body,
    }


def _scope_dirs(root, target):
    """Resolve a file or existing directory and enumerate root-to-leaf scopes."""
    raw = Path(target)
    if raw.is_absolute():
        raise InstructionChainError('Target must be repository-relative')
    absolute = (root / raw).resolve()
    if not _inside(absolute, root):
        raise InstructionChainError('Target escapes repository root')
    scope = absolute if absolute.is_dir() else absolute.parent
    if not _inside(scope, root):
        raise InstructionChainError('Target parent escapes repository root')
    result = [root]
    cursor = root
    for part in scope.relative_to(root).parts:
        cursor /= part
        result.append(cursor)
    return result


def resolve_chain(root, target='.', profile='shared', max_bytes=DEFAULT_BUDGET,
                  include_content=False):
    """Return ordered sources, suppressed candidates, and explicit limitations."""
    if profile not in PROFILES:
        raise InstructionChainError(f'Unknown profile: {profile}')
    if max_bytes <= 0:
        raise InstructionChainError('max_bytes must be positive')
    root = Path(root).resolve()
    if not root.is_dir():
        raise InstructionChainError('Repository root is not a directory')
    if not (root / 'AGENTS.md').is_file():
        raise InstructionChainError('Repository root AGENTS.md is missing')
    dirs = _scope_dirs(root, target)
    base, local = PROFILES[profile]
    sources, skipped, warnings = [], [], []
    for directory in dirs:
        seen = set()
        candidates = base + local
        for index, name in enumerate(candidates):
            source = _source(root, directory / name)
            if source is None:
                continue
            # Codex uses a replacement candidate within each directory, not
            # DSH-style additive candidates. Empty files do not shadow.
            if profile == 'codex' and sources and sources[-1]['scope'] == source['scope']:
                skipped.append({'path': source['path'], 'reason': 'shadowed-by-override'})
                continue
            # DSH collapses identical content within one candidate group.
            # Other profiles use this as a deterministic preflight convention.
            if source['digest'] in seen:
                skipped.append({'path': source['path'], 'reason': 'duplicate-in-scope'})
                continue
            seen.add(source['digest'])
            if name.endswith('.local.md'):
                warnings.append(f'Local overlay requires manual policy review: {source["path"]}')
            if not include_content:
                source.pop('content')
            sources.append(source)
        if profile == 'codex' and (directory / 'AGENTS.override.md').is_file():
            warnings.append(
                'Codex override may replace shared AGENTS.md in scope: '
                + directory.relative_to(root).as_posix()
            )
    total_bytes = sum(source['bytes'] for source in sources)
    if total_bytes > max_bytes:
        warnings.append(
            f'Visible instruction bytes {total_bytes} exceed requested advisory budget '
            f'{max_bytes}; actual host truncation/omission must be checked in the host'
        )
    if profile == 'claude':
        warnings.append('Claude entry-point text is listed, not expanded into AGENTS.md')
    return {
        'profile': profile,
        'target': Path(target).as_posix(),
        'root': str(root),
        'sources': sources,
        'skipped': skipped,
        'total_bytes': total_bytes,
        'advisory_max_bytes': max_bytes,
        'warnings': warnings,
        'host_verified': False,
    }


def audit_sources(root):
    """Structurally inspect every existing project instruction file.

    Semantic conflicts between different prose rules require a human review.
    Tool-global instructions, runtime delivery and subagent adoption are outside
    this repository verifier's reach.
    """
    root = Path(root).resolve()
    errors = []
    ignored_dirs = {'.git', '.venv', 'venv', 'node_modules', 'dist', 'build',
                    'target', '__pycache__', '.pytest_cache'}
    # Path.walk is Python 3.12+; keep compatible with earlier Python versions.
    import os
    for parent, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in ignored_dirs
                         and not (Path(parent) / d).is_symlink())
        for name in sorted(INSTRUCTION_NAMES.intersection(files)):
            path = Path(parent) / name
            rel = path.relative_to(root).as_posix()
            try:
                source = _source(root, path)
                if source is None:
                    errors.append(f'Empty instruction source: {rel}')
                elif source['bytes'] > 1048576:
                    errors.append(f'Instruction source exceeds 1 MiB: {rel}')
            except InstructionChainError as exc:
                errors.append(str(exc))
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument('--target', default='.', help='Existing directory or relative file path')
    parser.add_argument('--profile', choices=sorted(PROFILES), default='shared')
    parser.add_argument('--max-bytes', type=int, default=DEFAULT_BUDGET)
    parser.add_argument('--include-content', action='store_true',
                        help='Explicitly print loaded text (including local overlays)')
    args = parser.parse_args(argv)
    try:
        result = resolve_chain(args.root, args.target, args.profile,
                               args.max_bytes, args.include_content)
    except InstructionChainError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
