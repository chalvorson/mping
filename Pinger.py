import datetime
import math
import time

from pythonping import ping as pping


class Pinger:
    """This class provides a Pinger object that you can use to calculate latency
    metrics to an ip address.  Use the ping() method to measure the latency and
    update metrics.

    The object keeps track of the mean, variance, standard deviation, minimum, and
    maximum internally.  The variance property is calculated using Welford's
    algorithm.  The standard deviation is the square root of the variance.
    """

    def __init__(self, ip: str):
        self.ip = ip
        self.n = 0
        self.last = 0
        self.mean = 0
        self.M2 = 0
        self.variance = None
        self.min = float("inf")
        self.max = float("-inf")
        self.lost_packets = 0
        self.last_lost = None

    def __add(self, x):
        self.n += 1
        delta = x - self.mean
        self.mean += delta / self.n
        self.M2 += delta * (x - self.mean)
        if self.n > 1:
            self.variance = self.M2 / (self.n - 1)
        self.min = min(self.min, x)
        self.max = max(self.max, x)

    def ping(self):
        resp = pping(self.ip, count=1, timeout=1)
        if resp.packets_lost > 0:
            self.lost_packets += int(resp.packets_lost)
            self.last_lost = datetime.datetime.now()
            self.last = None
        else:
            self.__add(resp.rtt_avg_ms)
            self.last = resp.rtt_avg_ms

        return True

    @property
    def avg(self):
        if self.n == 0:
            return None
        else:
            return self.mean

    @property
    def stddev(self):
        if self.variance is not None:
            return math.sqrt(self.variance)
        else:
            return None


if __name__ == "__main__":
    pstat = Pinger("1.1.1.1")

    for _ in range(30):
        pstat.ping()
        time.sleep(1)

    # Print the statistics
    print(f"IP: {pstat.ip}")
    print(f"Packets: {pstat.n}")
    print(f"Lost: {pstat.lost_packets}")
    print(f"Mean: {pstat.mean}")
    print(f"Minimum: {pstat.min}")
    print(f"Maximum: {pstat.max}")
    print(f"Variance: {pstat.variance}")
    print(f"Standard deviation: {pstat.stddev}")
