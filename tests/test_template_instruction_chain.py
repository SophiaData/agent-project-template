# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
"""Instruction-chain preflight regression and negative-control tests."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'template_instruction_chain', ROOT / 'scripts/instruction_chain.py'
)
chain = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chain)


class InstructionChainContract(unittest.TestCase):
    def make_root(self, path):
        root = Path(path)
        (root / 'AGENTS.md').write_text('# Repository-wide rules\n', encoding='utf-8')
        return root

    def test_nested_scope_order_and_unrelated_siblings(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(temporary)
            for folder in ('docs', 'docs/deep', 'src'):
                (root / folder).mkdir(parents=True)
                (root / folder / 'AGENTS.md').write_text(
                    '# ' + folder + ' rules\n', encoding='utf-8'
                )
            result = chain.resolve_chain(root, 'docs/deep/page.md')
            self.assertEqual(
                [entry['path'] for entry in result['sources']],
                ['AGENTS.md', 'docs/AGENTS.md', 'docs/deep/AGENTS.md'],
            )
            self.assertFalse(result['host_verified'])
            self.assertNotIn('content', result['sources'][0])

    def test_existing_directory_scope_includes_its_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(temporary)
            (root / 'api').mkdir()
            (root / 'api/AGENTS.md').write_text('API rules\n', encoding='utf-8')
            result = chain.resolve_chain(root, 'api')
            self.assertEqual([s['path'] for s in result['sources']],
                             ['AGENTS.md', 'api/AGENTS.md'])

    def test_local_overlay_is_additive_in_shared_and_dsh(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(temporary)
            (root / 'AGENTS.local.md').write_text('My local notes\n', encoding='utf-8')
            (root / 'CLAUDE.md').write_text('Read AGENTS.md\n', encoding='utf-8')
            (root / 'CLAUDE.local.md').write_text('Claude local notes\n', encoding='utf-8')
            shared = chain.resolve_chain(root)
            dsh = chain.resolve_chain(root, profile='dsh')
            self.assertEqual([s['path'] for s in shared['sources']],
                             ['AGENTS.md', 'AGENTS.local.md'])
            self.assertEqual([s['path'] for s in dsh['sources']],
                             ['AGENTS.md', 'CLAUDE.md', 'AGENTS.local.md',
                              'CLAUDE.local.md'])
            self.assertTrue(any('manual policy review' in w for w in dsh['warnings']))

    def test_dsh_same_scope_duplicate_is_collapsed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(temporary)
            (root / 'CLAUDE.md').write_text('  # Repository-wide rules\n\n',
                                            encoding='utf-8')
            result = chain.resolve_chain(root, profile='dsh')
            self.assertEqual([s['path'] for s in result['sources']], ['AGENTS.md'])
            self.assertEqual(result['skipped'],
                             [{'path': 'CLAUDE.md', 'reason': 'duplicate-in-scope'}])

    def test_codex_override_replaces_same_directory_agents(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(temporary)
            (root / 'src').mkdir()
            (root / 'src/AGENTS.md').write_text('Shared directory policy\n',
                                                encoding='utf-8')
            (root / 'src/AGENTS.override.md').write_text('Codex override\n',
                                                         encoding='utf-8')
            result = chain.resolve_chain(root, 'src/file.py', profile='codex')
            self.assertEqual([s['path'] for s in result['sources']],
                             ['AGENTS.md', 'src/AGENTS.override.md'])
            self.assertEqual(result['skipped'],
                             [{'path': 'src/AGENTS.md', 'reason': 'shadowed-by-override'}])
            self.assertTrue(any('override may replace' in w for w in result['warnings']))

    def test_codex_empty_override_does_not_shadow(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(temporary)
            (root / 'AGENTS.override.md').write_text('   \n', encoding='utf-8')
            result = chain.resolve_chain(root, profile='codex')
            self.assertEqual([s['path'] for s in result['sources']], ['AGENTS.md'])

    def test_claude_is_shim_only_not_implicit_agents_expansion(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(temporary)
            (root / 'CLAUDE.md').write_text('Read AGENTS.md\n', encoding='utf-8')
            result = chain.resolve_chain(root, profile='claude')
            self.assertEqual([s['path'] for s in result['sources']], ['CLAUDE.md'])
            self.assertTrue(any('not expanded' in w for w in result['warnings']))

    def test_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(temporary)
            with self.assertRaisesRegex(chain.InstructionChainError, 'escapes'):
                chain.resolve_chain(root, '../outside/file.py')
            with self.assertRaisesRegex(chain.InstructionChainError, 'relative'):
                chain.resolve_chain(root, root / 'AGENTS.md')

    def test_symlinked_instruction_source_cannot_escape_repository(self):
        with tempfile.TemporaryDirectory() as temporary, \
             tempfile.TemporaryDirectory() as external:
            root = self.make_root(temporary)
            outside = Path(external) / 'rules.md'
            outside.write_text('private rules\n', encoding='utf-8')
            (root / 'src').mkdir()
            try:
                (root / 'src/AGENTS.md').symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest('Symlinks unavailable')
            with self.assertRaisesRegex(chain.InstructionChainError, 'escapes'):
                chain.resolve_chain(root, 'src/a.py')
            self.assertTrue(any('escapes project' in e for e in chain.audit_sources(root)))

    def test_invalid_encoding_and_empty_sources_are_reported(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(temporary)
            (root / 'src').mkdir()
            (root / 'src/AGENTS.md').write_bytes(bytes([255]))
            errors = chain.audit_sources(root)
            self.assertTrue(any('UTF-8' in e for e in errors), errors)
            (root / 'src/AGENTS.md').write_text('\n\n', encoding='utf-8')
            errors = chain.audit_sources(root)
            self.assertTrue(any('Empty instruction source' in e for e in errors), errors)

    def test_advisory_budget_does_not_pretend_to_reproduce_host(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(temporary)
            result = chain.resolve_chain(root, max_bytes=4, include_content=True)
            self.assertIn('content', result['sources'][0])
            self.assertTrue(any('advisory budget' in w for w in result['warnings']))
            self.assertFalse(result['host_verified'])

    def test_cli_returns_nonzero_when_target_escapes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(temporary)
            command = [sys.executable, str(ROOT / 'scripts/instruction_chain.py'),
                       '--root', str(root), '--target', '../outside.txt']
            proc = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 2, proc.stderr)
            self.assertIn('escapes', proc.stderr)

    def test_repository_root_chain_is_inspectable(self):
        result = chain.resolve_chain(ROOT, profile='dsh')
        self.assertIn('AGENTS.md', [s['path'] for s in result['sources']])
        self.assertFalse(chain.audit_sources(ROOT))


if __name__ == '__main__':
    unittest.main()
