# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
"""Regression tests for template bootstrapping and fail-closed quality gates."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


quality = load_module('template_quality', ROOT / 'scripts/run_quality.py')
verify = load_module('template_verify', ROOT / 'scripts/verify_project.py')
configure = load_module('template_configure', ROOT / 'scripts/configure_project.py')


class ProjectTemplateContract(unittest.TestCase):
    def test_governance_files_valid(self):
        self.assertEqual(verify.verify(ROOT), [])

    def test_template_version_matches_policy_without_schema_migration(self):
        policy = json.loads((ROOT / 'project-policy.json').read_text(encoding='utf-8'))
        version = (ROOT / 'TEMPLATE_VERSION').read_text(encoding='utf-8').strip()
        self.assertEqual(policy['schema_version'], 2)
        self.assertEqual(policy['template_version'], version)
        self.assertEqual(version, '2.3.0')

    def test_technology_profiles_are_present(self):
        profiles = ('python.md', 'typescript.md', 'java.md', 'data-engineering.md')
        for profile in profiles:
            self.assertTrue((ROOT / 'docs/standards' / profile).is_file(), profile)

    def test_defensive_pattern_documents_are_present(self):
        docs = ('README.md', 'general.md', 'data-engineering.md')
        for name in docs:
            self.assertTrue((ROOT / 'docs/defensive-patterns' / name).is_file(), name)

    def test_testing_policy_requires_independent_outcome_verification(self):
        policy = (ROOT / 'docs/testing.md').read_text(encoding='utf-8')
        self.assertIn('Verify actual outcomes', policy)
        self.assertIn("agent's own response", policy)

    def test_testing_policy_requires_supported_entry_path_for_shipped_behavior(self):
        policy = (ROOT / 'docs/testing.md').read_text(encoding='utf-8')
        self.assertIn('Exercise the supported execution path', policy)
        self.assertIn('built artifact', policy)

    def test_pr_template_requires_test_design_and_ai_disclosure(self):
        template = (ROOT / '.github/pull_request_template.md').read_text(encoding='utf-8')
        self.assertIn('## Test design', template)
        self.assertIn('## AI assistance (when applicable)', template)

    def test_quality_policy_accepts_optional_path_selectors(self):
        checks = [{'category': 'test', 'argv': ['python', '-m', 'pytest'],
                   'paths': ['src/**', 'tests/**/*.py', 'pyproject.toml']}]
        self.assertEqual(quality.validate_policy(self.policy(checks), True), checks)

    def test_quality_policy_rejects_unsafe_path_selectors(self):
        for patterns in (['../**'], ['/src/**'], ['src\\**'], ['src//tests']):
            checks = [{'category': 'test', 'argv': ['python', '-m', 'pytest'],
                       'paths': patterns}]
            with self.subTest(patterns=patterns):
                self.assertRaisesRegex(ValueError, 'paths', quality.validate_policy,
                                       self.policy(checks), True)

    def test_legacy_quality_checks_without_paths_remain_unconditional(self):
        checks = [{'category': 'test', 'argv': ['python', '-m', 'pytest']}]
        self.assertEqual(quality.select_checks(checks, ['docs/README.md'], True), checks)

    def test_path_glob_matches_root_and_nested_paths(self):
        self.assertTrue(quality.path_matches('tests/test_api.py', 'tests/**/*.py'))
        self.assertTrue(quality.path_matches('tests/unit/test_api.py', 'tests/**/*.py'))
        self.assertTrue(quality.path_matches('src/api.py', 'src/**'))
        self.assertFalse(quality.path_matches('web/app.ts', 'src/**'))

    def test_diff_selection_keeps_unscoped_checks_and_matching_checks(self):
        checks = [
            {'category': 'test', 'argv': ['pytest'], 'paths': ['src/**', 'tests/**']},
            {'category': 'lint', 'argv': ['ruff', 'check', '.']},
            {'category': 'build', 'argv': ['npm', 'run', 'build'], 'paths': ['web/**']},
        ]
        selected = quality.select_checks(checks, ['src/api.py'], True)
        self.assertEqual([entry['category'] for entry in selected], ['test', 'lint'])

    def test_source_change_without_matching_test_fails_closed(self):
        checks = [
            {'category': 'test', 'argv': ['pytest'], 'paths': ['tests/**']},
            {'category': 'lint', 'argv': ['ruff', 'check', '.'], 'paths': ['docs/**']},
        ]
        self.assertRaisesRegex(
            ValueError, 'no test check matched',
            quality.select_checks, checks, ['src/api.py'], True,
        )

    def test_documentation_change_can_skip_unmatched_scoped_checks(self):
        checks = [{'category': 'test', 'argv': ['pytest'], 'paths': ['src/**', 'tests/**']}]
        self.assertEqual(quality.select_checks(checks, ['docs/README.md'], True), [])

    def test_git_diff_reports_both_sides_of_a_rename(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            subprocess.run(['git', 'init'], cwd=root, check=True, capture_output=True)
            subprocess.run(['git', 'config', 'user.email', 'template-test@example.invalid'],
                           cwd=root, check=True, capture_output=True)
            subprocess.run(['git', 'config', 'user.name', 'Template Test'],
                           cwd=root, check=True, capture_output=True)
            source = root / 'src'
            source.mkdir()
            old_file = source / 'old.py'
            old_file.write_text('value = 1\n', encoding='utf-8')
            subprocess.run(['git', 'add', '.'], cwd=root, check=True, capture_output=True)
            subprocess.run(['git', 'commit', '-m', 'base'], cwd=root, check=True, capture_output=True)
            base = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, check=True,
                                  capture_output=True, text=True).stdout.strip()
            old_file.rename(source / 'new.py')
            subprocess.run(['git', 'add', '-A'], cwd=root, check=True, capture_output=True)
            subprocess.run(['git', 'commit', '-m', 'rename'], cwd=root, check=True,
                           capture_output=True)
            head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, check=True,
                                  capture_output=True, text=True).stdout.strip()
            changed = quality.get_changed_paths(base, head, root)
            self.assertEqual(set(changed), {'src/old.py', 'src/new.py'})

    def test_git_diff_failure_does_not_silently_skip_checks(self):
        with tempfile.TemporaryDirectory() as path:
            self.assertRaisesRegex(ValueError, 'cannot resolve Git change scope',
                                   quality.get_changed_paths, 'missing-base', 'HEAD', Path(path))

    def test_quality_workflow_fetches_history_and_supplies_diff_base(self):
        workflow = (ROOT / '.github/workflows/quality.yml').read_text(encoding='utf-8')
        self.assertIn('fetch-depth: 0', workflow)
        self.assertIn('QUALITY_BASE_SHA', workflow)
        self.assertIn('scripts/run_quality.py --base', workflow)

    def test_empty_directory_has_no_application_code(self):
        with tempfile.TemporaryDirectory() as path:
            self.assertFalse(quality.has_application_code(Path(path)))

    def test_consuming_project_with_source_is_not_a_contract_failure(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            (root / 'backend').mkdir()
            (root / 'backend' / 'server.py').write_text('print("hello")\n')
            self.assertTrue(quality.has_application_code(root))
            checks = [{'category': 'test', 'argv': ['python', '-m', 'pytest']}]
            self.assertEqual(quality.validate_policy(self.policy(checks), True), checks)

    def test_source_detection_handles_nonstandard_dirs(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            (root / 'backend/service').mkdir(parents=True)
            (root / 'backend/service/api.go').write_text('package api\n')
            self.assertTrue(quality.has_application_code(root))

    def test_empty_test_list_rejected_once_source_exists(self):
        self.assertRaisesRegex(ValueError, 'test check', quality.validate_policy,
                               self.policy([]), True)

    def test_lint_only_cannot_substitute_for_tests(self):
        checks = [{'category': 'lint', 'argv': ['python', '-m', 'compileall', 'src']}]
        self.assertRaisesRegex(ValueError, 'test check', quality.validate_policy,
                               self.policy(checks), True)

    def test_noop_cannot_claim_test_success(self):
        checks = [{'category': 'test', 'argv': ['echo', 'success']}]
        self.assertRaisesRegex(ValueError, 'placeholder/no-op', quality.validate_policy,
                               self.policy(checks), True)

    def test_valid_test_command_accepted(self):
        checks = [{'category': 'test', 'argv': ['python', '-m', 'unittest']}]
        self.assertEqual(quality.validate_policy(self.policy(checks), True), checks)

    def test_unsafe_release_setting_rejected(self):
        policy = self.policy([])
        policy['release_mode'] = 'automatic'
        self.assertRaisesRegex(ValueError, 'manual', quality.validate_policy, policy, False)

    def test_node_detection_and_test_script(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            (root / 'package.json').write_text(json.dumps({'scripts': {'test': 'vitest run'}}))
            self.assertEqual(configure.detect_stack(root), 'node')
            self.assertEqual(configure.candidate_checks(root, 'node'),
                             [{'category': 'test', 'argv': ['npm', 'test']}])

    def test_verifier_negative_control_rejects_missing_required_document(self):
        with tempfile.TemporaryDirectory() as path:
            errors = verify.verify(Path(path))
            self.assertIn('Missing: docs/defensive-patterns/general.md', errors)

    def test_verifier_negative_control_rejects_incomplete_pattern(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            doc = root / 'docs/defensive-patterns/general.md'
            doc.parent.mkdir(parents=True)
            doc.write_text(
                '## Deliberately incomplete rule\n\n'
                '### Applies when\nA test fixture activates this rule.\n',
                encoding='utf-8',
            )
            errors = []
            verify.verify_defensive_patterns(root, errors)
            self.assertTrue(
                any('missing subsection "Required invariant"' in error for error in errors),
                errors,
            )

    def test_verifier_negative_control_rejects_broken_markdown_link(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            doc = root / 'docs/defensive-patterns/README.md'
            doc.parent.mkdir(parents=True)
            doc.write_text('[deliberately broken](missing-target.md)\n', encoding='utf-8')
            errors = verify.verify(root)
            self.assertTrue(
                any(error.startswith('Broken/unsafe link: docs/defensive-patterns/README.md')
                    for error in errors),
                errors,
            )

    def test_template_governance_script_executes(self):
        argv = [sys.executable, 'scripts/verify_project.py']
        proc = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    @staticmethod
    def policy(checks):
        return dict(schema_version=2, project_name='sample', project_type='python',
                    template_version='2.3.0', require_checks_when_code_exists=True,
                    quality_checks=checks, release_mode='manual')


if __name__ == '__main__':
    unittest.main()
