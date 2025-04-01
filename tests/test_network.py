import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rich.console import Console
from monitor import network

console = Console()

if __name__ == "__main__":
    console = Console()
    network.print_network_stats(console)
