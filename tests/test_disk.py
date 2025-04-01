import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rich.console import Console
from monitor import disk

console = Console()

if __name__ == "__main__":
    disk.print_disk_usage(console)
