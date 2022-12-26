import unittest
from pathlib import Path

from main import log_changed_ip

parent = Path(__file__).parent
test_tsv = parent / 'test.tsv'


def invoke_log_changed_ip(ip, time):
    log_changed_ip(lambda: ip, changes_filename=test_tsv.name, time_provider=lambda: time)


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self._unlink()

    def tearDown(self) -> None:
        self._unlink()

    def test_first_log(self):
        invoke_log_changed_ip('1.2.3.4', 'now1')
        self.assertTrue(test_tsv.exists())
        self.assertEqual('1.2.3.4\tnow1\n', test_tsv.read_text())

    def test_second_unchanged_log(self):
        invoke_log_changed_ip('1.2.3.4', 'now1')
        invoke_log_changed_ip('1.2.3.4', 'now2')
        self.assertTrue(test_tsv.exists())
        self.assertEqual('1.2.3.4\tnow1\n', test_tsv.read_text())

    def test_second_changed_log(self):
        invoke_log_changed_ip('1.2.3.4', 'now1')
        invoke_log_changed_ip('5.6.7.8', 'now2')
        self.assertTrue(test_tsv.exists())
        self.assertEqual('1.2.3.4\tnow1\n5.6.7.8\tnow2\n', test_tsv.read_text())

    def test_no_ip_available(self):
        invoke_log_changed_ip('1.2.3.4', 'now1')
        invoke_log_changed_ip(None, 'now2')
        self.assertTrue(test_tsv.exists())
        self.assertEqual('1.2.3.4\tnow1\n', test_tsv.read_text())

    def _unlink(self):
        test_tsv.unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()
