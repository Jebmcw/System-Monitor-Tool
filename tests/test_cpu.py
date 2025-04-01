import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from monitor import cpu
from rich.console import Console


console = Console()

if __name__ == "__main__":
    cpu.print_cpu_usage(console)