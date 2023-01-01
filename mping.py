import concurrent.futures
import signal
import time

import click
from rich.live import Live
from rich.table import Table

from Pinger import Pinger

keep_going = True


def handler(signum, frame):
    global keep_going
    keep_going = False


signal.signal(signal.SIGINT, handler)


def do_ping(pingers: list):
    """Calls the ping method on each pinger object.  Speeds up the ping process
    by putting the pingers in a thread pool.

    Args:
        pingers (list): a list of Pinger objects which have the IP address and
        ping metrics.
    """
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as pool:
        for pinger in pingers:
            futures.append(pool.submit(pinger.ping))

    concurrent.futures.wait(
        futures, timeout=3.0, return_when=concurrent.futures.ALL_COMPLETED
    )


def generate_table(pingers: list) -> Table:
    """Make a Rich table and add a row for each IP address."""
    table = Table()
    table.add_column("IP Address")
    table.add_column("Last (ms)", justify="center", style="green")
    table.add_column("Min (ms)", justify="center", style="cyan")
    table.add_column("Max (ms)", justify="center", style="cyan")
    table.add_column("Avg (ms)", justify="center", style="deep_pink4")
    table.add_column("StdDev (ms)", justify="center", style="deep_pink4")
    table.add_column("Success", justify="center", style="green")
    table.add_column("Fail", justify="center", style="red")
    table.add_column("Loss (%)", justify="center", style="red")
    table.add_column("Last Fail", justify="right", style="yellow")

    do_ping(pingers)

    for pinger in pingers:
        table.add_row(
            f"{pinger.ip}",
            f"" if pinger.last is None else f"{pinger.last:>4.1f}",
            f"" if pinger.min == float("inf") else f"{pinger.min:>4.1f}",
            f"" if pinger.max == float("-inf") else f"{pinger.max:>4.1f}",
            f"" if pinger.avg is None else f"{pinger.avg:>4.1f}",
            f"" if pinger.stddev is None else f"{pinger.stddev:>4.1f}",
            f"{pinger.n:}",
            f"{pinger.lost_packets}",
            f""
            if (pinger.n + pinger.lost_packets) == 0
            else f"{(pinger.lost_packets/(pinger.n+pinger.lost_packets)*100):>6.2f}",
            f"" if pinger.last_lost is None else f"{pinger.last_lost:%H:%M:%S}",
        )
    return table


@click.command()
@click.option("--count", "-c", default=5, help="Number of pings.")
@click.argument("ip_list", required=True, nargs=-1)
def main(count: int, ip_list: list):
    global keep_going
    pingers = [Pinger(ip=ip) for ip in ip_list]

    with Live(generate_table(pingers), refresh_per_second=4) as live:
        if count > 0:
            for _ in range(count - 1):
                time.sleep(1.0)
                live.update(generate_table(pingers))
        else:
            while keep_going:
                time.sleep(1.0)
                live.update(generate_table(pingers))


if __name__ == "__main__":
    main()
