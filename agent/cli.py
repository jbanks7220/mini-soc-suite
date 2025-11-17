import argparse

def cli():
    parser = argparse.ArgumentParser(description="Mini-SOC Agent")

    parser.add_argument("--once", action="store_true",
                        help="Run a single log collection cycle")

    parser.add_argument("--realtime", action="store_true",
                        help="Run real-time log monitoring")

    return parser.parse_args()

