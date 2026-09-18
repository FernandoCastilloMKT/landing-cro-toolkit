import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('audit', Path(__file__).parents[1] / 'scripts/audit_public_repo.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class HistoryPrivacyTests(unittest.TestCase):
    def test_email_policy(self):
        pattern = audit.PATTERNS['personal email']
        self.assertIsNotNone(pattern.search('private' + '@' + 'mail.test'))
        self.assertIsNone(pattern.search('123+demo' + '@' + 'users.noreply.github.com'))
        self.assertIsNone(pattern.search('alerts' + '@' + 'example.invalid'))

    def test_deleted_email_and_author_are_reported_without_values(self):
        with tempfile.TemporaryDirectory() as d:
            env = dict(os.environ, GIT_AUTHOR_NAME='Demo', GIT_COMMITTER_NAME='Demo',
                       GIT_AUTHOR_EMAIL='123+demo'+'@'+'users.noreply.github.com',
                       GIT_COMMITTER_EMAIL='123+demo'+'@'+'users.noreply.github.com')
            def git(*args):
                subprocess.run(['git', '-C', d, *args], check=True, env=env, capture_output=True)
            git('init')
            secret = 'private' + '@' + 'mail.test'
            path = Path(d) / 'sample.txt'
            path.write_text(secret)
            git('add', '.')
            git('-c', 'commit.gpgsign=false', 'commit', '-m', 'Example')
            path.write_text('removed')
            git('add', '.')
            git('-c', 'commit.gpgsign=false', 'commit', '-m', 'Remove example')
            findings = audit.history_findings(Path(d), 'HEAD')
            self.assertTrue(findings)
            self.assertNotIn(secret, str(findings))
            env['GIT_AUTHOR_EMAIL'] = secret
            git('-c', 'commit.gpgsign=false', 'commit', '--allow-empty', '-m', 'Identity check')
            self.assertGreater(len(audit.history_findings(Path(d), 'HEAD')), len(findings))


if __name__ == '__main__':
    unittest.main()
