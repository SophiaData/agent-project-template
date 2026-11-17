# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
"""Regression tests for template bootstrapping and fail-closed quality gates."""
import importlib.util
import json
from pathlib import Path
import shutil
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

    def test_new_template_has_no_application_code(self):
        self.assertFalse(quality.has_application_code(ROOT))

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

    def test_template_scripts_execute(self):
        checks = [
            [sys.executable, 'scripts/verify_project.py'],
            [sys.executable, 'scripts/run_quality.py'],
        ]
        for argv in checks:
            with self.subTest(argv=argv):
                proc = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(proc.returncode, 0, proc.stderr)

    @staticmethod
    def policy(checks):
        return dict(schema_version=2, project_name='sample', project_type='python',
                    template_version='2.0.0', require_checks_when_code_exists=True,
                    quality_checks=checks, release_mode='manual')


if __name__ == '__main__':
    unittest.main()
