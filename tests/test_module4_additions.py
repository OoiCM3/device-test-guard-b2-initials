import unittest

from device_test_guard.disposition import decide_disposition
from device_test_guard.models import DeviceTestRecord
from device_test_guard.validation import validate_record


def record(device_id: str, passed: bool = True, temperature: float = 25.0, voltage: float = 1.0, retest_count: int = 0):
    return DeviceTestRecord(device_id, temperature, voltage, {"logic": passed}, retest_count)


class Module4AdditionalTests(unittest.TestCase):
    def test_voltage_boundaries_are_inclusive(self):
        self.assertEqual(validate_record(record("LOW_V", voltage=0.8)), ())
        self.assertEqual(validate_record(record("HIGH_V", voltage=1.2)), ())

    def test_exhausted_retest_is_held(self):
        batch = [record("DEV-001"), record("DEV-002", passed=False, retest_count=1)]
        disposition, _ = decide_disposition(batch, target_yield=90.0)
        self.assertEqual(disposition, "HOLD")

    def test_invalid_record_is_held(self):
        batch = [record("DEV-001", voltage=1.5)]
        disposition, _ = decide_disposition(batch, target_yield=90.0)
        self.assertEqual(disposition, "HOLD")


if __name__ == "__main__":
    unittest.main()
