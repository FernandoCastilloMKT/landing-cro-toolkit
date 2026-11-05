import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('guards', Path(__file__).parents[1] / 'scripts/audit_public_repo.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class PrivacyGuardsTests(unittest.TestCase):
    def test_credentials_are_detected_without_real_values(self):
        examples = {
            'Google OAuth secret': 'GOCSPX-' + 'a' * 30,
            'Google refresh token': '1//' + 'a' * 40,
            'Google OAuth client': '123456789012-' + 'a' * 24 + '.apps.googleusercontent.com',
            'Meta access token': 'EA' + 'a' * 80,
            'JWT': 'eyJ' + 'a' * 16 + '.' + 'b' * 16 + '.' + 'c' * 16,
        }
        for label, value in examples.items():
            with self.subTest(label=label):
                self.assertIsNotNone(audit.PATTERNS[label].search(value))

    def test_private_artifacts_are_blocked_even_when_empty(self):
        for name in ('credentials/empty.json', '.clasp.json', '.env.production', 'key.pem', '.openai/hosting.json', 'archive.zip'):
            with self.subTest(name=name):
                self.assertTrue(audit.blocked_path(Path(name)))
        self.assertFalse(audit.blocked_path(Path('.env.example')))

    def test_private_names_need_not_be_stored_in_the_repository(self):
        for text in ('ExampleCompany', 'example-company', 'EXAMPLE_COMPANY'):
            self.assertTrue(audit.confidential_match(text, ['example company']))
        self.assertFalse(audit.confidential_match('generic', ['example company']))
