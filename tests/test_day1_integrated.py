import unittest

from device_test_guard.models import DeviceTestRecord
from device_test_guard.service import analyse_batch
from device_test_guard.validation import validate_record


def record(device_id: str = "DEV-001", passed: bool = True, temperature: float = 25.0, voltage: float = 1.0, retest_count: int = 0):
    return DeviceTestRecord(device_id, temperature, voltage, {"logic": passed}, retest_count)


class Day1IntegratedTests(unittest.TestCase):
    def test_temperature_just_outside_range_is_rejected(self):
        low_temp_problems = validate_record(record(temperature=9.99))
        high_temp_problems = validate_record(record(temperature=85.01))
        self.assertIn("temperature is outside the training range", low_temp_problems)
        self.assertIn("temperature is outside the training range", high_temp_problems)

    def test_blank_device_identifier_is_rejected(self):
        problems = validate_record(record(device_id="   "))
        self.assertIn("device_id is required", problems)

    def test_empty_test_results_are_rejected(self):
        empty_results_record = DeviceTestRecord("DEV-001", 25.0, 1.0, {})
        problems = validate_record(empty_results_record)
        self.assertIn("at least one test result is required", problems)

    def test_empty_batch_summary_is_zero_and_held(self):
        summary = analyse_batch("EMPTY-BATCH", [])
        self.assertEqual(summary.record_count, 0)
        self.assertEqual(summary.yield_percent, 0.0)
        self.assertEqual(summary.disposition, "HOLD")


if __name__ == "__main__":
    unittest.main()
