from pathlib import Path
from rich.console import Console
from rich.table import Table
from collections import defaultdict
import re
import sys


console = Console()

LOGS_PATH = Path(__file__).parent / "logs.txt"

#Using regex pattern
LINE_RE = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2})\s"
    r"(?P<time>\d{2}:\d{2}:\d{2})\s"
    r"(?P<level>\w+)\s"
    r"(?P<message>.+)"
)

#PArsing line
def parse_log_line(line):
  match = LINE_RE.match(line.strip())
  return match.groupdict() if match else None

#Loading log via yield with lazy for optimisation
def load_logs(file):
  path = Path(file)

  try:
    with open(path, mode='r', encoding="utf-8", errors="strict") as fh:
      for line in fh:
        log = parse_log_line(line)
        if log:
          yield log

  except FileNotFoundError:
    print("File not found, try again with correct path")
    sys.exit(1)

  except Exception as error:
    print(error)
    sys.exit(1)

#Filtering logs
def filter_logs_by_level(logs, level):
  #Using list comprehension, lowering log["level"] and compare
  return [log for log in logs if log["level"].lower() == level.lower()]


#Counting logs
def count_logs_by_level(logs):
  counts = defaultdict(int)

  for log in logs:
    counts[log["level"]] +=1

  return dict(counts)

#Printing table with results
def display_log_counts(counts):
  table = Table(title="Log Statistics")

  table.add_column("Рівень логування", style="cyan")
  table.add_column("Кількість", style="magenta")

  for level, count in counts.items():
    table.add_row(level, str(count))

  console.print(table)


def main():
    if len(sys.argv) < 2:
      console.print("[yellow]Usage:[/] python main.py <log_file> [level]")
      sys.exit(1)

    file = sys.argv[1]
    level = sys.argv[2] if len(sys.argv) > 2 else None

    logs = list(load_logs(file))
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if level:
      filtered_logs = filter_logs_by_level(logs, level)

      console.print(f"\n[bold yellow]Деталі логів для рівня '{level.upper()}':[/]\n")

      for log in filtered_logs:
        console.print(f"[green]{log['date']} {log['time']}[/] - {log['message']}")



#Run script like this one:
#   python3 main.py ROOT/goit-pycore-hw-05/task3/logs.txt  - to show logs
#   OR
#   python3 main.py ROOT/goit-pycore-hw-05/task3/logs.txt error -  to show logs and specific level kind
if __name__ == "__main__":
   main()