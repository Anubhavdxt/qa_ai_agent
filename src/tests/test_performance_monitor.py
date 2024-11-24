import unittest
import time
from agent.performance_monitor import PerformanceMonitor


class TestPerformanceMonitor(unittest.TestCase):
    def test_timing(self):
        monitor = PerformanceMonitor()

        monitor.start_timing("test")
        time.sleep(0.1)  # Simulate some processing time
        monitor.stop_timing("test")

        self.assertIn("test", monitor.timings)
        self.assertGreater(monitor.timings["test"], 0.1)

    def test_print_timings(self):
        monitor = PerformanceMonitor()

        monitor.start_timing("test")
        time.sleep(0.1)
        monitor.stop_timing("test")

        monitor.print_timings()  # This will print the timings to the console


if __name__ == "__main__":
    unittest.main()
