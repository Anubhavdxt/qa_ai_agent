import time


class PerformanceMonitor:
    """
    Observer class for monitoring performance metrics.
    """

    def __init__(self):
        self.timings = {}

    def start_timing(self, name):
        """
        Start timing a specific operation.
        :param name: Name of the operation.
        """
        self.timings[name] = time.time()

    def stop_timing(self, name):
        """
        Stop timing a specific operation.
        :param name: Name of the operation.
        """
        if name in self.timings:
            self.timings[name] = time.time() - self.timings[name]

    def print_timings(self):
        """
        Print the timings of all monitored operations.
        """
        for name, timing in self.timings.items():
            print(f"{name.capitalize().replace('_', ' ')} Time: {timing:.4f} seconds")
