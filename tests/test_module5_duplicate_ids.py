import unittest

from device_test_guard.disposition import decide_disposition
from device_test_guard.models import DeviceTestRecord


def record(device_id: str, passed: bool = True, temperature: float = 25.0, voltage: float = 1.0, retest_count: int = 0):
    return DeviceTestRecord(device_id, temperature, voltage, {"logic": passed}, retest_count)


class Module5DuplicateIdentifierTests(unittest.TestCase):
    def test_duplicate_identifiers_hold_passing_batch(self):
        batch = [record("DEV-001", passed=True), record("DEV-001", passed=True)]
        disposition, _ = decide_disposition(batch, target_yield=90.0)
        self.assertEqual(disposition, "HOLD")

    def test_duplicate_identifiers_hold_below_target_batch(self):
        batch = [record("DEV-001", passed=True), record("DEV-001", passed=False, retest_count=0)]
        disposition, _ = decide_disposition(batch, target_yield=90.0)
        self.assertEqual(disposition, "HOLD")


if __name__ == "__main__":
    unittest.main()
